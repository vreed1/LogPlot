import pypyodbc
from datetime import datetime
import csv
        
class TempRecord:
    def __init__(self, datetime, temp):
        self.DateTime = datetime
        self.Temperature = temp
        
class TempSummaryRecord:
    def __init__(self, date, minTemp, maxTemp, avgTemp):
        self.Date = date
        self.MinTemp = minTemp
        self.MaxTemp = maxTemp
        self.AvgTemp = avgTemp
        
class Utils:
    @staticmethod
    def readRecordsFromFile(filename):
        tempRecords = []
        with open(filename, newline='') as f:
            reader = csv.reader(f)
            
            next(reader) #Skip plot title line
            next(reader) #Skip column header names
            #Can use header to check units of temperature
            #Should we automatically convert to fahrenheit or celsius?

            #Read data
            for row in reader:
                dt = datetime.strptime(row[1], '%m/%d/%y %I:%M:%S %p')
                temp = float(row[2])
                tempRecords.append(TempRecord(dt, temp))
        return tempRecords
                
    @staticmethod
    def makeSummary(records):
        summaryRecords = []

        #Get the unique dates from the temp records
        uniqueDates = set(o.DateTime.date() for o in records)
        dates = sorted(uniqueDates)

        #Get summaries for each date: minTemp, maxTemp, avgTemp
        for date in dates:
            dateRecords = [r for r in records if r.DateTime.date() == date]
            temps = [r.Temperature for r in dateRecords]
            minTemp = min(temps)
            maxTemp = max(temps)
            sumTemp = sum(temps)
            avgTemp = sumTemp/float(len(dateRecords))
            summaryRecords.append(TempSummaryRecord(date,minTemp,maxTemp,avgTemp))

        return summaryRecords
