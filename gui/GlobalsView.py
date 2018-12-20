# -*- coding: utf-8 -*-
"""
Created on Sat Dec  8 23:59:15 2018

@author: aelshaha
"""

import wx
import wx.grid
import DataConfig as config
import GridDataTable as gdt

from Events import EVENTS
from pubsub import pub

class GlobalsView():
    
    _gridCols = config.DataConfig.GLOBAL_COLS
    _gridRows = config.DataConfig.GLOBAL_PARAMS
    
    def __init__(self, parent, controller):
        self._controller = controller
        
        #manage layout
        headerBox = wx.StaticBox(parent, wx.ID_ANY, u"Global Parameters:" )
        headerBox.SetForegroundColour('white')
        
        self._mainLayout = wx.StaticBoxSizer(headerBox , wx.VERTICAL )
        
        gridLayout = wx.BoxSizer( wx.HORIZONTAL )
        #Grid and its data table
        self._gridTable = gdt.GridDataTable(self._gridCols, self._gridRows, autoCommit=True)
        self._gridTable.SetTableData(controller.GetGlobalParams())
        self._glGrid = wx.grid.Grid(parent, -1)
        self._glGrid.SetTable(self._gridTable, True)
        self._glGrid.SetColSize(0, 120)
        self._glGrid.SetRowLabelSize(150)
        self._glGrid.SetRowLabelAlignment(wx.ALIGN_LEFT, wx.ALIGN_CENTER)
        gridLayout.Add(self._glGrid, 1, wx.ALL|wx.EXPAND, 5)
        
        self._lb = wx.CheckListBox(parent, -1, choices=controller.GetScenarios())
        self._lb.Bind(wx.EVT_CHECKLISTBOX, self.OnScenarioChange)
        gridLayout.Add(self._lb, 1, wx.ALL|wx.EXPAND, 5)
        
        imgLayout = wx.BoxSizer( wx.HORIZONTAL )
        bitmap = wx.Bitmap( u"./imgs/Play.png", wx.BITMAP_TYPE_ANY )
        btnRun = wx.BitmapButton(parent, wx.ID_ANY, bitmap, wx.DefaultPosition, (132, 132), wx.BU_AUTODRAW|wx.RAISED_BORDER)
        btnRun.Bind(wx.EVT_BUTTON, self.OnRunClick)
        imgLayout.Add(btnRun, 0, wx.ALL|wx.ALIGN_CENTER, 5)
        
        bitmap = wx.Bitmap( u"./imgs/Abort.png", wx.BITMAP_TYPE_ANY )
        btnAbort = wx.BitmapButton(parent, wx.ID_ANY, bitmap, wx.DefaultPosition, (132, 132), wx.BU_AUTODRAW|wx.RAISED_BORDER)
        imgLayout.Add(btnAbort, 0, wx.ALL|wx.ALIGN_CENTER, 5)
        
        self._mainLayout.Add(gridLayout, 1, wx.ALL|wx.EXPAND, 5)
        self._mainLayout.Add(imgLayout, 1, wx.ALL|wx.ALIGN_CENTER, 5)
        
        pub.subscribe(self.PopulateGrid, EVENTS.GL_PARAMS_LOADED)
        pub.subscribe(self.PopulateScenarios, EVENTS.SCENARIOS_LOADED)
        
    def GetLayout(self):
        return self._mainLayout;

    def OnRunClick(self, event):
        self._controller.Run()
        
    def OnScenarioChange(self, event):
        index = event.GetSelection()
        lb = event.GetEventObject()
        label = lb.GetString(index)
        if lb.IsChecked(index):
            pub.sendMessage(EVENTS.SCENARIO_ADDED, scName=label)
        else:
            pub.sendMessage(EVENTS.SCENARIO_REMOVED, scName=label)
        
    def PopulateGrid(self, gl):
        self._gridTable.SetTableData(gl)
        msg = wx.grid.GridTableMessage(self._gridTable,
                                       wx.grid.GRIDTABLE_REQUEST_VIEW_GET_VALUES)
        self._gridTable.GetView().ProcessTableMessage(msg)
        
    def PopulateScenarios(self, scenarios):
        self._lb.SetCheckedStrings(scenarios)
        