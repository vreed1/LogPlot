import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cbook as cbook
import xlsxwriter as xl
import datetime as dt

class Grapher:
    def extractSeriesFromRecords(self, tempRecords):
        dates = []
        temps = []
        for record in tempRecords:
            dates.append(record.DateTime)
            temps.append(record.Temperature)
        return {'dates':dates, 'Temperature': temps}

    def extractSeriesFromSummaryRecords(self, tempSummaryRecords):
        dates = []
        maxTemp = []
        minTemp = []
        avgTemp = []
        for record in tempSummaryRecords:
            dates.append(record.Date)
            maxTemp.append(record.MaxTemp)
            minTemp.append(record.MinTemp)
            avgTemp.append(record.AvgTemp)
        return {'dates':dates, 'maxTemp':maxTemp, 'minTemp':minTemp, 'avgTemp':avgTemp}
    
    def plotTemps(self, tempRecords):
        data = self.extractSeriesFromRecords(tempRecords)
        dateFormat = '%m/%d/%Y %H:%M'
        return self.plotMatPlot('dates', data, dateFormat, 'Date', 'Temperature ($^\circ$F)')
        
    def plotTempSummary(self, tempSummaryRecords):
        data = self.extractSeriesFromSummaryRecords(tempSummaryRecords)
        dateFormat = '%m/%d/%Y'
        return self.plotMatPlot('dates', data, dateFormat, 'Date', 'Temperature ($^\circ$F)', addLegend = True)

    def plotTempsFromDictionary(self, xSeriesName, data, dateFormat):
        return self.plotMatPlot(xSeriesName, data, dateFormat, 'Date', 'Temperature ($^\circ$F)', addLegend = True)

    def plotTempsExcel(self, filename, tempRecords):
        data = self.extractSeriesFromRecords(tempRecords)
        dateFormat = 'mm/dd/yy hh:mm'
        return self.plotExcel(filename, data, dateFormat)

    def plotTempSummaryExcel(self, filename, tempSummaryRecords):
        data = self.extractSeriesFromSummaryRecords(tempSummaryRecords)
        dateFormat = 'mm/dd/yy'
        return self.plotExcel(filename, data, dateFormat)
    
    def plotMatPlot(self, xSeriesName, data, dateFormat, xLabel, yLabel, addLegend = False):
        # 'data' expected to be a dictionary where:
        # key = series name
        # values = list of series values
        # xSeriesName should match name of key for the x-axis series
        
        figure = plt.figure()
        graph = figure.add_subplot(1,1,1)

        #Format the x axis
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter(dateFormat))
        plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
        
        #Plot the data series
        x = data.pop(xSeriesName, None)
        if not x: return
        for key, vals in data.items():
            graph.plot(x, vals, label=key)

        #Add a legend if necessary
        if addLegend:
            handles, labels = graph.get_legend_handles_labels()
            graph.legend(handles,labels)

        #Add axis labels
        plt.xlabel(xLabel)
        plt.ylabel(yLabel)
        
        plt.gcf().autofmt_xdate()

        return figure
        
    def plotExcel(self, filename, data, dateformat):
        #Construct workbook, worksheet, chartsheet and chart
        workbook = xl.Workbook(filename)
        worksheet = workbook.add_worksheet()
        #chartsheet = workbook.add_chartsheet()
        chart = workbook.add_chart({'type': 'scatter', 'subtype': 'straight'})
        dateFormat = workbook.add_format({'num_format': dateformat})

        #Add dates to the first column of the worksheet
        dates = data.pop('dates', None)
        if not dates: return
        numDates = len(dates)
        worksheet.write(0, 0, 'Date')
        worksheet.write_column(1, 0, dates, dateFormat)
        
        #Add data to worksheet and get potential minimum values for y axis
        column = 1
        potentialMin = []
        for field, records in data.items():
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
