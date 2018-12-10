# -*- coding: utf-8 -*-
"""
Created on Wed Oct 31 11:28:37 2018

@author: aelshaha
"""

from pubsub import pub
from Events import EVENTS

import DataConfig as config
import pandas as pd
import math

class RESModel():
    
    def __init__(self, data=None):
        self._years             = {}
        self._sites             = {}
        self._models            = {}
        self._transmissions     = {}
        self._trnsmCommodities  = {}
        self._gl                = self.InitializeGlobalParams()
        if data:
            self._gl = data['_gl']
            pub.sendMessage(EVENTS.GL_PARAMS_LOADED, gl=self._gl)
            self._sites = data['_sites']
            pub.sendMessage(EVENTS.SITE_ADDED, sites=self._sites)
            self._years = data['_years']
            pub.sendMessage(EVENTS.YEAR_ADDED, years=self._years)
            for k, v in data['_models'].items():
                self._models[k] = SiteModel(k, 
                                            sorted(self._years.keys()),
                                            v['_commodities'],
                                            v['_processes'],
                                            v['_connections']                                            
                                  )

#-----------------------------------------------------------------------------#
    def InitializeGlobalParams(self):
        data = {}
        data['Value'] = SiteModel.InitializeData(config.DataConfig.GLOBAL_PARAMS)
        return data
#-----------------------------------------------------------------------------#
#-----------------------------------------------------------------------------#
    def InitializeSite(self, name):
        return SiteModel.InitializeData(config.DataConfig.SITE_PARAMS)
#-----------------------------------------------------------------------------#
    def AddSite(self, siteName):
        status = 0        
        if not (siteName in self._sites):
            self._sites[siteName]  = self.InitializeSite(siteName)
            self._models[siteName] = SiteModel(siteName, list(self._years.keys()))
            #notify subscribers that a site is added
            pub.sendMessage(EVENTS.SITE_ADDED, sites=self._sites)
        else:
            status = 1
        
        return status
#-----------------------------------------------------------------------------#
    def RemoveSites(self, sites):
        notify = 0
        for site in sites:
            self._sites.pop(site)
            self._models.pop(site)
            notify += 1
            
        #notify subscribers that a site is removed
        if notify > 0:
            pub.sendMessage(EVENTS.SITE_REMOVED, sites=self._sites, removeCount=notify)
#-----------------------------------------------------------------------------#
    def GetSites(self):
        return sorted(self._sites.keys())
#-----------------------------------------------------------------------------#
    def InitializeYear(self):
        return SiteModel.InitializeData(config.DataConfig.YEAR_PARAMS)
#-----------------------------------------------------------------------------#        
    def AddYear(self, year):
        if not (year in self._years):
            self._years[year] = self.InitializeYear()
            for m in self._models.values():
                m.AddYear(year)
            for v in self._transmissions.values():
                v['Years'][year] = SiteModel.InitializeData(config.DataConfig.TRANS_PARAMS)
            
            #notify subscribers that a year is added
            pub.sendMessage(EVENTS.YEAR_ADDED, years=self._years)
#-----------------------------------------------------------------------------#
    def RemoveYears(self, years):
        for year in years:
            self._years.pop(year)
            for m in self._models.values():
                m.RemoveYear(year)
            
        #notify subscribers that years are removed
        pub.sendMessage(EVENTS.YEAR_REMOVED, years=self._years, removeCount=len(years))
#-----------------------------------------------------------------------------#    
    def GetSiteModel(self, siteName):
        return self._models[siteName]
#-----------------------------------------------------------------------------#
    def GetGlobalParams(self):
        return self._gl
#-----------------------------------------------------------------------------#
    def CreateNewTrnsm(self):
        trnsId = 'NewTrnsm#' + str(len(self._transmissions) + 1)
        data = {}
        data['SiteIn'] = ''
        data['SiteOut'] = ''
        data['CommName'] = ''
        data['Years'] = {}
        data['Id'] = trnsId
        data['Name'] = trnsId
        data['Type'] = 'Trnsm'
        for year in self._years:
            data['Years'][year] = SiteModel.InitializeData(config.DataConfig.TRANS_PARAMS)
            
        return data
