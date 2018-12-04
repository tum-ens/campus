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

    COMM_SUPLM  = 'SupIm'
    COMM_BUY    = 'Buy'
    COMM_STOCK  = 'Stock'
    COMM_DEMAND = 'Demand'
    COMM_SELL   = 'Sell'
    COMM_ENV    = 'Env'


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
        {PARAM_KEY: 'timeSer',
         GRID_COL_LABEL: 'Hidden', GRID_COL_DATATYPE: wx.grid.GRID_VALUE_STRING, PARAM_DEFVALUE: ''},
        {PARAM_KEY: 'price',
         GRID_COL_LABEL:'Commodity price (Euro/MWh)', GRID_COL_DATATYPE: wx.grid.GRID_VALUE_FLOAT, PARAM_DEFVALUE: 0.00},
        {PARAM_KEY: 'max',
         GRID_COL_LABEL: 'Maximum commodity use', GRID_COL_DATATYPE: wx.grid.GRID_VALUE_STRING, PARAM_DEFVALUE: 'inf'},
        {PARAM_KEY: 'maxPerHour',
         GRID_COL_LABEL: 'Maximum commodity use per step', GRID_COL_DATATYPE: wx.grid.GRID_VALUE_STRING, PARAM_DEFVALUE: 'inf'},
        {PARAM_KEY: 'Action',
         GRID_COL_LABEL: 'Time S.', GRID_COL_DATATYPE: wx.grid.GRID_VALUE_STRING, PARAM_DEFVALUE: '...'},
        {PARAM_KEY: 'delay',
         GRID_COL_LABEL:'Delay time (h)', GRID_COL_DATATYPE: wx.grid.GRID_VALUE_FLOAT, PARAM_DEFVALUE: 0.00},
        {PARAM_KEY: 'eff',
         GRID_COL_LABEL:'Efficiency', GRID_COL_DATATYPE: wx.grid.GRID_VALUE_FLOAT, PARAM_DEFVALUE: 0.00},
          {PARAM_KEY: 'recov',
         GRID_COL_LABEL:'Recovery time (h)', GRID_COL_DATATYPE: wx.grid.GRID_VALUE_FLOAT, PARAM_DEFVALUE: 0.00},
          {PARAM_KEY: 'capMaxDo',
         GRID_COL_LABEL:'Downshift capacity (MWh)', GRID_COL_DATATYPE: wx.grid.GRID_VALUE_FLOAT, PARAM_DEFVALUE: 0.00},
        {PARAM_KEY: 'capMaxUp',
         GRID_COL_LABEL:'Upshift capacity (MWh)', GRID_COL_DATATYPE: wx.grid.GRID_VALUE_FLOAT, PARAM_DEFVALUE: 0.00}
    ]

    COMMODITY_COLS = [
        {PARAM_KEY: 'selected',
         GRID_COL_LABEL:'', GRID_COL_DATATYPE: wx.grid.GRID_VALUE_BOOL, PARAM_DEFVALUE: ''},
        {PARAM_KEY: 'Name',
         GRID_COL_LABEL: 'Name', GRID_COL_DATATYPE: wx.grid.GRID_VALUE_STRING, PARAM_DEFVALUE: ''},
        {PARAM_KEY: 'Action',
         GRID_COL_LABEL: '', GRID_COL_DATATYPE: wx.grid.GRID_VALUE_STRING, PARAM_DEFVALUE: '...'}
    ]

    PROCESS_PARAMS = [
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
         GRID_COL_LABEL: 'Weighted average cost of capital', GRID_COL_DATATYPE: wx.grid.GRID_VALUE_FLOAT, PARAM_DEFVALUE: 0.05},
        {PARAM_KEY: 'maxGrad',
         GRID_COL_LABEL:'Maximum power gradient (1/h)', GRID_COL_DATATYPE: wx.grid.GRID_VALUE_STRING, PARAM_DEFVALUE: 'inf'},
        {PARAM_KEY: 'minFraction',
         GRID_COL_LABEL: 'Minimum load fraction', GRID_COL_DATATYPE: wx.grid.GRID_VALUE_STRING, PARAM_DEFVALUE: 'inf'},
        {PARAM_KEY: 'depreciation',
         GRID_COL_LABEL: 'Depreciation period (a)', GRID_COL_DATATYPE: wx.grid.GRID_VALUE_NUMBER, PARAM_DEFVALUE: 20},
        {PARAM_KEY: 'areaPerCap',
         GRID_COL_LABEL: 'Area use per capacity (m^2/MW)', GRID_COL_DATATYPE: wx.grid.GRID_VALUE_STRING, PARAM_DEFVALUE: 'inf'}
    ]

    CONNECTION_PARAMS = [
        {PARAM_KEY: 'ratio',
         GRID_COL_LABEL:'Ratio (1)', GRID_COL_DATATYPE: wx.grid.GRID_VALUE_FLOAT, PARAM_DEFVALUE: 1.00},
        {PARAM_KEY: 'ratioMin',
         GRID_COL_LABEL: 'Ratio-Min', GRID_COL_DATATYPE: wx.grid.GRID_VALUE_FLOAT, PARAM_DEFVALUE: 0.00}
    ]

    STORAGE_PARAMS = [
        {PARAM_KEY: 'instCapC',
         GRID_COL_LABEL:'Installed capacity (MWh)', GRID_COL_DATATYPE: wx.grid.GRID_VALUE_FLOAT, PARAM_DEFVALUE: 0.00},
        {PARAM_KEY: 'capLoC',
         GRID_COL_LABEL:'Minimum capacity (MWh)', GRID_COL_DATATYPE: wx.grid.GRID_VALUE_FLOAT, PARAM_DEFVALUE: 0.00},
        {PARAM_KEY: 'capUpC',
         GRID_COL_LABEL:'Maximum capacity (MWh)', GRID_COL_DATATYPE: wx.grid.GRID_VALUE_FLOAT, PARAM_DEFVALUE: 0.00},
        {PARAM_KEY: 'instCapP',
         GRID_COL_LABEL:'Installed storage power (MW)', GRID_COL_DATATYPE: wx.grid.GRID_VALUE_FLOAT, PARAM_DEFVALUE: 0.00},
        {PARAM_KEY: 'capLoP',
         GRID_COL_LABEL:'Minimum power (MW)', GRID_COL_DATATYPE: wx.grid.GRID_VALUE_FLOAT, PARAM_DEFVALUE: 0.00},
        {PARAM_KEY: 'capUpP',
         GRID_COL_LABEL:'Maximum power (MW)', GRID_COL_DATATYPE: wx.grid.GRID_VALUE_FLOAT, PARAM_DEFVALUE: 0.00},
        {PARAM_KEY: 'effIn',
         GRID_COL_LABEL:'Efficiency input (1)', GRID_COL_DATATYPE: wx.grid.GRID_VALUE_FLOAT, PARAM_DEFVALUE: 0.00},
        {PARAM_KEY: 'effOut',
         GRID_COL_LABEL:'Efficiency output (1)', GRID_COL_DATATYPE: wx.grid.GRID_VALUE_FLOAT, PARAM_DEFVALUE: 0.00},
        {PARAM_KEY: 'invCostP',
         GRID_COL_LABEL:'Investment cost power (€/MW)', GRID_COL_DATATYPE: wx.grid.GRID_VALUE_FLOAT, PARAM_DEFVALUE: 0.00},
        {PARAM_KEY: 'invCostC',
         GRID_COL_LABEL:'Investment cost cap. (€/MWh)', GRID_COL_DATATYPE: wx.grid.GRID_VALUE_FLOAT, PARAM_DEFVALUE: 0.00},
        {PARAM_KEY: 'fixCostP',
         GRID_COL_LABEL:'Fix cost power (€/MW/a)', GRID_COL_DATATYPE: wx.grid.GRID_VALUE_FLOAT, PARAM_DEFVALUE: 0.00},
        {PARAM_KEY: 'fixCostC',
         GRID_COL_LABEL:'Fix cost capacity (€/MWh/a)', GRID_COL_DATATYPE: wx.grid.GRID_VALUE_FLOAT, PARAM_DEFVALUE: 0.00},
        {PARAM_KEY: 'varCostP',
         GRID_COL_LABEL:'Variable cost in/out (€/MWh)', GRID_COL_DATATYPE: wx.grid.GRID_VALUE_FLOAT, PARAM_DEFVALUE: 0.00},
        {PARAM_KEY: 'varCostC',
         GRID_COL_LABEL:'Variable cost cap. (€/MWh)', GRID_COL_DATATYPE: wx.grid.GRID_VALUE_FLOAT, PARAM_DEFVALUE: 0.00},
        {PARAM_KEY: 'lifetime',
         GRID_COL_LABEL:'Lifetime inst-cap (years)', GRID_COL_DATATYPE: wx.grid.GRID_VALUE_FLOAT, PARAM_DEFVALUE: 0.00},
        {PARAM_KEY: 'depreciation',
         GRID_COL_LABEL:'Depreciation period (a)', GRID_COL_DATATYPE: wx.grid.GRID_VALUE_FLOAT, PARAM_DEFVALUE: 0.00},
        {PARAM_KEY: 'wacc',
         GRID_COL_LABEL:'Weighted average cost of capital', GRID_COL_DATATYPE: wx.grid.GRID_VALUE_FLOAT, PARAM_DEFVALUE: 0.00},
        {PARAM_KEY: 'init',
         GRID_COL_LABEL:'Initial storage content', GRID_COL_DATATYPE: wx.grid.GRID_VALUE_FLOAT, PARAM_DEFVALUE: 0.00},
        {PARAM_KEY: 'discharge',
         GRID_COL_LABEL:'Discharge', GRID_COL_DATATYPE: wx.grid.GRID_VALUE_FLOAT, PARAM_DEFVALUE: 0.00},
    ]
