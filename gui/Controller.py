# -*- coding: utf-8 -*-
"""
Created on Wed Oct 31 11:35:21 2018

@author: aelshaha
"""
import Model as model
import MainView as view
import CommodityForm as commf
import ProcessForm as procf
import ConnectionForm as connf

from pubsub import pub
from Events import EVENTS

class Controller():
    
    _selectedCommodity = None
    _selectedProcess   = None
    
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
        #pub.subscribe(self.RemoveCommodities, EVENTS.COMMODITY_REMOVING)
        pub.subscribe(self.SelectCommodity, EVENTS.COMMODITY_SELECTED)
        pub.subscribe(self.DeselectCommodity, EVENTS.COMMODITY_DESELECTED)
        
        pub.subscribe(self.AddProcess, EVENTS.PROCESS_ADDING)
        pub.subscribe(self.EditProcess, EVENTS.PROCESS_EDITING)
        pub.subscribe(self.SelectProcess, EVENTS.PROCESS_SELECTED)
        pub.subscribe(self.DeselectProcess, EVENTS.PROCESS_DESELECTED)
        
        pub.subscribe(self.EditConnection, EVENTS.CONNECTION_EDITING)

        
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
        comForm = commf.CommodityDialog(self._view)
        comForm.PopulateCommodityGrid(comm)
        comForm.ShowModal()
    
    def RemoveCommodities(self, commodities):
        self._model.RemoveCommodities(commodities)
        
    def AddProcess(self, processName):
        self._model.AddProcess(processName)
        
    def EditProcess(self, processId):
        process = self._model.GetProcess(processId)
        processForm = procf.ProcessDialog(self._view)
        processForm.PopulateProcessGrid(process)
        processForm.ShowModal()
    
    def RemoveProcesses(self, processes):
        self._model.RemoveProcesses(processes)
        
    def SelectCommodity(self, commId):
        self._selectedCommodity = commId
        if self._selectedProcess:
            #Add a connection
            self._model.AddOutboundConnection(self._selectedProcess, self._selectedCommodity)
            self._selectedCommodity = self._selectedProcess = None
    
    def DeselectCommodity(self, commId):
        #Assert if diff Ids
        self._selectedCommodity = None
        
    def SelectProcess(self, processId):
        self._selectedProcess = processId
        if self._selectedCommodity:
            #Add a connection
            self._model.AddInboundConnection(self._selectedCommodity, self._selectedProcess)
            self._selectedCommodity = self._selectedProcess = None
    
    def DeselectProcess(self, processId):
        #Assert if diff Ids
        self._selectedProcess = None
        
    def EditConnection(self, connId):
        connection = self._model.GetConnection(connId)
        connForm = connf.ConnectionDialog(self._view)
        connForm.PopulateConnectionGrid(connection)
        connForm.ShowModal()