#-----------------------------------------------------------------------------#
    def SaveTransmission(self, data):
        trnsmId = data['Id']
        trnsmName = data['Name']
        success = True
        for v in self._transmissions.values():
            if v['Name'] == trnsmName and v['Id'] != trnsmId:
                success = False
                break
        if success:
            self.SaveTrnsmCommodities(data)
            if trnsmId not in self._transmissions:
                self._transmissions[trnsmId] = data
                pub.sendMessage(EVENTS.TRNSM_ADDED, objId=trnsmId)
            else:
                pub.sendMessage(EVENTS.TRNSM_EDITED, objId=trnsmId)
        
        return success            
#-----------------------------------------------------------------------------#
    def SaveTrnsmCommodities(self, data):
        #In part
        commInId = data['SiteIn'] + '.' + data['CommName']
        m = self._models[data['SiteIn']]
        commIn = m.GetCommByName(data['CommName'])
        self._trnsmCommodities[commInId] = commIn
        data['IN'] = [commInId]

        #out part
        commOutId = data['SiteOut'] + '.' + data['CommName']
        m = self._models[data['SiteOut']]
        commOut = m.GetCommByName(data['CommName'])
        self._trnsmCommodities[commOutId] = commOut            
        data['OUT'] = [commOutId]
#-----------------------------------------------------------------------------#
    def GetTransmission(self, trnsmId):
        return self._transmissions[trnsmId]
#-----------------------------------------------------------------------------#
    def CreateDF(self, tuples, names, columns, values):
        df = None
        if len(tuples) > 0:
            index = pd.MultiIndex.from_tuples(tuples, names=names)
            df = pd.DataFrame(values, columns=columns, index=index)
            
        return df
#-----------------------------------------------------------------------------#        
    def GetGlobalDF(self):
        tuples = []
        values = []
        years = sorted(self._years.keys())
        for year in years:
            if year == years[0]:
                #Discount rate
                prop = config.DataConfig.GLOBAL_PARAMS[0][config.DataConfig.PARAM_KEY]
                tuples.append((year, prop))
                values.append(self._gl['Value'][prop])
                #co2 budget
                prop = config.DataConfig.GLOBAL_PARAMS[1][config.DataConfig.PARAM_KEY]
                tuples.append((year, prop))
                values.append(self._gl['Value'][prop])
            data = self._years[year]
            for k, v in data.items():
                #skip 'selected'
                if k == config.DataConfig.YEAR_PARAMS[0][config.DataConfig.PARAM_KEY]:
                    continue
                
                tuples.append((year, k))
                values.append(v)
            if year == years[-1]:
                #Weight
                prop = config.DataConfig.GLOBAL_PARAMS[2][config.DataConfig.PARAM_KEY]
                tuples.append((year, prop))
                values.append(self._gl['Value'][prop])
        
        names = ['support_timeframe', 'Property']
        return self.CreateDF(tuples, names, ['value'], values)
#-----------------------------------------------------------------------------#        
    def GetSitesDF(self):
        tuples  = []
        values  = []
        columns = ['area']
        years = sorted(self._years.keys())
        for year in years:
            for site, data in self._sites.items():
                tuples.append((year, site))
                for col in columns:
                    values.append(data[col])
        
        names = ['support_timeframe', 'Name']
        return self.CreateDF(tuples, names, columns, values)
#-----------------------------------------------------------------------------#        
    def GetCommoditiesDF(self):
        tuples  = []
        values  = []
        columns = ['price', 'max', 'maxperhour']
        years = sorted(self._years.keys())
        for year in years:
            for site, m in self._models.items():
                ids = sorted(m._commodities.keys())
                for k in ids:
                    comm = m._commodities[k]
                    t = (year, site, comm['Name'], comm['Type'])
                    tuples.append(t)
                    data = comm['Years'][year]
                    v = []
                    for col in columns:
                        s = data[col]
                        if comm['Type'] in (config.DataConfig.COMM_SUPIM, 
                                            config.DataConfig.COMM_DEMAND):
                            s = math.nan
                        v.append(s)
                    values.append(v)
        
        names = ['support_timeframe', 'Site', 'Commodity', 'Type']
        return self.CreateDF(tuples, names, columns, values)
