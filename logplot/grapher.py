import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cbook as cbook
import xlsxwriter as xl
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

        #Format the x axis
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter(dateFormat))
        plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
        
        #Plot the data series
        for key, vals in ySeries.items():
            graph.plot(x, vals, label=key)

        #Add a legend if necessary
        if addLegend:
            handles, labels = graph.get_legend_handles_labels()
            graph.legend(handles,labels)

        #Add axis labels
        plt.xlabel('Date')
        plt.ylabel('Temperature ($^\circ$F)')
        
        plt.gcf().autofmt_xdate()

        return figure

    def plotTempsExcel(self, filename, tempRecords):
        dates = [record.DateTime for (record) in tempRecords]
        temps = [record.Temperature for (record) in tempRecords]
        data = {'SampleDate':dates, 'Temperature':temps}
        dateFormat = 'mm/dd/yy hh:mm'
        return self.plotExcel(filename, data, dateFormat)

    def plotTempSummaryExcel(self, filename, tempSummaryRecords):
        dates = [record.Date for (record) in tempSummaryRecords]
        maxTemp = [record.MaxTemp for (record) in tempSummaryRecords]
        minTemp = [record.MinTemp for (record) in tempSummaryRecords]
        avgTemp = [record.AvgTemp for (record) in tempSummaryRecords]
        data = {'SampleDate':dates, 'MaxTemp':maxTemp, 'MinTemp':minTemp, 'AvgTemp':avgTemp}
        dateFormat = 'mm/dd/yy'
        return self.plotExcel(filename, data, dateFormat)
        
    def plotExcel(self, filename, data, dateformat):
        #Construct workbook, worksheet, chartsheet and chart
        workbook = xl.Workbook(filename)
        worksheet = workbook.add_worksheet()
        #chartsheet = workbook.add_chartsheet()
        chart = workbook.add_chart({'type': 'scatter', 'subtype': 'straight'})
        dateFormat = workbook.add_format({'num_format': dateformat})

        #Add data to worksheet and get potential minimum values for y axis
        column = 1
        numDates = len(data['SampleDate'])
        potentialMin = []
        for field, records in data.items():
            if (field == 'SampleDate'):
                worksheet.write(0, 0, 'Date')
                worksheet.write_column(1,0,records, dateFormat)
            else:
                worksheet.write(0, column, field)
                worksheet.write_column(1,column,records)
                chart.add_series({
                    'name': ['Sheet1', 0, column],
                    'categories': ['Sheet1', 1, 0, numDates, 0],
                    'values': ['Sheet1', 1, column, len(records), column],
                    'marker': {'type': 'none'}
                })
                potentialMin.append(min(records))
                column += 1
                
	#Add axis labels, set minimum value for y axis (rounded down to nearest 10)
        minY = min(potentialMin)
        minY = minY - (minY%10)
        chart.set_x_axis({'name': 'Date'})
        chart.set_y_axis({'name': 'Temperature (degree Fahrenheit)', 'min':minY})

        #chartsheet.set_chart(chart)
        worksheet.insert_chart('F7', chart)
        workbook.close()
