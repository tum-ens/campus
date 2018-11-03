# -*- coding: utf-8 -*-
"""
Created on Wed Oct 31 02:56:46 2018

@author: aelshaha
"""

import wx
import wx.grid
import DataConfig as config
import GridDataTable as gdt

class CommodityDialog ( wx.Dialog ):
    
    _gridCols = config.DataConfig.COMMODITY_PARAMS
    
    def __init__(self, parent):
        wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = "Commodity data", size= wx.Size(700, 400))
        self.SetBackgroundColour("black")
        
        mainLayout = wx.StaticBoxSizer( wx.StaticBox(self, wx.ID_ANY, u"" ), wx.VERTICAL )
  
        self._gridTable = gdt.GridDataTable(self._gridCols)
        self._yearsGrid = wx.grid.Grid(mainLayout.GetStaticBox(), -1)
        self._yearsGrid.SetTable(self._gridTable, True)
        self._yearsGrid.AutoSizeColumns(False)
        mainLayout.Add(self._yearsGrid, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5)
        
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
        
    def PopulateCommodityGrid(self, dataPerYear): 
        new = len(dataPerYear)
        cur = self._gridTable.GetNumberRows()        
        msg = None
        if new > cur:#new rows
            msg = wx.grid.GridTableMessage(self._gridTable, wx.grid.GRIDTABLE_NOTIFY_ROWS_APPENDED, new-cur)
        elif new < cur: #rows removed
            msg = wx.grid.GridTableMessage(self._gridTable, wx.grid.GRIDTABLE_NOTIFY_ROWS_DELETED, new, cur-new)
        
        if msg:
            self._gridTable.SetTableData(dataPerYear)
            self._gridTable.GetView().ProcessTableMessage(msg)