#-----------------------------------------------------------------------------#        
    def GetProcessesDF(self):
        tuples  = []
        values  = []
        columns = []
        for c in config.DataConfig.PROCESS_PARAMS:
            columns.append(c[config.DataConfig.PARAM_KEY])
        years = sorted(self._years.keys())
        for year in years:
            for site, m in self._models.items():
                ids = sorted(m._processes.keys())
                for k in ids:
                    p = m._processes[k]
                    if p['Type'] == 'Storage':
                        continue
                    t = (year, site, p['Name'])
                    tuples.append(t)
                    data = p['Years'][year]
                    v = []
                    for col in columns:
                        s = data[col]
                        if year != years[0] and col in (columns[0], columns[1]):
                            s = math.nan
                        v.append(s)
                    values.append(v)
        
        names = ['support_timeframe', 'Site', 'Process']
        return self.CreateDF(tuples, names, columns, values)
#-----------------------------------------------------------------------------#        
    def GetStoragesDF(self):
        tuples  = []
        values  = []
        columns = []
        for c in config.DataConfig.STORAGE_PARAMS:
            columns.append(c[config.DataConfig.PARAM_KEY])
        years = sorted(self._years.keys())
        for year in years:
            for site, m in self._models.items():
                ids = sorted(m._processes.keys())
                for k in ids:
                    strg = m._processes[k]
                    if strg['Type'] != 'Storage':
                        continue
                    commName = m._commodities[strg['IN'][0]]['Name']
                    t = (year, site, strg['Name'], commName)
                    tuples.append(t)
                    data = strg['Years'][year]
                    v = []
                    for col in columns:
                        s = data[col]
                        if year != years[0] and col in ('inst-cap-c', 
                                                        'inst-cap-p', 
                                                        'lifetime'):
                            s = math.nan
                        v.append(s)
                    values.append(v)
        
        names = ['support_timeframe', 'Site', 'Storage', 'Commodity']
        return self.CreateDF(tuples, names, columns, values)
#-----------------------------------------------------------------------------#        
    def GetConnectionsDF(self):
        tuples  = []
        values  = []
        columns = []
        for c in config.DataConfig.CONNECTION_PARAMS:
            columns.append(c[config.DataConfig.PARAM_KEY])
        years = sorted(self._years.keys())
        for year in years:
            for site, m in self._models.items():
                ids = sorted(m._connections.keys())
                for k in ids:
                    conn = m._connections[k]
                    t = (year, 
                         m._processes[conn['Proc']]['Name'], 
                         m._commodities[conn['Comm']]['Name'],
                         conn['Dir'].title())
                    tuples.append(t)
                    data = conn['Years'][year]
                    v = []
                    for col in columns:
                        v.append(data[col])
                    values.append(v)
        
        names = ['support_timeframe', 'Process', 'Commodity', 'Direction']
        return self.CreateDF(tuples, names, columns, values)
#-----------------------------------------------------------------------------#        
    def GetCommTimeSerDF(self, commTypes):
        #columns
        data = {}
        for site, m in self._models.items():
            ids = sorted(m._commodities.keys())
            for k in ids:
                comm = m._commodities[k]
                if comm['Type'] not in commTypes:
                    continue
                col = site + '.' + comm['Name']
                data[col] = comm
        #tuples        
        years = sorted(self._years.keys())
        t = range(0, 8761)
        tuples  = [(x, y) for x in years for y in t]
        names = ['support_timeframe', 't']
        df = self.CreateDF(tuples, names, [], [])
        for col, comm in data.items():
            v = []
            for year in years:
                timeSer = comm['Years'][year]['timeSer']
                l = timeSer.split('|')
                #print('l', len(l))
                v = v + l
            df[col] = pd.Series(v, index=df.index)
        
        #print(df.info(verbose=True))
        return df
