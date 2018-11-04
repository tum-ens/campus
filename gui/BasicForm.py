# -*- coding: utf-8 -*-
"""
Created on Sat Nov  3 20:50:45 2018

@author: aelshaha
"""

import wx

class BasicForm(wx.Dialog):
    
    _gridTables = []
    
    def __init__(self, parent, formTitle, formSize):
        wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = formTitle, size= formSize)
        self.SetBackgroundColour("black")
        
        mainLayout = wx.BoxSizer( wx.VERTICAL )
        self._contentLayout = wx.BoxSizer( wx.VERTICAL )
        mainLayout.Add(self._contentLayout, 1, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL, 5)
        
        btnsLayout = wx.BoxSizer( wx.HORIZONTAL )
        btnOk = wx.Button(self, label="Ok")
        btnOk.Bind(wx.EVT_BUTTON, self.OnOk)
        btnCancel = wx.Button(self, label="Cancel")
        btnCancel.Bind(wx.EVT_BUTTON, self.OnCancel)
        btnFillAll = wx.Button(self, label="Fill all as first year")
        btnsLayout.Add(btnOk, 0, wx.ALL, 5)
        btnsLayout.Add(btnCancel, 0, wx.ALL, 5)
        btnsLayout.Add(btnFillAll, 0, wx.ALL, 5)        
        mainLayout.Add(btnsLayout, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5)
        
        self.SetSizer( mainLayout )
        self.Layout()
        #mainLayout.Fit(self)
        self.Centre( wx.BOTH )
        
    def OnCancel(self, event):
        super().Close()
        
    def OnOk(self, event):
        for gt in self._gridTables:
            gt.Commit()
        super().Close()
    
    def SetContent(self, content, align):
        self._contentLayout.Add(content, 1, wx.ALL|wx.EXPAND|align, 5)
    
    def PopulateGrid(self, gridTable, dataPerYear):
        self._gridTables.append(gridTable)
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
