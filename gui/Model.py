# -*- coding: utf-8 -*-
"""
Created on Wed Oct 31 11:28:37 2018

@author: aelshaha
"""

from pubsub import pub
from Events import EVENTS

import DataConfig as config

class RESModel():
    
    def __init__(self):
        self._years  = {}
        self._sites  = {}
        self._models = {}

    def InitializeSite(self, name):
        return SiteModel.InitializeData(config.DataConfig.SITE_PARAMS)

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

    def RemoveSites(self, sites):
        notify = 0
        for site in sites:
            self._sites.pop(site)
            self._models.pop(site)
            notify += 1
            
        #notify subscribers that a site is removed
        if notify > 0:
            pub.sendMessage(EVENTS.SITE_REMOVED, sites=self._sites, removeCount=notify)
            
    def InitializeYear(self):
        return SiteModel.InitializeData(config.DataConfig.YEAR_PARAMS)
        
    def AddYear(self, year):
        if not (year in self._years):
            self._years[year] = self.InitializeYear()
            for m in self._models.values():
                m.AddYear(year)
            
            #notify subscribers that a year is added
            pub.sendMessage(EVENTS.YEAR_ADDED, years=self._years)

    def RemoveYears(self, years):
        for year in years:
            self._years.pop(year)
            for m in self._models.values():
                m.RemoveYear(year)
            
        #notify subscribers that years are removed
        pub.sendMessage(EVENTS.YEAR_REMOVED, years=self._years, removeCount=len(years))
    
    def GetSiteModel(self, siteName):
        return self._models[siteName]
            
#-----------------------------------------------------------------------------#    
class SiteModel():

    def __init__(self, name, years):
        self._name           = name
        self._years          = years
        self._commodities    = {}
        self._processes      = {}
        self._connections    = {}
        
    def InitializeData(cols):
        data = {}
        for col in cols:
            data[col[config.DataConfig.PARAM_KEY]] = col[config.DataConfig.PARAM_DEFVALUE]

        return data
        
        
    def InitializeCommodity(self):
        return SiteModel.InitializeData(config.DataConfig.COMMODITY_PARAMS)
        
    def InitializeProcess(self):
        return SiteModel.InitializeData(config.DataConfig.PROCESS_PARAMS)
    
    def InitializeConnection(self):
        return SiteModel.InitializeData(config.DataConfig.CONNECTION_PARAMS)
        
    def AddYear(self, year):
        self._years.append(year)
        
        for data in self._commodities.values():
            data['Years'][year] = self.InitializeCommodity()
        
        for data in self._processes.values():
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
        if commType in (config.DataConfig.COMM_SUPLM, config.DataConfig.COMM_BUY):
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
                pub.sendMessage(EVENTS.COMMODITY_ADDED + self._name)
            else:
                pub.sendMessage(EVENTS.COMMODITY_EDITED + self._name)
        
        #Add further checks for status
        return success
        
    def GetCommodity(self, commId):        
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
                pub.sendMessage(EVENTS.PROCESS_ADDED + self._name)
            else:
                pub.sendMessage(EVENTS.PROCESS_EDITED + self._name)
        
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