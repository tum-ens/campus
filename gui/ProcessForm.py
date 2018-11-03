# -*- coding: utf-8 -*-
"""
Created on Wed Oct 31 02:56:46 2018

@author: aelshaha
"""

import wx
import wx.grid
import DataConfig as config
import GridDataTable as gdt


class ProcessDialog ( wx.Dialog ):
    
    _grid1Cols = config.DataConfig.PROCESS_ECO_PARAMS

    _grid2Cols = config.DataConfig.PROCESS_TECH_PARAMS
    
    def __init__(self, parent):
        wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = "Process data", size= wx.Size(800, 600))
        self.SetBackgroundColour("black")
        
        mainLayout = wx.BoxSizer( wx.VERTICAL )
        
        h1 = wx.StaticBox(self, wx.ID_ANY, u"Economical parameters:" )
        h1.SetForegroundColour('white')
        layout1 = wx.StaticBoxSizer(h1, wx.VERTICAL )
        #Grid and its data table
        self._gridTable1 = gdt.GridDataTable(self._grid1Cols)
        self._yearsGrid1 = wx.grid.Grid(h1, -1)
        self._yearsGrid1.SetTable(self._gridTable1, True)
        self._yearsGrid1.AutoSizeColumns(False)
        layout1.Add(self._yearsGrid1, 1, wx.ALL, 5)            
        
        h2 = wx.StaticBox(self, wx.ID_ANY, u"Technical parameters:" )
        h2.SetForegroundColour('white')
        layout2 = wx.StaticBoxSizer(h2, wx.VERTICAL )
        #Grid and its data table
        self._gridTable2 = gdt.GridDataTable(self._grid2Cols)
        self._yearsGrid2 = wx.grid.Grid(h2, -1)
        self._yearsGrid2.SetTable(self._gridTable2, True)
        self._yearsGrid2.AutoSizeColumns(False)
        layout2.Add(self._yearsGrid2, 1, wx.ALL|wx.EXPAND, 5)

        mainLayout.Add(layout1, 1, wx.ALL, 5)
        mainLayout.Add(layout2, 1, wx.ALL|wx.EXPAND, 5)
        
        btnsLayout = wx.BoxSizer( wx.HORIZONTAL )
        btnOk = wx.Button(self, label="Ok")
        btnCancel = wx.Button(self, label="Cancel")
        btnFillAll = wx.Button(self, label="Fill all as first year")
        btnsLayout.Add(btnOk, 0, wx.ALL, 5)
        btnsLayout.Add(btnCancel, 0, wx.ALL, 5)
        btnsLayout.Add(btnFillAll, 0, wx.ALL, 5)        
        mainLayout.Add(btnsLayout, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5)
        
        self.SetSizer( mainLayout )
        self.Layout()
        #mainLayout.Fit(self)    
        self.Centre( wx.BOTH )
        
    def PopulateProcessGrid(self, dataPerYear):
        self.PopulateGrid(self._gridTable1, dataPerYear)
        self.PopulateGrid(self._gridTable2, dataPerYear)
        
    def PopulateGrid(self, gridTable, dataPerYear):
        new = len(dataPerYear)
        cur = gridTable.GetNumberRows()        
        msg = None
        if new > cur:#new rows
            msg = wx.grid.GridTableMessage(gridTable, wx.grid.GRIDTABLE_NOTIFY_ROWS_APPENDED, new-cur)
        elif new < cur: #rows removed
            msg = wx.grid.GridTableMessage(gridTable, wx.grid.GRIDTABLE_NOTIFY_ROWS_DELETED, new, cur-new)
        
        if msg:
            gridTable.SetTableData(dataPerYear)
            gridTable.GetView().ProcessTableMessage(msg)