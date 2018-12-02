# -*- coding: utf-8 -*-
"""
Created on Tue Oct 30 11:07:15 2018

@author: aelshaha
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Oct 29 19:03:07 2018

@author: aelshaha
"""

import wx
import wx.lib.ogl as ogl
import RESShapes as res

from pubsub import pub
from Events import EVENTS

class RESView(wx.Panel):

    _actions = {1 : {'Name' : 'SupIm', 'ImgPath' : 'Solar_WE_10.png'},
                2 : {'Name' : 'Buy', 'ImgPath' : 'Buy.png'},
                #######################################################
                3 : {'Name' : 'Stock', 'ImgPath' : 'Gas.png'},
                #######################################################
                4 : {'Name' : 'Demand', 'ImgPath' : 'Elec.png'},
                5 : {'Name' : 'Sell', 'ImgPath' : 'Sell.png'},
                6 : {'Name' : 'Env', 'ImgPath' : 'Env.png'},
                #######################################################
                10 : {'Name' : 'Process', 'ImgPath' : 'Process.png'},
                11 : {'Name' : 'Storage', 'ImgPath' : 'Storage.png'},
                }
    

    def __init__( self, parent, controller, siteName ):
        wx.Frame.__init__ ( self, parent)
        self._controller = controller
        self._siteName = siteName
        self._shapes   = {}
        #self.SetBackgroundColour("black")
        
        #manage layout
        mainLayout = wx.BoxSizer( wx.VERTICAL )
        barLayout = self.BuildToolBar()
        mainLayout.Add(barLayout, 0, wx.ALL|wx.EXPAND, 2)
        
        self.BuildCanvas()
        mainLayout.Add(self._canvas, 1, wx.ALL|wx.EXPAND, 5)
        
        self.SetSizer( mainLayout )
        self.Layout()        
        self.Centre( wx.BOTH )
        
        pub.subscribe(self.RebuildRES, EVENTS.COMMODITY_ADDED + self._siteName)
        pub.subscribe(self.RebuildRES, EVENTS.COMMODITY_EDITED + self._siteName)
        pub.subscribe(self.RebuildRES, EVENTS.PROCESS_ADDED + self._siteName)
        pub.subscribe(self.RebuildRES, EVENTS.PROCESS_EDITED + self._siteName)
        #pub.subscribe(self.ConnectionIsAdded, EVENTS.CONNECTION_ADDED)
        
        pub.subscribe(self.OnItemMove, EVENTS.ITEM_MOVED + self._siteName)
    #-------------------------------------------------------------------------#
    def GetSiteName(self):
        return self._siteName
    #-------------------------------------------------------------------------#
    def BuildToolBar(self):
        barLayout = wx.BoxSizer( wx.HORIZONTAL )
        
        actionsLayout = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Actions:" ), wx.HORIZONTAL )
        tb = wx.ToolBar( actionsLayout.GetStaticBox(), -1 , style=wx.TB_HORIZONTAL|wx.TB_FLAT) 
        for key, val in self._actions.items():
            img = wx.Image('./imgs/' + val['ImgPath'], wx.BITMAP_TYPE_ANY)
            #img = img.Scale(32, 32)
            tooltip = val['Name']
            if key%10 == 0:
                tb.AddSeparator()
            tb.AddTool(key, tooltip, wx.Bitmap(img), wx.NullBitmap, wx.ITEM_NORMAL, tooltip, "Add new '" + tooltip + "'", None)
        
        tb.Bind(wx.EVT_TOOL, self.OnToolClick)
        actionsLayout.Add(tb, 1, wx.ALL|wx.EXPAND, 2)
        tb.Realize()
        
        barLayout.Add(actionsLayout, 1, wx.ALL|wx.EXPAND, 2)
        
        return barLayout
    #-------------------------------------------------------------------------#    
    def OnToolClick(self, event):
       #print("tool %s clicked\n" % event.GetId())
       if event.GetId() == 10:
           pub.sendMessage(EVENTS.PROCESS_ADDING)
       elif event.GetId() == 11:
           pub.sendMessage(EVENTS.STORAGE_ADDING)
       else:
           commType = self._actions[event.GetId()]['Name']
           pub.sendMessage(EVENTS.COMMODITY_ADDING, commType=commType)
    #-------------------------------------------------------------------------#       
    def BuildCanvas(self):
        ogl.OGLInitialize() 
        self._canvas = ogl.ShapeCanvas(self)
        maxWidth  = 4000
        maxHeight = 2000
        self._canvas.SetScrollbars(20, 20, maxWidth/20, maxHeight/20)
        self._canvas.SetBackgroundColour(wx.WHITE)
        self._diagram = ogl.Diagram()
        self._canvas.SetDiagram(self._diagram)
        self._diagram.SetCanvas(self._canvas)
        #self._canvas.Bind(wx.EVT_CHAR_HOOK, self.WhenAkeyIsPressed)
        
    #-------------------------------------------------------------------------#   
    def RefreshCanvas(self):
       dc = wx.ClientDC(self._canvas)
       self._canvas.PrepareDC(dc)
       self._canvas.Redraw(dc)

    #-------------------------------------------------------------------------#    
    def RebuildRES(self):
        #print('Inside Rebuild')
        self.RemoveAllShapes()
        self.DrawCommAndProc()
        
        #draw connections
        processes = self._controller.GetProcesses()
        for k in sorted(processes):
            p = processes[k]
            procShape = self._shapes[k]
            conns = self.BuildConnections(p, procShape)
            self.DrawProcConnections(procShape, conns)
                
        self.RefreshCanvas()
    #-------------------------------------------------------------------------#
    def DrawProcConnections(self, procShape, lines):
        #loop on lines and adjust Y
        leftLines = [l for l in lines if l.GetX() < procShape.GetX()]
        rightLines= [l for l in lines if l.GetX() > procShape.GetX()]
        #print(leftLines, rightLines)
        lineY = procShape.GetAttachY()
        for line in leftLines:
            lineY += procShape._hight / (len(leftLines)+1)
            line.SetEnds(line.GetEnds()[0], lineY, line.GetEnds()[2], lineY)
        
        lineY = procShape.GetAttachY()
        for line in rightLines:
            lineY += procShape._hight / (len(rightLines)+1)
            line.SetEnds(line.GetEnds()[0], lineY, line.GetEnds()[2], lineY)
            
        procShape.SetConnections(lines)
    #-------------------------------------------------------------------------#
    def BuildConnections(self, p, procShape):        
        lines = []            
        lineY = procShape.GetAttachY()
        #Draw in (always from left to right)
        isDblArrow = (p['Type'] == 'Storage')
        for inComm in p['IN']:
            commShape = self._shapes[inComm]
            line = res.ConnectionShape(self._canvas, wx.ID_ANY, commShape.GetColor(), isDblArrow)
            line.SetEnds(commShape.GetX(), lineY, procShape.GetAttachX(), lineY)
            lines.append(line)
        #Draw out
        for outComm in p['OUT']:
            commShape = self._shapes[outComm]
            line = res.ConnectionShape(self._canvas, wx.ID_ANY, commShape.GetColor())
            x1, x2 = 0, 0
            if commShape.GetX() > procShape.GetX():
                x1 = procShape.GetAttachX(True)
            else:
                x1 = procShape.GetAttachX()
            x2 = commShape.GetX()
            line.SetEnds(x1, lineY, x2, lineY)
            lines.append(line)
            
        return lines
    #-------------------------------------------------------------------------#
    def DrawCommAndProc(self):
        commDict = self._controller.GetCommodities()
        x, y = 50, 50
        prevGrp = '0'
        prevCommHasProc = False
        for k in sorted(commDict):
            xOffset = 100
            data = commDict[k]            
            if prevGrp != data['Group']:
                if prevCommHasProc: x -= 100
                self.DrawGroupArea(x)
                prevGrp = data['Group']                
                if prevCommHasProc: 
                    x += 100
                else:
                    x += xOffset

            commShape = res.CommodityShape(self._canvas, x, 10, k, data['Name'], data['Color'])            
            self._shapes[k] = commShape
            processes = self._controller.GetLinkedProcesses(k)
            #print(processes)            
            if len(processes) > 0: 
                x+=100
            for k in sorted(processes):
                if k in self._shapes.keys():
                    y = self._shapes[k].GetY()
                else:
                    y = 60                
                p = processes[k]
                procShape = res.ProcessShape(self._canvas, x, y, k, p['Name'], p['Type'])
                self._shapes[procShape.GetId()] = procShape
                #move positions to draw next process
                if procShape._width > xOffset: xOffset = procShape._width                
                y+= procShape._height                
                        
            if len(processes) > 0: 
                x = x + xOffset/2 + 25
                prevCommHasProc = True
            else:
                x += xOffset
                prevCommHasProc = False
    #-------------------------------------------------------------------------#
    def DrawGroupArea(self, x):
        line = ogl.LineShape()
        line.MakeLineControlPoints(2)
        line.SetEnds(x, 0, x, 2000)
        #self.SetDraggable(True, True)
        line.SetCanvas(self._canvas)
        line.SetPen(wx.Pen(wx.BLACK, 1, wx.DOT_DASH|wx.ALPHA_TRANSPARENT))
        #if brush:  shape.SetBrush(brush)
        self._diagram.AddShape(line)
        line.Show(True)        
    #-------------------------------------------------------------------------#
    def RemoveAllShapes(self):
        dc = wx.ClientDC(self._canvas)
        self._canvas.PrepareDC(dc)
        for shape in self._diagram.GetShapeList():
            shape.Show(False)        
            self._canvas.RemoveShape(shape)
            
        self._diagram.RemoveAllShapes()
        self._diagram.Clear(dc)
        self._canvas.Redraw(dc)
        #self._shapes.clear()
    #-------------------------------------------------------------------------#
    def OnItemMove(self, item):
        dc = wx.ClientDC(self._canvas)
        self._canvas.PrepareDC(dc)
        process = item
        lines = process.GetConnections()
        self.DrawProcConnections(process, lines)
            
        self._diagram.Clear(dc)
        self._canvas.Redraw(dc)
        