#-----------------------------------------------------------------------------#
    def GetDemandTimeSerDF(self):
        return self.GetCommTimeSerDF([config.DataConfig.COMM_DEMAND])
#-----------------------------------------------------------------------------#
    def GetSupImTimeSerDF(self):
        return self.GetCommTimeSerDF([config.DataConfig.COMM_SUPIM])
#-----------------------------------------------------------------------------#
    def GetBuySellTimeSerDF(self):
        commTypes = [config.DataConfig.COMM_BUY, config.DataConfig.COMM_SELL]
        return self.GetCommTimeSerDF(commTypes)        
#-----------------------------------------------------------------------------#
    def GetDsmDF(self):
        tuples  = []
        values  = []
        columns = []
        dsmCols = [x for x in config.DataConfig.COMMODITY_PARAMS[5:]]
        for c in dsmCols:
            columns.append(c[config.DataConfig.PARAM_KEY])
        years = sorted(self._years.keys())
        for year in years:
            for site, m in self._models.items():
                ids = sorted(m._commodities.keys())
                for k in ids:
                    comm = m._commodities[k]
                    if comm['Type'] != config.DataConfig.COMM_DEMAND or comm['DSM'] != True:
                        continue
                        
                    t = (year, site, comm['Name'])
                    tuples.append(t)
                    data = comm['Years'][year]
                    v = []
                    for col in columns:
                        s = data[col]                        
                        v.append(s)
                    values.append(v)
        
        names = ['support_timeframe', 'Site', 'Commodity']
        return self.CreateDF(tuples, names, columns, values)        
