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
import StorageForm as strgf
import wx

from pubsub import pub
from Events import EVENTS

class Controller():
    
    def __init__(self):
        
        #Model part
        self._resModel = model.RESModel()
        self._model = None
        
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
        pub.subscribe(self.SaveCommodity, EVENTS.COMMODITY_SAVE)
        #pub.subscribe(self.SelectCommodity, EVENTS.COMMODITY_SELECTED)
        #pub.subscribe(self.DeselectCommodity, EVENTS.COMMODITY_DESELECTED)
        
        pub.subscribe(self.AddProcess, EVENTS.PROCESS_ADDING)
        pub.subscribe(self.EditProcess, EVENTS.PROCESS_EDITING)
        pub.subscribe(self.SaveProcess, EVENTS.PROCESS_SAVE)
        #pub.subscribe(self.SelectProcess, EVENTS.PROCESS_SELECTED)
        #pub.subscribe(self.DeselectProcess, EVENTS.PROCESS_DESELECTED)
        
        pub.subscribe(self.AddStorage, EVENTS.STORAGE_ADDING)
        pub.subscribe(self.EditStorage, EVENTS.STORAGE_EDITING)
        pub.subscribe(self.SaveStorage, EVENTS.STORAGE_SAVE)
        
        pub.subscribe(self.EditConnection, EVENTS.CONNECTION_EDITING)
        
        pub.subscribe(self.RESSelected, EVENTS.RES_SELECTED)
        pub.subscribe(self.OnItemDoubleClick, EVENTS.ITEM_DOUBLE_CLICK)
        pub.subscribe(self.OnItemMove, EVENTS.ITEM_MOVED)

    
    def AddSite(self, site):
        status = self._resModel.AddSite(site)
        if status == 1:
            wx.MessageBox('A Site with the same name already exist!', 'Error', wx.OK|wx.ICON_ERROR)
        else:
            self._view.AddRESTab(self, site)            
    
    def RemoveSites(self, sites):
        s = wx.MessageBox('Are you sure? All site(s) data will be lost!', 'Warning', wx.OK|wx.CANCEL|wx.ICON_WARNING)
        if s == wx.OK:
            self._resModel.RemoveSites(sites)
            self._view.RemoveRESTab(sites)
            
    def RESSelected(self, siteName):    
        self._model = self._resModel.GetSiteModel(siteName)
        
    def AddYear(self, year):
        self._resModel.AddYear(year)
    
    def RemoveYears(self, years):
        s = wx.MessageBox('Are you sure? All year(s) data will be lost!', 'Warning', wx.OK|wx.CANCEL|wx.ICON_WARNING)
        if s == wx.OK:
            self._resModel.RemoveYears(years)
        
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
        
    def AddStorage(self):
        newStorage = self._model.CreateNewStorage()        
        self._storageForm = strgf.StorageDialog(self._view)
        self._storageForm.PopulateStorage(newStorage, self._model.GetCommodityList())
        self._storageForm.ShowModal()
    
    def SaveStorage(self, data):
        status = self._model.SaveProcess(data)#storage is a process
        if status == 1:
            wx.MessageBox('A storage with the same name already exist!', 'Error', wx.OK|wx.ICON_ERROR)
        elif status == 2:
            wx.MessageBox('Please select a commodity!', 'Error', wx.OK|wx.ICON_ERROR)
        else:
            self._storageForm.Close()            
            
        
    def EditStorage(self, storageId):
        storage = self._model.GetStorage(storageId)
        self._storageForm = strgf.StorageDialog(self._view)
        self._storageForm.PopulateStorage(storage, self._model.GetCommodityList())
        self._storageForm.ShowModal()
        
    def EditConnection(self, procId, commId, In_Out):
        connection = self._model.GetConnection(procId, commId, In_Out)
        connForm = connf.ConnectionDialog(self._view)
        connForm.PopulateConnectionGrid(connection)
        connForm.ShowModal()
        
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
        
    def OnItemDoubleClick(self, itemId, itemType):
        if itemType == 'Commodity':
            self.EditCommodity(itemId)
        elif itemType == 'Process':
            self.EditProcess(itemId)
        elif itemType == 'Storage':
            self.EditStorage(itemId)
            
    def OnItemMove(self, item):
        pub.sendMessage(EVENTS.ITEM_MOVED + self._model.GetSiteName(), item=item)
        