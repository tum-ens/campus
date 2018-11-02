# -*- coding: utf-8 -*-
"""
Created on Wed Oct 31 02:56:46 2018

@author: aelshaha
"""

import wx
import wx.grid
import collections


class ProcessDialog ( wx.Dialog ):
    
    _grid1Cols = {'instCap': 'Installed capacity (MW)',
                    'lifetime': 'Lifetime of inst-cap (years)',
                    'capLo': 'Minimum capacity (MW)',
                    'capUp': 'Maximum capacity (MW)',
                    'invCost': 'Investment cost (Euro/MW)',
                    'fixCost': 'Annual fix cost (Euro/MW/a)',
                    'varCost': 'Variable costs (Euro/MWh)',
                    'startupCost': 'Startup cost (Euro)',
                    'wacc': 'Weighted average cost of capital'} 

    _grid2Cols = {'maxGrad': 'Maximum power gradient (1/h)',
                'minFraction': 'Minimum load fraction',
                'depreciation': 'Depreciation period (a)',
                'areaPerCap': 'Area use per capacity (m^2/MW)'}
    
    def __init__(self, parent):
        wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = "Process data", size= wx.Size(800, 600))
        self.SetBackgroundColour("black")
        
        mainLayout = wx.BoxSizer( wx.VERTICAL )
        
        h1 = wx.StaticBox(self, wx.ID_ANY, u"Economical parameters:" )
        h1.SetForegroundColour('white')
        layout1 = wx.StaticBoxSizer(h1, wx.VERTICAL )
        self._yearsGrid1 = wx.grid.Grid(h1, -1)
        self._yearsGrid1.CreateGrid(0, len(self._grid1Cols))
        for i, item in enumerate(self._grid1Cols.items()):
            self._yearsGrid1.SetColSize(i, 200)
            self._yearsGrid1.SetColLabelValue(i, item[1])
        layout1.Add(self._yearsGrid1, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5)            
        
        h2 = wx.StaticBox(self, wx.ID_ANY, u"Technical parameters:" )
        h2.SetForegroundColour('white')
        layout2 = wx.StaticBoxSizer(h2, wx.VERTICAL )
        self._yearsGrid2 = wx.grid.Grid(h2, -1)
        self._yearsGrid2.CreateGrid(0, len(self._grid2Cols))
        for i, item in enumerate(self._grid2Cols.items()):
            self._yearsGrid2.SetColSize(i, 200)
            self._yearsGrid2.SetColLabelValue(i, item[1])
        layout2.Add(self._yearsGrid2, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5)

        mainLayout.Add(layout1, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5)
        mainLayout.Add(layout2, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5)
        
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
        self.PopulateGrid(self._yearsGrid1, self._grid1Cols.keys(), dataPerYear)
        self.PopulateGrid(self._yearsGrid2, self._grid2Cols.keys(), dataPerYear)
        
    def PopulateGrid(self, grid, cols, dataPerYear):
        i = grid.GetNumberRows()
        if i > 0:
            grid.DeleteRows(0, i)
            i = 0
            
        dataPerYear = collections.OrderedDict(sorted(dataPerYear.items()))
        for year, data in dataPerYear.items():
            grid.InsertRows(i, 1)
            grid.SetRowLabelValue(i, year)
            for j, key in enumerate(cols):
                grid.SetCellValue(i, j, data[key])            
            i += 1      
    
    def __del__( self ):
        pass
        