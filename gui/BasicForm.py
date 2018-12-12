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
        btnFillAll.Bind(wx.EVT_BUTTON, self.OnFillAll)
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
        
    def OnFillAll(self, event):
        for gt in self._gridTables:
            gt.FillAll()
            msg = wx.grid.GridTableMessage(gt, wx.grid.GRIDTABLE_REQUEST_VIEW_GET_VALUES)
            gt.GetView().ProcessTableMessage(msg)
    
    def SetContent(self, content, align):
        self._contentLayout.Add(content, 1, wx.ALL|wx.EXPAND|align, 5)
    
    def PopulateGrid(self, gridTable, dataPerYear):
        self._gridTables.clear()
        self._gridTables.append(gridTable)
        self._grid = gridTable.GetView()
        #self._grid.Bind(wx.EVT_KEY_DOWN, self.OnKeyPress)
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

    def OnKeyPress(self, event):
        if event.ControlDown() and event.GetKeyCode() == 86:
            if not wx.TheClipboard.IsOpened():  # may crash, otherwise
                do = wx.TextDataObject()
                wx.TheClipboard.Open()
                success = wx.TheClipboard.GetData(do)
                wx.TheClipboard.Close()
                if success:
                    s = do.GetText()
                    s = str.replace(s, ',', '')
                    cells = s.split('\t')
                    row = self._grid.GetGridCursorRow()
                    col = self._grid.GetGridCursorCol()
                    for v in cells:
                        if col < self._grid.GetNumberCols():
                            self._grid.SetCellValue(row, col, v)
                            col+=1                