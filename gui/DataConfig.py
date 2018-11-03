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

    PROCESS_ECO_PARAMS = [
                  {PARAM_KEY: 'instCap', 
                   GRID_COL_LABEL:'Installed capacity (MW)', GRID_COL_DATATYPE: wx.grid.GRID_VALUE_FLOAT, PARAM_DEFVALUE: 0.00},
                  {PARAM_KEY: 'lifetime', 
                   GRID_COL_LABEL: 'Lifetime of inst-cap (years)', GRID_COL_DATATYPE: wx.grid.GRID_VALUE_FLOAT, PARAM_DEFVALUE: 0.00},
                  {PARAM_KEY: 'capLo', 
                   GRID_COL_LABEL: 'Minimum capacity (MW)', GRID_COL_DATATYPE: wx.grid.GRID_VALUE_FLOAT, PARAM_DEFVALUE: 0.00},
                  {PARAM_KEY: 'capUp', 
                   GRID_COL_LABEL:'Maximum capacity (MW)', GRID_COL_DATATYPE: wx.grid.GRID_VALUE_FLOAT, PARAM_DEFVALUE: 0.00},
                  {PARAM_KEY: 'invCost', 
                   GRID_COL_LABEL: 'Investment cost (Euro/MW)', GRID_COL_DATATYPE: wx.grid.GRID_VALUE_FLOAT, PARAM_DEFVALUE: 0.00},
                  {PARAM_KEY: 'fixCost', 
                   GRID_COL_LABEL: 'Annual fix cost (Euro/MW/a)', GRID_COL_DATATYPE: wx.grid.GRID_VALUE_STRING, PARAM_DEFVALUE: 'inf'},
                  {PARAM_KEY: 'varCost', 
                   GRID_COL_LABEL:'Variable costs (Euro/MWh)', GRID_COL_DATATYPE: wx.grid.GRID_VALUE_STRING, PARAM_DEFVALUE: 'inf'},
                  {PARAM_KEY: 'startupCost', 
                   GRID_COL_LABEL: 'Startup cost (Euro)', GRID_COL_DATATYPE: wx.grid.GRID_VALUE_STRING, PARAM_DEFVALUE: 'inf'},
                  {PARAM_KEY: 'wacc', 
                   GRID_COL_LABEL: 'Weighted average cost of capital', GRID_COL_DATATYPE: wx.grid.GRID_VALUE_FLOAT, PARAM_DEFVALUE: 0.05}                          
                ]
                
    PROCESS_TECH_PARAMS = [
                  {PARAM_KEY: 'maxGrad', 
                   GRID_COL_LABEL:'Maximum power gradient (1/h)', GRID_COL_DATATYPE: wx.grid.GRID_VALUE_STRING, PARAM_DEFVALUE: 'inf'},
                  {PARAM_KEY: 'minFraction', 
                   GRID_COL_LABEL: 'Minimum load fraction', GRID_COL_DATATYPE: wx.grid.GRID_VALUE_STRING, PARAM_DEFVALUE: 'inf'},
                  {PARAM_KEY: 'depreciation', 
                   GRID_COL_LABEL: 'Depreciation period (a)', GRID_COL_DATATYPE: wx.grid.GRID_VALUE_NUMBER, PARAM_DEFVALUE: 20},
                  {PARAM_KEY: 'areaPerCap', 
                   GRID_COL_LABEL: 'Area use per capacity (m^2/MW)', GRID_COL_DATATYPE: wx.grid.GRID_VALUE_STRING, PARAM_DEFVALUE: 'inf'}
                ]
                     
    