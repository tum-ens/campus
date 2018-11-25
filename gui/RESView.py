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
import RESEvtHandler as evt


from pubsub import pub
from Events import EVENTS

class ProcessShape(ogl.RectangleShape):
    def __init__(self, canvas, x, y, uuid, text):
        self._width = 150
        self._hight = 30
        ogl.RectangleShape.__init__(self, self._width, self._hight)
        self.SetDraggable(False, False)
        self.SetCanvas(canvas)
        self.SetX(x)
        self.SetY(y)
        self.SetPen(wx.BLACK_PEN)
        self.SetBrush(wx.WHITE_BRUSH)
        if text:
            self.AddText(text)
        #shape.SetShadowMode(ogl.SHADOW_RIGHT)
        self.SetFont(wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.BOLD))
        canvas.GetDiagram().AddShape(self)
        self.Show(True)        

        evthandler = evt.RESEvtHandler()
        evthandler.SetShape(self)
        evthandler.SetPreviousHandler(self.GetEventHandler())
        self.SetEventHandler(evthandler)
        
        self._uuid = uuid
        
    def GetId(self):
        return self._uuid
    
    def GetAttachX(self, forward=False):
        if forward: 
            return self.GetX() + self._width/2

        return self.GetX() - self._width/2

    def GetAttachY(self):
        return self.GetY() - self._hight/2

class CommodityShape(ogl.LineShape):
    def __init__(self, canvas, x, y, uuid, text, color):
        ogl.LineShape.__init__(self)        
        self.MakeLineControlPoints(2)
        self.SetEnds(x, y, x, 2000)
        #self.SetDraggable(True, True)
        self.SetCanvas(canvas)
        self._color = color
        self.SetPen(wx.Pen(color, 0.5, wx.SOLID))
        #if brush:  shape.SetBrush(brush)
        if text:
            #self.AddText(text)
            self.SetFormatMode(ogl.FORMAT_SIZE_TO_CONTENTS, 1)
            self.FormatText(wx.ClientDC(canvas), text, 1)## start
        #shape.SetShadowMode(ogl.SHADOW_RIGHT)
        self.SetFont(wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.BOLD))
        canvas.GetDiagram().AddShape(self)
        self.Show(True)        

        evthandler = evt.RESEvtHandler()
        evthandler.SetShape(self)
        evthandler.SetPreviousHandler(self.GetEventHandler())
        self.SetEventHandler(evthandler)
        
        self._uuid = uuid
        
    def GetId(self):
        return self._uuid
    
    def GetGroup(self):
        return self._uuid[0]

    def GetColor(self):
        return self._color
        
class ConnectionShape(ogl.LineShape):
    def __init__(self, canvas, uuid, color):
        ogl.LineShape.__init__(self)
        self.MakeLineControlPoints(2)
        self.AddArrow(ogl.ARROW_ARROW)
        #self.SetDraggable(True, True)
        self.SetCanvas(canvas)
        self.SetPen(wx.Pen(color, 0.5, wx.SOLID))
        #if brush:  shape.SetBrush(brush)
        #shape.SetShadowMode(ogl.SHADOW_RIGHT)
        canvas.GetDiagram().AddShape(self)
        self.Show(True)
        
        self._uuid = uuid
        
    def GetId(self):
        return self._uuid   

