# -*- coding: utf-8 -*-
"""
Created on Mon Oct 29 19:03:07 2018

@author: aelshaha
"""

import wx        
import YearsView as yv
import SitesView as sv

class GeneralView(wx.Panel):
    
    _gridCols = ['', 'Discount rate', 'CO2 limit', 'CO2 budget']

    def __init__( self, parent ):
        wx.Panel.__init__ ( self, parent)
        self.SetBackgroundColour("black")
        #self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
        
        #
        yearsView = yv.YearsView(self)           
        yearsLayout = yearsView.GetLayout()
        
        sitesView = sv.SitesView(self)
        sitesLayout = sitesView.GetLayout()    
        
        mainLayout = wx.BoxSizer( wx.HORIZONTAL )
        mainLayout.Add(yearsLayout, 0, wx.ALL|wx.EXPAND, 5)
        mainLayout.Add(sitesLayout, 0, wx.ALL|wx.EXPAND, 5)
        
        
        self.SetSizer( mainLayout )
        self.Layout()        
        self.Centre( wx.BOTH )