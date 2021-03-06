import os
import pypyodbc
from collections import defaultdict
from enum import Enum

class dbTools:
    #Parameters for Access Database connection
    driver = 'Microsoft Access Driver (*.mdb, *.accdb)'
    dbName = 'Sample.accdb'

    def __init__(self):
        parentPath = os.path.abspath('..')
        self.dbPath = os.path.join(parentPath, self.dbName)
        self.ConnectionString = 'Driver={%s};DBQ=%s' % (self.driver, self.dbPath)

    def insert(self, tableName, fields, values):
        #Connect to the the database
        conn = pypyodbc.connect(self.ConnectionString)

        #Get an operational cursor of the connected database
        cur = conn.cursor()

        #Add records to the database
        #Expects fields and values to each consist of comma-separated list of strings (see DailySummary for example)
        insertCmd = 'INSERT INTO %s(%s)' % (tableName, fields)
        for value in values:
            cmd = ('%s VALUES(%s)') % (insertCmd, value)
            cur.execute(cmd)

        #Commit changes
        cur.commit()

        #Close connection
        conn.close()

    def get(self, tableName, dateBegin, dateEnd, fields):
        #Connect to the the database
        conn = pypyodbc.connect(self.ConnectionString)

        #Get an operational cursor of the connected database
        cur = conn.cursor()

        #Select data from desired fields between desired dates
        fieldStr = ','.join(fields)
        select = "SELECT %s FROM %s" % (fieldStr, tableName)
        cur.execute(select + " WHERE SampleDate BETWEEN ? AND ?",
                    [dateBegin, dateEnd])

        #Package data into a dictionary -> (fieldName, Records)
        data = defaultdict(list)
        for row in cur:
            i = 0
            for field in fields:
                data[field].append(row[i])
                i += 1            

        return data
    
class DailySummary():   
    _tablename = ""
    _dateformat = ""
    _fields = None
    def __init__(self):
        DailySummary._tablename = 'DailySummary'
        DailySummary._fields = Enum('Fields', 'SampleDate MaxTemp MinTemp AvgTemp')
        DailySummary._dateformat = '%m/%d/%Y'

    @property
    def TableName(self):
        return DailySummary._tablename
    @property
    def Fields(self):
        return DailySummary._fields
    @property
    def DateFormat(self):
        return DailySummary._dateformat

    #Returns a comma separated string of the desired field names (default all possible fields)
    def GetStringOfFields(self, selectedFields = None):
        if selectedFields is None:
            return ','.join([field.name for field in self.Fields])
        return ','.join([self.Fields(field).name for field in selectedFields])

    def insert(self, records):
        values = []
        for record in records:
            dtString = record.Date.strftime('%m/%d/%y')
            values.append("'%s', %f, %f, %f" % (dtString, record.MaxTemp, record.MinTemp, record.AvgTemp))
        tools = dbTools()
        tools.insert(self.TableName, self.GetStringOfFields(), values)

    def get(self, dateBegin, dateEnd, fieldsToQuery):
        tools = dbTools()
        data = tools.get(self.TableName, dateBegin, dateEnd, fieldsToQuery)
        data['SampleDate'] = [x.date() for x in data['SampleDate']]
        return data
            
    
    