#-----------------------------------------------------------------------------#
#-----------------------------------------------------------------------------#    
class SiteModel():

    def __init__(self, name, years, commodities=None, processes=None, connections=None):
        self._name           = name
        self._years          = years
        self._commodities    = {}
        self._processes      = {}
        self._connections    = {}
        
        if commodities:
            self._commodities = commodities
        if processes:
            self._processes = processes
        if connections:
            self._connections = connections
        
    def InitializeData(cols):
        data = {}
        for col in cols:
            data[col[config.DataConfig.PARAM_KEY]] = col[config.DataConfig.PARAM_DEFVALUE]

        return data        
        
    def InitializeCommodity(self):
        return SiteModel.InitializeData(config.DataConfig.COMMODITY_PARAMS)
        
    def InitializeProcess(self):
        return SiteModel.InitializeData(config.DataConfig.PROCESS_PARAMS)
        
    def InitializeStorage(self):
        return SiteModel.InitializeData(config.DataConfig.STORAGE_PARAMS)
    
    def InitializeConnection(self):
        return SiteModel.InitializeData(config.DataConfig.CONNECTION_PARAMS)
        
    def AddYear(self, year):
        self._years.append(year)
        
        for data in self._commodities.values():
            data['Years'][year] = self.InitializeCommodity()
        
        for data in self._processes.values():
            if data['Type'] == 'Storage':
                data['Years'][year] = self.InitializeStorage()
            else:
                data['Years'][year] = self.InitializeProcess()
            
        for data in self._connections.values():
            data['Years'][year] = self.InitializeConnection()

    def RemoveYear(self, year):
        self._years.remove(year)
        
        for data in self._commodities.values():
            data['Years'].pop(year)
            
        for data in self._processes.values():
            data['Years'].pop(year)
            
        for data in self._connections.values():
            data['Years'].pop(year)
            
    def GetCommodityGroup(self, commType):
        grp = '2-1'
        if commType in (config.DataConfig.COMM_SUPIM, config.DataConfig.COMM_BUY):
            grp = '0-1'
        elif commType in (config.DataConfig.COMM_STOCK):
            grp = '1-1'
        elif commType in (config.DataConfig.COMM_ENV):
            grp = '2-2'
            
        return grp
            
    def CreateNewCommodity(self, commType):
        grp = self.GetCommodityGroup(commType)
        num = str(len(self._commodities) + 1)
        if(len(num) < 2):
            num = '0' + num
        commId = grp + '_' + num + '_' + str.replace(commType, ' ', '_')
        data = {}
        data['Years'] = {}
        data['Id'] = commId
        data['Name'] = commType + '#' + num
        data['Type'] = commType
        data['Group'] = grp[0]
        data['Color'] = (0,0,0)
        data['DSM'] = False
        for year in self._years:
            data['Years'][year] = self.InitializeCommodity()
        
        return data
    
    def SaveCommodity(self, data):
        commId = data['Id']
        commName = data['Name']
        success = True
        for v in self._commodities.values():
            if v['Name'] == commName and v['Id'] != commId:
                success = False
                break
        if success:
            if commId not in self._commodities:
                self._commodities[commId] = data
                pub.sendMessage(EVENTS.COMMODITY_ADDED + self._name, objId=commId)
            else:
                pub.sendMessage(EVENTS.COMMODITY_EDITED + self._name, objId=commId)
        
        #Add further checks for status
        return success
        
    def GetCommodity(self, commId):
        if commId in self._commodities:
            return self._commodities[commId]

    def GetCommodityList(self):
        x = {}
        ids = sorted(self._commodities.keys())        
        for k in ids:
            x[k] = {'selected': '', 'Name': self._commodities[k]['Name'], 'Action': '...'}
        
        return x

    def CreateNewProcess(self):
        processId = 'NewProcess#' + str(len(self._processes) + 1)
        data = {}
        data['IN'] = []
        data['OUT'] = []
        data['Years'] = {}
        data['Id'] = processId
        data['Name'] = processId
        data['Type'] = ''
        for year in self._years:
            data['Years'][year] = self.InitializeProcess()   
            
        return data
    
    
    def SaveProcess(self, data):
        processId = data['Id']
        processName = data['Name']
        status = 0
        for v in self._processes.values():
            if v['Name'] == processName and v['Id'] != processId:
                status = 1
                break
        
        if len(data['IN']) == 0 and len(data['OUT']) == 0:
            status = 2
        
        if status == 0:                        
            self.SaveConnections(processId, data['IN'], 'IN')
            self.SaveConnections(processId, data['OUT'], 'OUT')
            if processId not in self._processes:
                self._processes[processId] = data
                pub.sendMessage(EVENTS.PROCESS_ADDED + self._name, objId=processId)
            else:
                pub.sendMessage(EVENTS.PROCESS_EDITED + self._name, objId=processId)
        
        #Add further checks for status
        return status

    def GetProcess(self, processId):
        return self._processes[processId]  
    
    def AddConnection(self, procId, commId, In_Out):
        connId = procId+'$'+commId+'$'+In_Out
        if connId not in self._connections.keys():            
            yearsData = {}
            for year in self._years:
                yearsData[year] = self.InitializeConnection()
            data = {}            
            data['Dir'] = In_Out
            data['Proc'] = procId
            data['Comm'] = commId
            data['Years'] = yearsData
            self._connections[connId] = data

        return connId
        
    def SaveConnections(self, processId, commList, direction):
        #Remove deselcted connections
        idsToDel = []
        for k, v in self._connections.items():
            if v['Proc'] == processId and v['Dir'] == direction:
                if v['Comm'] not in commList:
                    idsToDel.append(k)
        
        for k in idsToDel:
            self._connections.pop(k)
        
        for comm in commList:
            self.AddConnection(processId, comm, direction)
        #
        #print(direction, self._connections.keys())
            
    def GetConnection(self, procId, commId, In_Out):
        connId = self.AddConnection(procId, commId, In_Out)
        return self._connections[connId]

    def CreateNewStorage(self):
        storageId = 'NewStorage#' + str(len(self._processes) + 1)
        data = {}
        data['IN'] = []
        data['OUT'] = []
        data['Years'] = {}
        data['Id'] = storageId
        data['Name'] = storageId
        data['Type'] = 'Storage'
        for year in self._years:
            data['Years'][year] = self.InitializeStorage()   
            
        return data

    def GetStorage(self, storageId):
        return self._processes[storageId]

    def GetSiteName(self):
        return self._name
        
    def GetCommByName(self, commName):
        for v in self._commodities.values():
            if v['Name'] == commName:
                return v
        
        return None
