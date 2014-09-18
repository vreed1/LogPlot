from enum import Enum
import requests, json
from datetime import datetime

class MaxRetrieval(Enum):
    #Relates interval to max retrieval time (in days)
    SIX_MINUTE = 31
    HOUR = 365
    MONTH = 3650

class Units(Enum):
    english = 0
    metric = 1
    
class TideParameters:
    #For more detail on possible parameters and values, see http://tidesandcurrents.noaa.gov/api/
    def __init__(self, station, beginDate, endDate, dataProduct, datum, units,
                 timeZone, interval, rformat):
        self._params = {}
        #Station should be a 7 character station id
        self._params['station'] = station
        #date can be yyyyMMdd, yyyyMMdd HH:mm, MM/dd/yyyy, or MM/dd/yyyy HH:mm
        self._params['begin_date'] = beginDate
        self._params['end_date'] = endDate
        #data product (for now, only expecting water_level)
        self._params['product'] = dataProduct
        #datum (e.g. MHHW, MTL, MLLW, etc)
        self._params['datum'] = datum
        #Units (metric (Celsius, meters) or english (fahrenheit, feet))
        self._params['units'] = units
        #time zone (gmt, lst, or lst_ldt)
        self._params['time_zone'] = timeZone
        #interval (depends on the station. Some common ones: 6 (6-minute), h (hourly), m (monthly))
        #Max retrieval times:
        #6-minute : 31 days
        #hourly : 1 year
        #monthly: 10 years
        self._params['interval'] = interval
        #format of response (json, xml or csv)
        self._params['format'] = rformat
        
    @property
    def Params(self):
        return self._params

class TideDataRetriever:
    def __init__(self):
        #Station ID hard coded to Juneau,AK for now
        #self.stationId = 9452210
        #Api web address
        self.webAddress = r'http://tidesandcurrents.noaa.gov/api/datagetter'

    def makeRequest(self, parameters):
        #expecting 'parameters' to be a dictionary of query params
        r = requests.get(self.webAddress, params=parameters)
        jdata = r.json()
        data = jdata['data']
        interval = parameters['interval']
        
        dateRecs = []
        waterlevels = []
        if interval == '6' or interval == 'h':
            uniqueDates = set(self.getDate(r['t']).date() for r in data)
            dates = sorted(uniqueDates)
            for date in dates:
                dateRecords = [r for r in data if self.getDate(r['t']).date() == date]
                levels = [float(r['v']) for r in dateRecords]
                avgLevel = sum(levels)/float(len(dateRecords))
                dateRecs.append(date)
                waterlevels.append(avgLevel)
        else:
            for record in data:
                dateRecs.append(self.getDate(record['t']).date())
                waterlevels.append(float(record['v']))
        return {'dates':dateRecs, 'levels':waterlevels}

    def getDate(self, dateStr):
        return datetime.strptime(dateStr, '%Y-%m-%d %H:%M')

    def getMatPlotDict(self, data):
        dates = []
        levels = []
        for key,val in data.items():
            dates.append(key)
            levels.append(val)
        return {'dates':dates, 'levels':levels}
        

    
