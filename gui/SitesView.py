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

class SitesView():
    
    _gridCols = ['', 'Site Area']

    def __init__(self, parent):
        
        #manage layout
        headerBox = wx.StaticBox(parent, wx.ID_ANY, u"Manage Sites:" )
        headerBox.SetForegroundColour('white')
        
        self._mainLayout = wx.StaticBoxSizer(headerBox , wx.HORIZONTAL )
        sitesLayout = wx.BoxSizer( wx.VERTICAL )
        #imgLayout = wx.BoxSizer( wx.VERTICAL )
        
        self._mainLayout.Add(sitesLayout, 0, wx.ALL|wx.EXPAND, 5 )
        #mainLayout.Add(imgLayout, 1, wx.EXPAND|wx.ALIGN_CENTER, 5 )
        
        #Add site section        
        addSiteLayout = wx.StaticBoxSizer( wx.StaticBox(parent, wx.ID_ANY, u"" ), wx.HORIZONTAL )
        #label = wx.StaticText(addSiteLayout.GetStaticBox(), -1, "Site:")
        #addSiteLayout.Add(label, 0, wx.ALL, 5)
        
        self._txtSite = wx.TextCtrl(addSiteLayout.GetStaticBox())
        self._txtSite.Bind(wx.EVT_TEXT, self.TxtSiteOnTextChange)
        addSiteLayout.Add(self._txtSite, 0, wx.ALL, 5)
        
        self._btnAdd = wx.Button(addSiteLayout.GetStaticBox(), label="Add Site")
        self._btnAdd.Bind(wx.EVT_BUTTON, self.BtnAddOnClick) 
        self._btnAdd.Disable()
        addSiteLayout.Add(self._btnAdd, 0, wx.ALL, 5)
        
        self._btnRemove = wx.Button(addSiteLayout.GetStaticBox(), label="Remove Selected Site(s)")
        self._btnRemove.Bind(wx.EVT_BUTTON, self.BtnRemoveOnClick)
        #self._btnRemove.Disable()
        addSiteLayout.Add(self._btnRemove, 0, wx.ALL, 5 )
        
        sitesLayout.Add(addSiteLayout, 0, wx.ALL|wx.EXPAND, 5)
        
        #Grid of 4 cols
        self._sitesGrid = wx.grid.Grid(parent, -1)
        self._sitesGrid.CreateGrid(0, len(self._gridCols))
        #col1 as checkbox
        attr = wx.grid.GridCellAttr()
        attr.SetEditor(wx.grid.GridCellBoolEditor())
        attr.SetRenderer(wx.grid.GridCellBoolRenderer())        
        #col2-4
        for i in range(0, len(self._gridCols)):
            self._sitesGrid.SetColSize(i, 120)
            self._sitesGrid.SetColLabelValue(i, self._gridCols[i])
        self._sitesGrid.SetColAttr(0, attr)
        self._sitesGrid.SetColSize(0, 20)
        #self._listOfYrs.Bind( wx.EVT_LIST_ITEM_SELECTED, self.ListOfSitesOnSelectionChange)
        #self._listOfYrs.Bind( wx.EVT_LIST_ITEM_DESELECTED, self.ListOfSitesOnSelectionChange)
                
        sitesLayout.Add(self._sitesGrid, 1, wx.ALL|wx.EXPAND, 5)
        
        #bitmap = wx.StaticBitmap( self, wx.ID_ANY, wx.Bitmap( u"Energy.jpeg", wx.BITMAP_TYPE_ANY ))
        #imgLayout.Add(bitmap, 1, wx.EXPAND, 5)          
        
        pub.subscribe(self.PopulateSitesGrid, EVENTS.SITE_ADDED)
        pub.subscribe(self.PopulateSitesGrid, EVENTS.SITE_REMOVED)
        
    def GetLayout(self):
        return self._mainLayout;                        
    
    def TxtSiteOnTextChange(self, event):
        txt = event.GetEventObject().GetValue()
        if len(txt) > 0:
            self._btnAdd.Enable()
        else:
            self._btnAdd.Disable()
        
        
    def BtnAddOnClick(self, event):
        newSite = self._txtSite.GetValue()
        pub.sendMessage(EVENTS.SITE_ADDING, site=newSite)
            
    def BtnRemoveOnClick(self, event):
        rows = self._sitesGrid.GetNumberRows()
        if rows == 0:
            return
        
        sitesToRmv = []
        for i in range(0, rows):
            val = self._sitesGrid.GetCellValue(i, 0)
            if val:
                sitesToRmv.append(self._sitesGrid.GetRowLabelValue(i))
        
        pub.sendMessage(EVENTS.SITE_REMOVING, sites=sitesToRmv)
        
    def PopulateSitesGrid(self, sites):       
        i = self._sitesGrid.GetNumberRows()
        if i > 0:
            self._sitesGrid.DeleteRows(0, i)
            i = 0
            
        sites = collections.OrderedDict(sorted(sites.items()))
        for site, data in sites.items():
            self._sitesGrid.InsertRows(i, 1)
            self._sitesGrid.SetRowLabelValue(i, site)
            #self._sitesGrid.SetCellValue(i, 0, bool(data['selected']))
            self._sitesGrid.SetCellValue(i, 1, data['siteArea'])
            i += 1