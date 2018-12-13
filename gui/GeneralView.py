# -*- coding: utf-8 -*-
"""
Created on Mon Oct 29 19:03:07 2018

@author: aelshaha
"""

import wx        
import YearsView as yv
import SitesView as sv
import GlobalsView as gv

class GeneralView(wx.Panel):
    
    def __init__( self, parent, controller ):
        wx.Panel.__init__ ( self, parent)
        self.SetBackgroundColour("black")
        #self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
        
        #
        yearsView = yv.YearsView(self)
        yearsLayout = yearsView.GetLayout()
        
        sitesView = sv.SitesView(self)
        sitesLayout = sitesView.GetLayout()
        
        globalsLayout = gv.GlobalsView(self, controller).GetLayout()
        
        mainLayout = wx.BoxSizer( wx.HORIZONTAL )        
        mainLayout.Add(sitesLayout, 0, wx.ALL|wx.EXPAND, 5)
        mainLayout.Add(yearsLayout, 0, wx.ALL|wx.EXPAND, 5)
        mainLayout.Add(globalsLayout, 1, wx.ALL|wx.EXPAND, 5)
        
        
        self.SetSizer( mainLayout )
        self.Layout()        
        self.Centre( wx.BOTH )