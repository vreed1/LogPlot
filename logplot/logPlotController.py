from utils import *
from dbTools import *
from grapher import *

class Controller:

    def __init__(self):
        self.currentFile = ""
        self.tempRecords = []
        
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
        graph = Grapher()
        return graph.plotSummaryPreview(summaryRecords)

    def PlotDetailedPreview(self, filename):
        if self.currentFile != filename:
            self.readRecords(filename)
        #figure should be reference to MatPlot figure
        graph = Grapher()
        return graph.plotTempPreview(self.tempRecords)
        
