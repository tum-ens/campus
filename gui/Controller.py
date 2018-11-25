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
import wx

from pubsub import pub
from Events import EVENTS

class Controller():
    
    _selectedCommodity = None
    _selectedProcess   = None
    
    def __init__(self):
        #Model part
        self._model = model.Model()
        
        #view part
        self._view = view.MainView(self)
        self._view.Maximize()
        self._view.Show()
        
        #subscribe on Views events
        pub.subscribe(self.AddYear, EVENTS.YEAR_ADDING)
        pub.subscribe(self.RemoveYears, EVENTS.YEAR_REMOVING)
        
        pub.subscribe(self.AddSite, EVENTS.SITE_ADDING)
        pub.subscribe(self.RemoveSites, EVENTS.SITE_REMOVING)
        
        pub.subscribe(self.AddCommodity, EVENTS.COMMODITY_ADDING)
        pub.subscribe(self.EditCommodity, EVENTS.COMMODITY_EDITING)
        pub.subscribe(self.SaveCommodity, EVENTS.COMMODITY_SAVE)
        #pub.subscribe(self.SelectCommodity, EVENTS.COMMODITY_SELECTED)
        #pub.subscribe(self.DeselectCommodity, EVENTS.COMMODITY_DESELECTED)
        
        pub.subscribe(self.AddProcess, EVENTS.PROCESS_ADDING)
        pub.subscribe(self.EditProcess, EVENTS.PROCESS_EDITING)
        pub.subscribe(self.SaveProcess, EVENTS.PROCESS_SAVE)
        #pub.subscribe(self.SelectProcess, EVENTS.PROCESS_SELECTED)
        #pub.subscribe(self.DeselectProcess, EVENTS.PROCESS_DESELECTED)
        
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
        comm = self._model.CreateNewCommodity(commType)        
        self._comForm = commf.CommodityDialog(self._view)
        self._comForm.PopulateCommodity(comm)
        self._comForm.ShowModal()
        
    def EditCommodity(self, commId):
        comm = self._model.GetCommodity(commId)
        self._comForm = commf.CommodityDialog(self._view)
        self._comForm.PopulateCommodity(comm)
        self._comForm.ShowModal()
        
    def SaveCommodity(self, data):
        status = self._model.SaveCommodity(data)
        if status:
            self._comForm.Close()
        else:
            wx.MessageBox('A Commodity with the same name already exist!', 'Error', wx.OK|wx.ICON_ERROR)
    
    def RemoveCommodities(self, commodities):
        self._model.RemoveCommodities(commodities)
        
    def AddProcess(self):
        newProcess = self._model.CreateNewProcess()        
        self._processForm = procf.ProcessDialog(self._view)
        self._processForm.PopulateProcess(newProcess, self._model.GetCommodityList())
        self._processForm.ShowModal()
    
    def SaveProcess(self, data):
        status = self._model.SaveProcess(data)
        if status == 1:
            wx.MessageBox('A process with the same name already exist!', 'Error', wx.OK|wx.ICON_ERROR)
        elif status == 2:
            wx.MessageBox('Please select atleast one input/output commodity!', 'Error', wx.OK|wx.ICON_ERROR)
        else:
            self._processForm.Close()            
            
        
    def EditProcess(self, processId):
        process = self._model.GetProcess(processId)
        self._processForm = procf.ProcessDialog(self._view)
        self._processForm.PopulateProcess(process, self._model.GetCommodityList())
        self._processForm.ShowModal()
    
    def RemoveProcesses(self, processes):
        self._model.RemoveProcesses(processes)        
        
    def EditConnection(self, procId, commId, In_Out):
        connection = self._model.GetConnection(procId, commId, In_Out)
        connForm = connf.ConnectionDialog(self._view)
        connForm.PopulateConnectionGrid(connection)
        connForm.ShowModal()
        
    def SelectCommodity(self, commId):
        self._selectedCommodity = commId
    
    def DeselectCommodity(self, commId):
        #Assert if diff Ids
        self._selectedCommodity = None
        
    def SelectProcess(self, processId):
        self._selectedProcess = processId
    
    def DeselectProcess(self, processId):
        #Assert if diff Ids
        self._selectedProcess = None            
        
    def GetCommodities(self):
        return self._model._commodities
    
    def GetProcesses(self):
        return self._model._processes
        
    def GetLinkedProcesses(self, commName):
        d = {}
        for k, p in self._model._processes.items():
            if len(p['IN']) > 0 and p['IN'][-1] == commName:
                d[k] = p

        for k, p in self._model._processes.items():
            if len(p['IN']) == 0 and len(p['OUT']) > 0 and p['OUT'][0] == commName:
                d[k] = p

                
        return d
        