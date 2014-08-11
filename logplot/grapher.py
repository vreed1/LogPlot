import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cbook as cbook
import datetime as dt

class Grapher:
    def plotTempPreview(self, tempRecords):      
        x = [record.DateTime for (record) in tempRecords]
        temps = {'Temperature': [record.Temperature for (record) in tempRecords]}
        dateFormat = '%m/%d/%Y %H:%M'
        return self.plotMatPlot(x, temps, dateFormat)
        
    def plotSummaryPreview(self, tempSummaryRecords):
        x = [record.Date for (record) in tempSummaryRecords]
        maxTemp = [record.MaxTemp for (record) in tempSummaryRecords]
        minTemp = [record.MinTemp for (record) in tempSummaryRecords]
        avgTemp = [record.AvgTemp for (record) in tempSummaryRecords]
        ySeries = {'maxTemp':maxTemp, 'minTemp':minTemp, 'avgTemp':avgTemp}
        dateFormat = '%m/%d/%Y'
        return self.plotMatPlot(x, ySeries, dateFormat, addLegend = True)

    def plotMatPlot(self, x, ySeries, dateFormat, addLegend = False):
        # 'x' expected to hold list of dates
        # 'ySeries' expected to be a dictionary, where:
        # key = series name
        # values = list of series values
        
        figure = plt.figure()
        graph = figure.add_subplot(1,1,1)

        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter(dateFormat))
        plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())

        for key, vals in ySeries.items():
            graph.plot(x, vals, label=key)

        if addLegend:
            handles, labels = graph.get_legend_handles_labels()
            graph.legend(handles,labels)

        plt.gcf().autofmt_xdate()

        return figure
