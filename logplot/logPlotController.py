import sys
import logPlotView as lpv
from utils import *
from dbTools import *
from grapher import *
from PyQt4.QtGui import QApplication

class Controller:

    def __init__(self):
        self.currentFile = ""
        self.tempRecords = []
        self.graph = Grapher()
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
        #self.view.ui.plotButton.clicked.connect(self.PlotFromDatabase)        

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
        DailySummary.insert(summaryRecords)

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

#-----------------Helper Methods--------------------- 
    
    def PlotPreview(self, filename, summary = True):
        if self.currentFile != filename:
            self.ReadRecords(filename)
        #Get appropriate records and plot
        figure = None
        if summary:
            records = Utils.makeSummary(self.tempRecords)
            figure = self.graph.plotSummaryPreview(records)
        else:
            figure = self.graph.plotTempPreview(self.tempRecords)       
        #Update preview canvas in view
        self.view.UpdatePreviewCanvas(figure)

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



        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    controller = Controller()
    sys.exit(app.exec_())
