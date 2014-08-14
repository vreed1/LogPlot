from utils import *
from dbTools import *
from grapher import *

class Controller:

    def __init__(self):
        self.currentFile = ""
        self.tempRecords = []
        self.graph = Grapher()
        
    def readRecords(self, filename):
        #Store name of file
        self.currentFile = filename
        #Read in records
        self.tempRecords = Utils.readRecordsFromFile(filename)
        
    def RecordDataFromFile(self, filename):
        if self.currentFile != filename:
            self.readRecords(filename)
        #Get daily summary
        summaryRecords = Utils.makeSummary(self.tempRecords)
        #Add to daily summary table in database
        DailySummary.insert(summaryRecords)

    def PlotSummaryPreview(self, filename):
        if self.currentFile != filename:
            self.readRecords(filename)
        #Create summary
        summaryRecords = Utils.makeSummary(self.tempRecords)
        #figure should be reference to MatPlot figure
        return self.graph.plotSummaryPreview(summaryRecords)

    def PlotDetailedPreview(self, filename):
        if self.currentFile != filename:
            self.readRecords(filename)
        #figure should be reference to MatPlot figure
        return self.graph.plotTempPreview(self.tempRecords)

    def PlotTempsExcel(self, filename):
        if not self.tempRecords:
            #TODO: error, no records to plot
            return
        return self.graph.plotTempsExcel(filename, self.tempRecords)

    def PlotSummaryExcel(self, filename):
        if not self.tempRecords:
            #TODO: error, no records to plot
            return
        summaryRecords = Utils.makeSummary(self.tempRecords)
        return self.graph.plotTempSummaryExcel(filename, summaryRecords)
        
