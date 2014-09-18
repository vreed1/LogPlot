import sys
import logPlotView as lpv
from PyQt4.QtGui import QApplication
from datetime import datetime, timedelta
from utils import *
from dbTools import *
from grapher import *
from tideDataRetriever import *

class Controller:

    def __init__(self):
        self.currentFile = ""
        self.tempRecords = []
        self.graph = Grapher()
        self.dbSummary = DailySummary()
        self.view = lpv.LogPlot()
        self.view.show()
        self.ConnectViewEvents()

    def ConnectViewEvents(self):
        #Connect buttons from Upload tab
        self.view.ui.FileBrowseButton.clicked.connect(self.FileBrowse)
        self.view.ui.RecordButton.clicked.connect(self.Record)
        self.view.ui.PlotExcelButton.clicked.connect(self.PlotExcel)
        self.view.ui.previewSummary.toggled.connect(self.PreviewSummary)
        self.view.ui.previewAll.toggled.connect(self.PreviewAll)

        #Connect buttons from Plot tab
        self.view.ui.plotButton.clicked.connect(self.PlotFromDatabase)        

#-----------------Event Handlers---------------------   
    def FileBrowse(self):
        path = self.view.FileBrowseDialog()
        if not self.FileNameValid(path, '.csv'): return
        self.view.ui.filePath.setText(path)
        self.view.ui.previewSummary.setChecked(True)
        
    def Record(self):
        filename = self.view.ui.filePath.text()
        if self.currentFile != filename:
            self.ReadRecords(filename)
        #Get daily summary
        summaryRecords = Utils.makeSummary(self.tempRecords)
        #Add to daily summary table in database
        self.dbSummary.insert(summaryRecords)

    def PreviewSummary(self):
        self.PlotPreview(self.view.ui.filePath.text())

    def PreviewAll(self):
        self.PlotPreview(self.view.ui.filePath.text(), summary = False)        
        
    def PlotExcel(self):
        #Get directory of save location
        savePath = self.view.SaveDialog("untitled.xlsx", "Excel files (*xlsx)")
        if not self.FileNameValid(savePath, '.xlsx'): return
        if not self.tempRecords:
            #TODO: error, no records to plot
            return
        if self.view.ui.previewAll.isChecked():
            self.graph.plotTempsExcel(savePath, self.tempRecords)
        else:
            summaryRecords = Utils.makeSummary(self.tempRecords)
            self.graph.plotTempSummaryExcel(savePath, summaryRecords)

    def DateString(self, date, desiredFormat = '%m/%d/%Y'):
        #dateStr = datetime.strftime(date, desiredFormat)
        return datetime.strftime(date, desiredFormat)

    def PlotFromDatabase(self):
        # Get the date and interval specifications for the plot
        beginDate = self.DateString(self.view.ui.beginDate.date().toPyDate())
        endDate = self.DateString(self.view.ui.endDate.date().toPyDate())
        interval = str(self.view.ui.PlotInterval.currentText())
        # Get requested temperature fields
        temperatureFields = []
        levels = {}
        temperatureFields.append(self.dbSummary.Fields.SampleDate.name)
        if self.view.ui.MaxTempCheck.isChecked():
            temperatureFields.append(self.dbSummary.Fields.MaxTemp.name)
        if self.view.ui.MinTempCheck.isChecked():
            temperatureFields.append(self.dbSummary.Fields.MinTemp.name)
        if self.view.ui.AvgTempCheck.isChecked():
            temperatureFields.append(self.dbSummary.Fields.AvgTemp.name)
        # Read temperature records from database (returns a dictionary of (field, values)
        data = self.dbSummary.get(beginDate, endDate, temperatureFields)
        # If water levels were also requested, get that information from CO-OPS
        if self.view.ui.WaterLevelCheck.isChecked():
            levels = self.MakeTideRequest(beginDate, endDate, interval,
                                          self.view.ui.Units.currentIndex(),
                                          str(self.view.ui.Datum.currentText()))
            figure = self.graph.plotMatPlotDualYAxis('SampleDate', data, levels, '%m/%d/%Y', 'Date',
                                                     'Temp', 'Water Level')
            self.view.UpdateCanvas(self.view.plotCanvas, figure)
        else:
            xSeries = self.dbSummary.Fields.SampleDate.name
            dateFormat = self.dbSummary.DateFormat
            figure = self.graph.plotTempsFromDictionary(xSeries, data, dateFormat)
            self.view.UpdateCanvas(self.view.plotCanvas, figure)
        
        #figure = self.graph.plotTempsFromDictionary(xSeries, data, dateFormat)
        #figure = self.graph.plotMatPlot('dates', levels, '%Y-%m-%d', 'Date', 'Level')

        #Update canvas
        #self.view.UpdateCanvas(self.view.plotCanvas, figure)

#-----------------Helper Methods--------------------- 
    
    def PlotPreview(self, filename, summary = True):
        if self.currentFile != filename:
            self.ReadRecords(filename)
        #Get appropriate records and plot
        figure = None
        if summary:
            records = Utils.makeSummary(self.tempRecords)
            figure = self.graph.plotTempSummary(records)
        else:
            figure = self.graph.plotTemps(self.tempRecords)       
        #Update preview canvas in view
        self.view.UpdateCanvas(self.view.previewCanvas, figure)

    def FileNameValid(self, filename, ending):
        if not filename or not filename.endswith(ending):
            #TODO: error dialog, must provide valid filename
            return False
        else: return True

    def ReadRecords(self, filename):
        #Store name of file
        self.currentFile = filename
        #Read in records
        self.tempRecords = Utils.readRecordsFromFile(filename)

    def MakeTideRequest(self, beginDate, endDate, interval, units, datum):
        station = '9452210' #Juneau, AK
        product = 'water_level'
        timeZone = 'gmt'
        rformat = 'json'
        rUnits = Units(units).name
        requestInterval = self.GetInterval(beginDate, endDate, interval)
        if requestInterval is None:
            #TODO: handle error, requested date range exceeds retrieval time of requested interval
            return
        #Convert date formats to ones suitable for tide api and generate all parameters
        begin = datetime.strftime(datetime.strptime(beginDate, '%m/%d/%Y'),'%Y%m%d')
        end = datetime.strftime(datetime.strptime(endDate, '%m/%d/%Y'), '%Y%m%d')
        params = TideParameters(station, begin, end, product,
                                datum, rUnits, timeZone, requestInterval, rformat)
        #Make the api call and retrieve data
        tdr = TideDataRetriever()
        return tdr.makeRequest(params.Params)

    def GetInterval(self, beginDate, endDate, interval):
        begin = datetime.strptime(beginDate, '%m/%d/%Y')
        end = datetime.strptime(endDate, '%m/%d/%Y')
        diff = int((end - begin).days)
        if interval == 'Daily':
            if (diff <= MaxRetrieval.SIX_MINUTE.value): return '6'
            elif (diff <= MaxRetrieval.HOUR.value): return 'h'
            else: return None #Beyond max retrieval of hourly, only monthly means available for Juneau
        else:
            if (diff <= MaxRetrieval.MONTH.value): return 'm'
            else: return None


        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    controller = Controller()
    sys.exit(app.exec_())
