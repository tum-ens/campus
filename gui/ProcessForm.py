# -*- coding: utf-8 -*-
"""
Created on Wed Oct 31 02:56:46 2018

@author: aelshaha
"""

import wx
import wx.grid
import DataConfig as config
import GridDataTable as gdt
import BasicForm as bf


class ProcessDialog ( bf.BasicForm ):
    
    _grid1Cols = config.DataConfig.PROCESS_ECO_PARAMS

    _grid2Cols = config.DataConfig.PROCESS_TECH_PARAMS
    
    def __init__(self, parent):
        super().__init__(parent, "Process data", wx.Size(800, 600))
        contentLayout = wx.BoxSizer( wx.VERTICAL )
        
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

        contentLayout.Add(layout1, 1, wx.ALL, 5)
        contentLayout.Add(layout2, 1, wx.ALL|wx.EXPAND, 5)
        super().SetContent(contentLayout, wx.ALIGN_CENTER_HORIZONTAL)        
        
    def PopulateProcessGrid(self, dataPerYear):
        super().PopulateGrid(self._gridTable1, dataPerYear)
        super().PopulateGrid(self._gridTable2, dataPerYear)
        