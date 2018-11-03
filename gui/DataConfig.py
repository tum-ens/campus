# -*- coding: utf-8 -*-
"""
Created on Sat Nov  3 15:02:37 2018

@author: aelshaha
"""

import wx.grid

class DataConfig():
    
    PARAM_KEY        = 'key'
    PARAM_DEFVALUE   = 'defVal'
    
    GRID_COL_LABEL      = 'label'
    GRID_COL_DATATYPE   = 'dataType'
    
    
    YEAR_PARAMS = [
                  {PARAM_KEY: 'selected', 
                   GRID_COL_LABEL:'', GRID_COL_DATATYPE: wx.grid.GRID_VALUE_BOOL, PARAM_DEFVALUE: ''},
                  {PARAM_KEY: 'discountRate', 
                   GRID_COL_LABEL: 'Discount rate', GRID_COL_DATATYPE: wx.grid.GRID_VALUE_FLOAT, PARAM_DEFVALUE: 0.00},
                  {PARAM_KEY: 'co2Limit', 
                   GRID_COL_LABEL: 'CO2 limit', GRID_COL_DATATYPE: wx.grid.GRID_VALUE_STRING, PARAM_DEFVALUE: 'inf'},
                  {PARAM_KEY: 'co2Budet', 
                   GRID_COL_LABEL: 'CO2 budget', GRID_COL_DATATYPE: wx.grid.GRID_VALUE_NUMBER, PARAM_DEFVALUE: 1000000}
                ]
                     
    SITE_PARAMS = [
                  {PARAM_KEY: 'selected', 
                   GRID_COL_LABEL:'', GRID_COL_DATATYPE: wx.grid.GRID_VALUE_BOOL, PARAM_DEFVALUE: ''},
                  {PARAM_KEY: 'siteArea', 
                   GRID_COL_LABEL: 'Site Area', GRID_COL_DATATYPE: wx.grid.GRID_VALUE_NUMBER, PARAM_DEFVALUE: 100000}
                ]
                     
    COMMODITY_PARAMS = [
                  {PARAM_KEY: 'price', 
                   GRID_COL_LABEL:'Commodity price (Euro/MWh)', GRID_COL_DATATYPE: wx.grid.GRID_VALUE_FLOAT, PARAM_DEFVALUE: 0.00},
                  {PARAM_KEY: 'max', 
                   GRID_COL_LABEL: 'Maximum commodity use', GRID_COL_DATATYPE: wx.grid.GRID_VALUE_STRING, PARAM_DEFVALUE: 'inf'},
                  {PARAM_KEY: 'maxPerHour', 
                   GRID_COL_LABEL: 'Maximum commodity use per step', GRID_COL_DATATYPE: wx.grid.GRID_VALUE_STRING, PARAM_DEFVALUE: 'inf'}
                ]
                     
    