class RESView(wx.Panel):     
    
    _shapes = {}

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
                }
    

    def __init__( self, parent, controller ):
        wx.Frame.__init__ ( self, parent)
        self._controller = controller
        #self.SetBackgroundColour("black")
        
        #manage layout
        mainLayout = wx.BoxSizer( wx.VERTICAL )
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
        mainLayout.Add(barLayout, 0, wx.ALL|wx.EXPAND, 2)
        
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
        
        mainLayout.Add(self._canvas, 1, wx.ALL|wx.EXPAND, 5)        
        
        self.SetSizer( mainLayout )
        self.Layout()        
        self.Centre( wx.BOTH )
        
        
        pub.subscribe(self.ShapOnDoubleClick, EVENTS.SHAPE_DOUBLE_CLICK)
        #pub.subscribe(self.ShapeSelect, EVENTS.SHAPE_SELECTED)
        #pub.subscribe(self.ShapeDeselect, EVENTS.SHAPE_DESELECTED)
        
        pub.subscribe(self.RebuildRES, EVENTS.COMMODITY_ADDED)
        pub.subscribe(self.RebuildRES, EVENTS.COMMODITY_EDITED)
        pub.subscribe(self.RebuildRES, EVENTS.PROCESS_ADDED)        
        pub.subscribe(self.RebuildRES, EVENTS.PROCESS_EDITED)
        #pub.subscribe(self.ConnectionIsAdded, EVENTS.CONNECTION_ADDED)
        
    def OnToolClick(self, event):
       #print("tool %s clicked\n" % event.GetId())
       if event.GetId() == 10:
           pub.sendMessage(EVENTS.PROCESS_ADDING)
       else:
           commType = self._actions[event.GetId()]['Name']
           pub.sendMessage(EVENTS.COMMODITY_ADDING, commType=commType)
    #-------------------------------------------------------------------------#   
    def RefreshCanvas(self):
       dc = wx.ClientDC(self._canvas)
       self._canvas.PrepareDC(dc)
       self._canvas.Redraw(dc)
    #-------------------------------------------------------------------------#    
    def ShapOnDoubleClick(self, shapeId):        
        shapeType = self._shapes[shapeId]['type']
        if shapeType == 'process':
            pub.sendMessage(EVENTS.PROCESS_EDITING, processId=self._shapes[shapeId]['uId'])
        elif shapeType == 'commodity':
            pub.sendMessage(EVENTS.COMMODITY_EDITING, commId=self._shapes[shapeId]['uId'])
        #elif shapeType == 'connection':
        #    pub.sendMessage(EVENTS.CONNECTION_EDITING, connId=self._shapes[shapeId]['uId'])       

    #-------------------------------------------------------------------------#    
    def RebuildRES(self):
        #print('Inside Rebuild')
        self.RemoveAllShapes()
        self.DrawCommAndProc()
        
        #draw connections
        processes = self._controller.GetProcesses()
        for k in sorted(processes):
            p = processes[k]
            procShape = self._shapes[k]['shape']
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
    #-------------------------------------------------------------------------#
    def BuildConnections(self, p, procShape):        
        lines = []            
        lineY = procShape.GetAttachY()
        #Draw in (always from left to right)
        for inComm in p['IN']:
            commShape = self._shapes[inComm]['shape']
            line = ConnectionShape(self._canvas, wx.ID_ANY, commShape.GetColor())
            line.SetEnds(commShape.GetX(), lineY, procShape.GetAttachX(), lineY)
            lines.append(line)
        #Draw out
        for outComm in p['OUT']:
            commShape = self._shapes[outComm]['shape']
            line = ConnectionShape(self._canvas, wx.ID_ANY, commShape.GetColor())
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

            commShape = CommodityShape(self._canvas, x, 10, k, data['Name'], data['Color'])            
            self._shapes[k] = {'type': 'commodity', 'uId': k, 'shape': commShape}
            processes = self._controller.GetLinkedProcesses(k)
            #print(processes)            
            if len(processes) > 0: 
                x+=100
            for k in sorted(processes):
                y+=10                
                p = processes[k]
                procShape = ProcessShape(self._canvas, x, y, p['Id'], p['Name'])
                self._shapes[procShape.GetId()] = {'type': 'process', 'uId': p['Id'], 'shape': procShape}                    
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
    
    def RemoveAllShapes(self):
        dc = wx.ClientDC(self._canvas)
        self._canvas.PrepareDC(dc)
        for shape in self._diagram.GetShapeList():
            shape.Show(False)        
            self._canvas.RemoveShape(shape)
            
        self._diagram.RemoveAllShapes()
        self._diagram.Clear(dc)
        self._canvas.Redraw(dc)
        self._shapes.clear()