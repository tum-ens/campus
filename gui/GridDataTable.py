# -*- coding: utf-8 -*-
"""
Created on Sat Nov  3 15:07:35 2018

@author: aelshaha
"""

import wx.grid
import DataConfig as config

class GridDataTable(wx.grid.GridTableBase):
    
    def __init__(self, cols, data = {}):
        wx.grid.GridTableBase.__init__(self)
        
        self._cols = cols
        self._data = {}
    
    #--------------------------------------------------
    def SetTableData(self, data):
        self._data = data
    
    #--------------------------------------------------
    # required methods for the wxPyGridTableBase interface
    def GetNumberRows(self):
        #print('GetNumberRows', len(self._data))
        return len(self._data)
    
    def GetNumberCols(self):
        #print('GetNumberCols', len(self._cols))
        return len(self._cols)
    
    def IsEmptyCell(self, row, col):
        #print('IsEmptyCell', row, col)
        rowKey = self.GetRowLabelValue(row)
        colKey = self._cols[col][config.DataConfig.PARAM_KEY]
        if rowKey and colKey:
            return not self._data[rowKey][colKey]

        return True
    
    # Get/Set values in the table.  The Python version of these
    # methods can handle any data-type, (as long as the Editor and
    # Renderer understands the type too,) not just strings as in the
    # C++ version.
    def GetValue(self, row, col):
        #print('GetValue', row, col)
        rowKey = self.GetRowLabelValue(row)
        colKey = self._cols[col][config.DataConfig.PARAM_KEY]
        if rowKey and colKey:
            return self._data[rowKey][colKey]

        return ''
    
    def SetValue(self, row, col, value):
        #print('SetValue', row, col, value)
        rowKey = self.GetRowLabelValue(row)
        colKey = self._cols[col][config.DataConfig.PARAM_KEY]
        self._data[rowKey][colKey] = value
    
    #--------------------------------------------------
    # Some optional methods
    # Called when the grid needs to display labels
    def GetColLabelValue(self, col):
        #print('GetColLabelValue', col)
        return self._cols[col][config.DataConfig.GRID_COL_LABEL]

    def GetRowLabelValue(self, row):
        #print('GetRowLabelValue', row, len(self._data))
        if row < len(self._data):
            return sorted(list(self._data.keys()))[row]

        return ''
    
    # Called to determine the kind of editor/renderer to use by
    # default, doesn't necessarily have to be the same type used
    # natively by the editor/renderer if they know how to convert.
    def GetTypeName(self, row, col):
        #print('GetTypeName', row, col)
        return self._cols[col][config.DataConfig.GRID_COL_DATATYPE]
    
    # Called to determine how the data can be fetched and stored by the
    # editor and renderer.  This allows you to enforce some type-safety
    # in the grid.
    def CanGetValueAs(self, row, col, typeName):
        colType = self._cols[col][config.DataConfig.GRID_COL_DATATYPE]
        if typeName == colType:
            return True
        else:
            return False
    
    def CanSetValueAs(self, row, col, typeName):
        return self.CanGetValueAs(row, col, typeName)
#---------------------------------------------------------------------------
