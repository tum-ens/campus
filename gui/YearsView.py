# -*- coding: utf-8 -*-
"""
Created on Wed Oct 31 15:43:07 2018

@author: aelshaha
"""

import wx
import wx.grid
import collections

from Events import EVENTS
from pubsub import pub

class YearsView():
    
    _gridCols = ['', 'Discount rate', 'CO2 limit', 'CO2 budget']

    def __init__(self, parent):
        
        #manage layout
        headerBox = wx.StaticBox(parent, wx.ID_ANY, u"Manage Years:" )
        headerBox.SetForegroundColour('white')
        
        self._mainLayout = wx.StaticBoxSizer(headerBox , wx.HORIZONTAL )
        yearsLayout = wx.BoxSizer( wx.VERTICAL )
        #imgLayout = wx.BoxSizer( wx.VERTICAL )
        
        self._mainLayout.Add(yearsLayout, 0, wx.ALL|wx.EXPAND, 5 )
        #mainLayout.Add(imgLayout, 1, wx.EXPAND|wx.ALIGN_CENTER, 5 )
        
        #Add year section        
        addYearLayout = wx.StaticBoxSizer( wx.StaticBox(parent, wx.ID_ANY, u"" ), wx.HORIZONTAL )
        #label = wx.StaticText(addYearLayout.GetStaticBox(), -1, "Year:")
        #addYearLayout.Add(label, 0, wx.ALL, 5)
        
        self._txtYear = wx.TextCtrl(addYearLayout.GetStaticBox())
        self._txtYear.SetMaxLength(4.0)        
        self._txtYear.Bind(wx.EVT_CHAR, self.TxtYearOnKeyPress)
        self._txtYear.Bind(wx.EVT_TEXT, self.TxtYearOnTextChange)
        addYearLayout.Add(self._txtYear, 0, wx.ALL, 5)
        
        self._btnAdd = wx.Button(addYearLayout.GetStaticBox(), label="Add Year")
        self._btnAdd.Bind(wx.EVT_BUTTON, self.BtnAddOnClick) 
        self._btnAdd.Disable()
        addYearLayout.Add(self._btnAdd, 0, wx.ALL, 5)
        
        self._btnRemove = wx.Button(addYearLayout.GetStaticBox(), label="Remove Selected Year(s)")
        self._btnRemove.Bind(wx.EVT_BUTTON, self.BtnRemoveOnClick)
        #self._btnRemove.Disable()
        addYearLayout.Add(self._btnRemove, 0, wx.ALL, 5 )
        
        yearsLayout.Add(addYearLayout, 0, wx.ALL|wx.EXPAND, 5)
        
        #Grid of 4 cols
        self._yearsGrid = wx.grid.Grid(parent, -1)
        self._yearsGrid.CreateGrid(0, 4)
        #col1 as checkbox
        attr = wx.grid.GridCellAttr()
        attr.SetEditor(wx.grid.GridCellBoolEditor())
        attr.SetRenderer(wx.grid.GridCellBoolRenderer())        
        #col2-4
        for i in range(0, len(self._gridCols)):
            self._yearsGrid.SetColSize(i, 120)
            self._yearsGrid.SetColLabelValue(i, self._gridCols[i])
        self._yearsGrid.SetColAttr(0, attr)
        self._yearsGrid.SetColSize(0, 20)
        #self._listOfYrs.Bind( wx.EVT_LIST_ITEM_SELECTED, self.ListOfYearsOnSelectionChange)
        #self._listOfYrs.Bind( wx.EVT_LIST_ITEM_DESELECTED, self.ListOfYearsOnSelectionChange)
                
        yearsLayout.Add(self._yearsGrid, 1, wx.ALL|wx.EXPAND, 5)
        
        #bitmap = wx.StaticBitmap( self, wx.ID_ANY, wx.Bitmap( u"Energy.jpeg", wx.BITMAP_TYPE_ANY ))
        #imgLayout.Add(bitmap, 1, wx.EXPAND, 5)          
        
        pub.subscribe(self.PopulateYearsGrid, EVENTS.YEAR_ADDED)
        pub.subscribe(self.PopulateYearsGrid, EVENTS.YEAR_REMOVED)
        
    def GetLayout(self):
        return self._mainLayout;
                
        
    def TxtYearOnKeyPress(self, event):
        acceptable_characters = "1234567890\b" #include backspace        
        key = event.GetKeyCode()
        
        if chr(key) in acceptable_characters: 
            txt = event.GetEventObject().GetValue()
            if len(txt) == 0 and chr(key) == '0':
                return False
                
            event.Skip()
            return
        else:
            return False
    
    def TxtYearOnTextChange(self, event):
        txt = event.GetEventObject().GetValue()
        if len(txt) == 4:
            self._btnAdd.Enable()
        else:
            self._btnAdd.Disable()
        
        
    def BtnAddOnClick(self, event):
        newYear = self._txtYear.GetValue()
        pub.sendMessage(EVENTS.YEAR_ADDING, year=newYear)        
            
    def BtnRemoveOnClick(self, event):
        rows = self._yearsGrid.GetNumberRows()
        if rows == 0:
            return
        
        yrsToRmv = []
        for i in range(0, rows):
            val = self._yearsGrid.GetCellValue(i, 0)
            if val:
                yrsToRmv.append(self._yearsGrid.GetRowLabelValue(i))
        
        pub.sendMessage(EVENTS.YEAR_REMOVING, years=yrsToRmv)
        
    def PopulateYearsGrid(self, years):       
        i = self._yearsGrid.GetNumberRows()
        if i > 0:
            self._yearsGrid.DeleteRows(0, i)
            i = 0
            
        years = collections.OrderedDict(sorted(years.items()))
        for year, data in years.items():
            self._yearsGrid.InsertRows(i, 1)
            self._yearsGrid.SetRowLabelValue(i, year)
            #self._yearsGrid.SetCellValue(i, 0, bool(data['selected']))
            self._yearsGrid.SetCellValue(i, 1, data['discountRate'])
            self._yearsGrid.SetCellValue(i, 2, data['co2Limit'])
            self._yearsGrid.SetCellValue(i, 3, data['co2Budet'])
            i += 1