# -*- coding: utf-8 -*-
"""
Created on Wed Oct 31 11:28:37 2018

@author: aelshaha
"""

from pubsub import pub
from Events import EVENTS
    
class Model():
    _years = {}
    _sites = {}
    _commodities = {}
    _processes = {}

    def __init__(self):
        return        

    def AddYear(self, year):
        if not (year in self._years):
            self._years[year] = {'selected': '', 'discountRate': '0.00', 'co2Limit': 'inf', 'co2Budet': '1,000,000'}
            
            for data in self._commodities.values():
                data[year] = self.InitializeCommodity()
            
            for data in self._processes.values():
                data[year] = self.InitializeProcess()
            
            #notify subscribers that a year is added
            pub.sendMessage(EVENTS.YEAR_ADDED, years=self._years)

    def RemoveYears(self, years):
        notify = False
        for year in years:
            self._years.pop(year)
            
            for data in self._commodities.values():
                data.pop(year)
                
            for data in self._processes.values():
                data.pop(year)
                
            notify = True
            
        #notify subscribers that a year is removed
        if notify:
            pub.sendMessage(EVENTS.YEAR_REMOVED, years=self._years)
            
    
    def AddSite(self, site):
        if not (site in self._sites):
            self._sites[site] = {'selected': '', 'siteArea':  '100,000'}
            #notify subscribers that a site is added
            pub.sendMessage(EVENTS.SITE_ADDED, sites=self._sites)

    def RemoveSites(self, sites):
        notify = False
        for site in sites:
            self._sites.pop(site)
            notify = True
            
        #notify subscribers that a site is removed
        if notify:
            pub.sendMessage(EVENTS.SITE_REMOVED, sites=self._sites)
            
    def AddCommodity(self, commType):
        commId = str.replace(commType, ' ', '_') + str(len(self._commodities) + 1)
        data = {}
        for year in self._years:
            data[year] = self.InitializeCommodity()
        self._commodities[commId] = data
        
        #notify subscribers that a site is added
        pub.sendMessage(EVENTS.COMMODITY_ADDED, commId=commId, commType = commType)
        
    def InitializeCommodity(self):
        data = {'price': '0.00', 'max':  'Inf', 'maxPerHour': 'Inf'}
        return data
        
    def GetCommodity(self, commId):
        return self._commodities[commId]

    def AddProcess(self, processName):
        processId = str.replace(processName, ' ', '_') + str(len(self._processes) + 1)
        data = {}
        for year in self._years:
            data[year] = self.InitializeProcess()
        self._processes[processId] = data
        
        #notify subscribers that a site is added
        pub.sendMessage(EVENTS.PROCESS_ADDED, processId=processId, processName=processName)
        
    def InitializeProcess(self):
        return {'instCap': '0.00', 'lifetime': '0.00', 'capLo': '0.00', 'capUp': '0.00', 'invCost': '0.00', 'fixCost': 'Inf', 
            'varCost': 'Inf', 'startupCost': 'Inf', 'wacc': '0.05', 'maxGrad': 'Inf', 'minFraction': 'Inf', 'depreciation': '20', 
            'areaPerCap': 'Inf'}
    
    def GetProcess(self, processId):
        return self._processes[processId]