# -*- coding: utf-8 -*-
"""
Created on Wed Oct 31 11:28:37 2018

@author: aelshaha
"""

from pubsub import pub
from Events import EVENTS

import DataConfig as config
    
class Model():
    _years          = {}
    _sites          = {}
    _commodities    = {}
    _processes      = {}
    _connections    = {}

    def __init__(self):
        return    
        
    def InitializeData(self, cols):
        data = {}
        for col in cols:
            data[col[config.DataConfig.PARAM_KEY]] = col[config.DataConfig.PARAM_DEFVALUE]

        return data
        
    def InitializeYear(self):
        return self.InitializeData(config.DataConfig.YEAR_PARAMS)
    
    def InitializeSite(self):
        return self.InitializeData(config.DataConfig.SITE_PARAMS)
        
    def InitializeCommodity(self):
        return self.InitializeData(config.DataConfig.COMMODITY_PARAMS)
        
    def InitializeProcess(self):
        ecoData = self.InitializeData(config.DataConfig.PROCESS_ECO_PARAMS)
        techData = self.InitializeData(config.DataConfig.PROCESS_TECH_PARAMS)
        data = ecoData.copy()
        data.update(techData)
        return data
    
    def InitializeConnection(self):
        return {'ratio': '1.00', 'ratioMin': ''}

    def AddYear(self, year):
        if not (year in self._years):
            self._years[year] = self.InitializeYear()
            
            for data in self._commodities.values():
                data[year] = self.InitializeCommodity()
            
            for data in self._processes.values():
                data[year] = self.InitializeProcess()
                
            for data in self._connections.values():
                data[year] = self.InitializeConnection()
            
            #notify subscribers that a year is added
            pub.sendMessage(EVENTS.YEAR_ADDED, years=self._years)

    def RemoveYears(self, years):
        notify = 0
        for year in years:
            self._years.pop(year)
            
            for data in self._commodities.values():
                data.pop(year)
                
            for data in self._processes.values():
                data.pop(year)
                
            for data in self._connections.values():
                data.pop(year)
                
            notify += 1
            
        #notify subscribers that a year is removed
        if notify > 0:
            pub.sendMessage(EVENTS.YEAR_REMOVED, years=self._years, removeCount=notify)
            
    
    def AddSite(self, site):
        if not (site in self._sites):
            self._sites[site] = self.InitializeSite()
            #notify subscribers that a site is added
            pub.sendMessage(EVENTS.SITE_ADDED, sites=self._sites)

    def RemoveSites(self, sites):
        notify = 0
        for site in sites:
            self._sites.pop(site)
            notify += 1
            
        #notify subscribers that a site is removed
        if notify > 0:
            pub.sendMessage(EVENTS.SITE_REMOVED, sites=self._sites, removeCount=notify)
            
    def AddCommodity(self, commType):
        commId = str.replace(commType, ' ', '_') + '#' + str(len(self._commodities) + 1)
        data = {}
        for year in self._years:
            data[year] = self.InitializeCommodity()
        self._commodities[commId] = data
        
        #notify subscribers that a commodity is added
        pub.sendMessage(EVENTS.COMMODITY_ADDED, commId=commId, commType = commType)
        
    
        
    def GetCommodity(self, commId):
        return self._commodities[commId]

    def AddProcess(self, processName):
        processId = str.replace(processName, ' ', '_') + '#' + str(len(self._processes) + 1)
        data = {}
        for year in self._years:
            data[year] = self.InitializeProcess()
        self._processes[processId] = data
        
        #notify subscribers that a process is added
        pub.sendMessage(EVENTS.PROCESS_ADDED, processId=processId, processName=processName)
        
    
    
    def GetProcess(self, processId):
        return self._processes[processId]

    def AddInboundConnection(self, fromCommId, toProcessId):
        connId = self.AddConnection(fromCommId, toProcessId)
        if connId:
            pub.sendMessage(EVENTS.CONNECTION_ADDED, direction='Inbound', connId=connId, commId=fromCommId, processId=toProcessId)
        
    def AddOutboundConnection(self, fromProcessId, toCommId):
        connId = self.AddConnection(fromProcessId, toCommId)
        if connId:
            pub.sendMessage(EVENTS.CONNECTION_ADDED, direction='Outbound', connId=connId, commId=toCommId, processId=fromProcessId)   
    
    def AddConnection(self, fromId, toId):
        connId = fromId + '>' + toId
        if connId not in self._connections.keys():
            data = {}
            for year in self._years:
                data[year] = self.InitializeConnection()
            self._connections[connId] = data
            return connId
            
        return
        
    
            
    def GetConnection(self, connId):
        return self._connections[connId]