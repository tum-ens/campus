# -*- coding: utf-8 -*-
"""
Created on Sat Nov  3 15:07:35 2018

@author: aelshaha
"""

import wx.grid
import copy as cpy
import DataConfig as config

class GridDataTable(wx.grid.GridTableBase):
    
    def __init__(self, cols, autoCommit=False):
        wx.grid.GridTableBase.__init__(self)
        
        self._cols = cols
        self._autoCommit = autoCommit        
        self._tmpData = {}
        self._data = {}
    
    #--------------------------------------------------
    def SetTableData(self, data):
        self._data = data
        if self._autoCommit:
            self._tmpData = self._data
        else:
            self._tmpData = cpy.deepcopy(self._data)
            
    def Commit(self):
        #print('Commit')
        self._data.update(self._tmpData) #only if data is NOT shared
#        for year, params in self._tmpData.items():
#            for col in self._cols:
#                colKey = col[config.DataConfig.PARAM_KEY]
#                self._data[year][colKey] = params[colKey]
    
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
            return not self._tmpData[rowKey][colKey]

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
            return self._tmpData[rowKey][colKey]

        return ''
    
    def SetValue(self, row, col, value):
        #print('SetValue', row, col, value)
        v = self.ConvertToNumber(value)
        if not v:
            return
        
        rowKey = self.GetRowLabelValue(row)
        colKey = self._cols[col][config.DataConfig.PARAM_KEY]
        
        self._tmpData[rowKey][colKey] = v
    
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
        
    def GetData(self):
        return self._tmpData
    
    def FillAll(self):
        data = {}
        if self._autoCommit:
            data = self._data
        else:
            data = self._tmpData
            
        if len(data) == 0: return

        firstKey = sorted(data)[0]
        for key in data.keys():
            if key != firstKey:
                data[key] = data[firstKey]

    def ConvertToNumber(self, value):
        try:
            vf = float(value)
            try:
                vi = int(value)
                return "{:,}".format(vi)
            except ValueError:            
                return "{:,}".format(vf)
        except ValueError:
            if value.lower() == config.DataConfig.INF.lower():
                return config.DataConfig.INF
            else:
                return None
#---------------------------------------------------------------------------
