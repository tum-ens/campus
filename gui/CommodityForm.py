# -*- coding: utf-8 -*-
"""
Created on Wed Oct 31 02:56:46 2018

@author: aelshaha
"""

import wx
import wx.grid
import collections


class CommodityDialog ( wx.Dialog ):
    
    _gridCols = ['Commodity price (Euro/MWh)', 'Maximum commodity use', 'Maximum commodity use per step']
    
    def __init__(self, parent):
        wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = "Commodity data", size= wx.Size(800, 500))
        self.SetBackgroundColour("black")
        
        mainLayout = wx.StaticBoxSizer( wx.StaticBox(self, wx.ID_ANY, u"" ), wx.VERTICAL )
  
        self._yearsGrid = wx.grid.Grid(mainLayout.GetStaticBox(), -1)
        self._yearsGrid.CreateGrid(0, len(self._gridCols))
        for i in range(0, len(self._gridCols)):
            self._yearsGrid.SetColSize(i, 200)
            self._yearsGrid.SetColLabelValue(i, self._gridCols[i])

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
        i = self._yearsGrid.GetNumberRows()
        if i > 0:
            self._yearsGrid.DeleteRows(0, i)
            i = 0
            
        dataPerYear = collections.OrderedDict(sorted(dataPerYear.items()))
        for year, data in dataPerYear.items():
            self._yearsGrid.InsertRows(i, 1)
            self._yearsGrid.SetRowLabelValue(i, year)
            self._yearsGrid.SetCellValue(i, 0, data['price'])
            self._yearsGrid.SetCellValue(i, 1, data['max'])
            self._yearsGrid.SetCellValue(i, 2, data['maxPerHour'])
            i += 1      
    
    def __del__( self ):
        pass
        