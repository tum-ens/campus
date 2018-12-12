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
import TransmissionForm as tf
import pandas as pd
import json
import wx

from pubsub import pub
from Events import EVENTS

import sys
sys.path.insert(0, '..')
import urbs

class Controller():
    
    def __init__(self):
        
        #Model part
        self._resModel = model.RESModel()
        self._model = None
        
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
        
        pub.subscribe(self.AddStorage, EVENTS.STORAGE_ADDING)
        pub.subscribe(self.EditStorage, EVENTS.STORAGE_EDITING)
        pub.subscribe(self.SaveStorage, EVENTS.STORAGE_SAVE)
        
        pub.subscribe(self.EditConnection, EVENTS.CONNECTION_EDITING)
        
        pub.subscribe(self.AddTransmission, EVENTS.TRNSM_ADDING)
        pub.subscribe(self.SaveTransmission, EVENTS.TRNSM_SAVE)
        
        pub.subscribe(self.RESSelected, EVENTS.RES_SELECTED)
        pub.subscribe(self.OnItemDoubleClick, EVENTS.ITEM_DOUBLE_CLICK)
        pub.subscribe(self.OnItemMove, EVENTS.ITEM_MOVED)
        pub.subscribe(self.OnSaveConfig, EVENTS.SAVE_CONFIG)
        pub.subscribe(self.OnLoadConfig, EVENTS.LOAD_CONFIG)

    
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
        if comm:
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
        
    def AddTransmission(self):
        newTrns = self._resModel.CreateNewTrnsm()
        self._trnsForm = tf.TransmissionDialog(self._view, self)
        self._trnsForm.PopulateTrans(newTrns, self._resModel.GetSites())
        self._trnsForm.ShowModal()
        
    def SaveTransmission(self, data):
        status = self._resModel.SaveTransmission(data)
        if status:
            self._trnsForm.Close()
        else:
            wx.MessageBox('A Transmission line with the same name already exist!', 'Error', wx.OK|wx.ICON_ERROR)
            
    def EditTransmission(self, trnsmId):
        trnsm = self._resModel.GetTransmission(trnsmId)
        self._trnsForm = tf.TransmissionDialog(self._view, self)
        self._trnsForm.PopulateTrans(trnsm, self._resModel.GetSites())
        self._trnsForm.ShowModal()
            
    def GetTransmissions(self):
        return self._resModel._transmissions
        
    def GetTrnsmCommodities(self):
        return self._resModel._trnsmCommodities
        
    def GetCommonCommodities(self, site1, site2):
        m1 = self._resModel.GetSiteModel(site1)
        m2 = self._resModel.GetSiteModel(site2)
        
        c1 = set([x['Name'] for x in m1._commodities.values()])
        c2 = set([x['Name'] for x in m2._commodities.values()])
        
        l = c1 & c2
        return list(l)
        
    def OnItemDoubleClick(self, itemId, itemType):
        if itemType == 'Commodity':
            self.EditCommodity(itemId)
        elif itemType == 'Process':
            self.EditProcess(itemId)
        elif itemType == 'Storage':
            self.EditStorage(itemId)
        elif itemType == 'Trnsm':
            self.EditTransmission(itemId)
            
    def OnItemMove(self, item):
        if item.GetType() == 'Trnsm':
            pub.sendMessage(EVENTS.TRNSM_ITEM_MOVED, item=item)
        else:
            pub.sendMessage(EVENTS.ITEM_MOVED + self._model.GetSiteName(), item=item)

    def SerializeObj(self, obj):
        #print(obj)
        if isinstance(obj, wx.Colour):
            return obj.GetAsString()
        
        return obj.__dict__
    
    def OnSaveConfig(self, filename):
        with open(filename, 'w') as fp:
            json.dump(self._resModel, fp, default=self.SerializeObj, indent=2)
    
    def OnLoadConfig(self, filename):
        self._view.RemoveRESTab(self._resModel._sites)
        with open(filename, 'r') as fp:
            data = json.load(fp)
            self._resModel = model.RESModel(data)
            for site in sorted(self._resModel._sites):
                resTab = self._view.AddRESTab(self, site)
                self._model = self._resModel.GetSiteModel(site)
                resTab.RebuildRES(None)
                resTab.Refresh()
    
    def GetGlobalParams(self):
        return self._resModel.GetGlobalParams()
        
    def Run(self):
        #self.GetDataFrames()
        #return
        result_name = 'Campus'
        result_dir = urbs.prepare_result_directory(result_name) # name + time stamp
    
        # copy input file to result directory
        # shutil.copyfile(input_file, os.path.join(result_dir, input_file))
        # copy runme.py to result directory
        # shutil.copyfile(__file__, os.path.join(result_dir, __file__))
    
        # Choose Solver (cplex, glpk, gurobi, ...)
        #Solver = 'gurobi'
        Solver = self._resModel.GetSolver()
    
        # simulation timesteps
        (offset, length) = self._resModel.GetTimeStepTuple()  # time step selection
        #print((offset, length))
        timesteps = range(offset, offset+length+1)
        dt=self._resModel.GetDT()
        #print(dt)
    
        # plotting commodities/sites
        plot_tuples = [
            (2015, 'Campus', 'Elec'),
            (2015, 'Campus', 'Heat'),
            (2015, 'Campus', 'Cold'),
            (2015, 'Campus', 'Heat low'),
            (2020, 'Campus', 'Elec'),
            (2020, 'Campus', 'Heat'),
            (2020, 'Campus', 'Cold'),
            (2020, 'Campus', 'Heat low'),
            (2025, 'Campus', 'Elec'),
            (2025, 'Campus', 'Heat'),
            (2025, 'Campus', 'Cold'),
            (2025, 'Campus', 'Heat low'),
            (2030, 'Campus', 'Elec'),
            (2030, 'Campus', 'Heat'),
            (2030, 'Campus', 'Cold'),
            (2030, 'Campus', 'Heat low'),
            (2035, 'Campus', 'Elec'),
            (2035, 'Campus', 'Heat'),
            (2035, 'Campus', 'Cold'),
            (2035, 'Campus', 'Heat low'),
            (2040, 'Campus', 'Elec'),
            (2040, 'Campus', 'Heat'),
            (2040, 'Campus', 'Cold'),
            (2040, 'Campus', 'Heat low')
            ]
    
        # optional: define names for sites in plot_tuples
        plot_sites_name = {}
    
        # detailed reporting commodity/sites
        report_tuples = [
            (2015, 'Campus', 'Elec'),
            (2015, 'Campus', 'Heat'),
            (2015, 'Campus', 'Cold'),
            (2015, 'Campus', 'Heat low'),
            (2015, 'Campus', 'CO2'),
            (2020, 'Campus', 'Elec'),
            (2020, 'Campus', 'Heat'),
            (2020, 'Campus', 'Cold'),
            (2020, 'Campus', 'CO2'),
            (2020, 'Campus', 'Heat low'),
            (2025, 'Campus', 'Elec'),
            (2025, 'Campus', 'Heat'),
            (2025, 'Campus', 'Cold'),
            (2025, 'Campus', 'Heat low'),
            (2025, 'Campus', 'CO2'),
            (2030, 'Campus', 'Elec'),
            (2030, 'Campus', 'Heat'),
            (2030, 'Campus', 'Cold'),
            (2030, 'Campus', 'Heat low'),
            (2030, 'Campus', 'CO2'),
            (2035, 'Campus', 'Elec'),
            (2035, 'Campus', 'Heat'),
            (2035, 'Campus', 'Cold'),
            (2035, 'Campus', 'Heat low'),
            (2035, 'Campus', 'CO2'),
            (2040, 'Campus', 'Elec'),
            (2040, 'Campus', 'Heat'),
            (2040, 'Campus', 'Cold'),
            (2040, 'Campus', 'Heat low'),
            (2040, 'Campus', 'CO2'),
            ]
    
        # optional: define names for sites in report_tuples
        report_sites_name = {}
    
        # plotting timesteps
        plot_periods = {
            'win': range(1000, 1000+24*7),
            # 'spr': range(3000, 3000+24*7),
            # 'sum': range(5000, 5000+24*7),
            # 'win': range(7000, 7000+24*7)
        }
    
        # add or change plot colors
        my_colors = {
            'South': (230, 200, 200),
            'Mid': (200, 230, 200),
            'North': (200, 200, 230)}
        for country, color in my_colors.items():
            urbs.COLORS[country] = color
    
        # select scenarios to be run
        scenarios = [
                     urbs.scenario_base,
                     # urbs.sc_CO2limit(40000),
                     # urbs.sc_1proprop('Campus', 'PV S 30°', 'inv-cost', 600000)
        ]
    
        #print(scenarios)
        for scenario in scenarios:
            #print(scenario)
            prob = urbs.run_scenario(self._resModel.GetDataFrames(), Solver, timesteps, scenario,
                                result_dir, dt,
                                plot_tuples=plot_tuples,
                                plot_sites_name=plot_sites_name,
                                plot_periods=plot_periods,
                                report_tuples=report_tuples,
                                report_sites_name=report_sites_name)
    
