# -*- coding: utf-8 -*-
"""
Created on Wed Oct 31 11:35:21 2018

@author: aelshaha
"""
import Model as model
import MainView as view
import CommodityForm as cf
import ProcessForm as pf

from pubsub import pub
from Events import EVENTS

class Controller():
    def __init__(self):
        #Model part
        self._model = model.Model()
        
        #view part
        self._view = view.MainView()
        self._view.Maximize()
        self._view.Show()
        
        #subscribe on Views events
        pub.subscribe(self.AddYear, EVENTS.YEAR_ADDING)
        pub.subscribe(self.RemoveYears, EVENTS.YEAR_REMOVING)
        
        pub.subscribe(self.AddSite, EVENTS.SITE_ADDING)
        pub.subscribe(self.RemoveSites, EVENTS.SITE_REMOVING)
        
        pub.subscribe(self.AddCommodity, EVENTS.COMMODITY_ADDING)
        pub.subscribe(self.EditCommodity, EVENTS.COMMODITY_EDITING)
        pub.subscribe(self.RemoveCommodities, EVENTS.COMMODITY_REMOVING)
        
        pub.subscribe(self.AddProcess, EVENTS.PROCESS_ADDING)
        pub.subscribe(self.EditProcess, EVENTS.PROCESS_EDITING)
        pub.subscribe(self.RemoveProcesses, EVENTS.PROCESS_REMOVING)

        
    def AddYear(self, year):
        self._model.AddYear(year)
    
    def RemoveYears(self, years):
        self._model.RemoveYears(years)
        
    def AddSite(self, site):
        self._model.AddSite(site)
    
    def RemoveSites(self, sites):
        self._model.RemoveSites(sites)
        
    def AddCommodity(self, commType):
        self._model.AddCommodity(commType)
        
    def EditCommodity(self, commId):
        comm = self._model.GetCommodity(commId)
        comForm = cf.CommodityDialog(self._view)
        comForm.PopulateCommodityGrid(comm)
        comForm.ShowModal()
    
    def RemoveCommodities(self, commodities):
        self._model.RemoveCommodities(commodities)
        
    def AddProcess(self, processName):
        self._model.AddProcess(processName)
        
    def EditProcess(self, processId):
        process = self._model.GetProcess(processId)
        processForm = pf.ProcessDialog(self._view)
        processForm.PopulateProcessGrid(process)
        processForm.ShowModal()
    
    def RemoveProcesses(self, processes):
        self._model.RemoveProcesses(processes)