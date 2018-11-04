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

class CommodityDialog ( bf.BasicForm ):
    
    _gridCols = config.DataConfig.COMMODITY_PARAMS
    
    def __init__(self, parent):
        super().__init__(parent, "Commodity data", wx.Size(700, 400))
  
        self._gridTable = gdt.GridDataTable(self._gridCols)
        self._yearsGrid = wx.grid.Grid(self)
        self._yearsGrid.SetTable(self._gridTable, True)
        self._yearsGrid.AutoSizeColumns(False)
        super().SetContent(self._yearsGrid, wx.ALIGN_CENTER_HORIZONTAL)
        
    def PopulateCommodityGrid(self, dataPerYear): 
        super().PopulateGrid(self._gridTable, dataPerYear)
