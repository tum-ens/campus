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

class RESView(wx.Panel):     
    
    _shapes = {}

    _commodityImgs = {  1 : {'Name' : 'Solar S 30°', 'ImgPath' : './imgs/Solar_S_30.png'},
                        2 : {'Name' : 'Solar WE 10°', 'ImgPath' : './imgs/Solar_WE_10.png'},
                        3 : {'Name' : 'Elec', 'ImgPath' : './imgs/Elec.png'},
                        4 : {'Name' : 'Heat', 'ImgPath' : './imgs/Heat.png'},
                        5 : {'Name' : 'Cold', 'ImgPath' : './imgs/Cold.png'},
                        6 : {'Name' : 'Heat low', 'ImgPath' : './imgs/Heat_low.png'},
                        7 : {'Name' : 'Gas', 'ImgPath' : './imgs/Gas.png'},
                        8 : {'Name' : 'H2', 'ImgPath' : './imgs/H2.png'},
                        9 : {'Name' : 'IS CC', 'ImgPath' : './imgs/IS_CC.png'},
                        10 : {'Name' : 'Slack', 'ImgPath' : './imgs/Slack.png'},
                        11 : {'Name' : 'Geothermal Heat', 'ImgPath' : './imgs/Geothermal_Heat.png'},
                        12 : {'Name' : 'Gridelec Mix', 'ImgPath' : './imgs/Gridelec_Mix.png'},
                        13 : {'Name' : 'Gridelec Green', 'ImgPath' : './imgs/Gridelec_Green.png'},
                        14 : {'Name' : 'CO2', 'ImgPath' : './imgs/CO2.png'}
                      }
    

    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent)
        #self.SetBackgroundColour("black")        
        #self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
        
        #manage layout
        mainLayout = wx.BoxSizer( wx.VERTICAL )
        barLayout = wx.BoxSizer( wx.HORIZONTAL )
        
        #self._btnAdd = wx.Button(self, label="Add Shape!")
        #self._btnAdd.Bind(wx.EVT_BUTTON, self.BtnAddOnClick) 
        #mainLayout.Add(self._btnAdd, 0, wx.ALL, 5)
        
        commoditiesLayout = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Commodities:" ), wx.HORIZONTAL )
        tb = wx.ToolBar( commoditiesLayout.GetStaticBox(), -1 ) 
        for key, val in self._commodityImgs.items():
            img = wx.Image(val['ImgPath'], wx.BITMAP_TYPE_ANY)
            #img = img.Scale(32, 32)
            tooltip = val['Name']
            tb.AddTool(key, tooltip, wx.Bitmap(img), wx.NullBitmap, wx.ITEM_NORMAL, tooltip, "Add new '" + tooltip + "'", None)
        
        tb.Bind(wx.EVT_TOOL, self.OnToolClick)
        commoditiesLayout.Add(tb, 0, wx.ALL|wx.EXPAND, 2)
        tb.Realize()
        
        processesLayout = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Process:"), wx.HORIZONTAL )
        label = wx.StaticText(processesLayout.GetStaticBox(), -1, "Process name:")
        processesLayout.Add(label, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        self._txtProcessName = wx.TextCtrl(processesLayout.GetStaticBox(), size = wx.Size(200, 25))
        self._txtProcessName.Bind(wx.EVT_TEXT, self.TxtProcessOnTextChange)
        processesLayout.Add(self._txtProcessName, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        
        self._btnAddProcess = wx.Button(processesLayout.GetStaticBox(), label="Add Process")
        self._btnAddProcess.Bind(wx.EVT_BUTTON, self.BtnAddOnClick)
        self._btnAddProcess.Disable()
        processesLayout.Add(self._btnAddProcess, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        
        barLayout.Add(commoditiesLayout, 0, wx.ALL, 2)
        barLayout.Add(processesLayout, 0, wx.ALL|wx.EXPAND, 2)
        mainLayout.Add(barLayout, 0, wx.ALL, 2)
        
        ogl.OGLInitialize() 
        self._canvas = ogl.ShapeCanvas(self)
        maxWidth  = 4000
        maxHeight = 2000
        self._canvas.SetScrollbars(20, 20, maxWidth/20, maxHeight/20)
        self._diagram = ogl.Diagram()
        self._canvas.SetDiagram(self._diagram)
        self._diagram.SetCanvas(self._canvas)
        
        mainLayout.Add(self._canvas, 1, wx.ALL|wx.EXPAND, 5)        
        
        self.SetSizer( mainLayout )
        self.Layout()        
        self.Centre( wx.BOTH )
        
        
        pub.subscribe(self.ShapOnDoubleClick, EVENTS.SHAPE_DOUBLE_CLICK)
        pub.subscribe(self.ShapeSelect, EVENTS.SHAPE_SELECTED)
        pub.subscribe(self.ShapeDeselect, EVENTS.SHAPE_DESELECTED)
        
        pub.subscribe(self.CommodityIsAdded, EVENTS.COMMODITY_ADDED)
        pub.subscribe(self.ProcessIsAdded, EVENTS.PROCESS_ADDED)        
        pub.subscribe(self.ConnectionIsAdded, EVENTS.CONNECTION_ADDED)     
        

    def TxtProcessOnTextChange(self, event):
        txt = event.GetEventObject().GetValue()
        if len(txt) > 0:
            self._btnAddProcess.Enable()
        else:
            self._btnAddProcess.Disable()
            
    def BtnAddOnClick(self, event):
        if len(self._txtProcessName.GetValue()) > 0:
            pub.sendMessage(EVENTS.PROCESS_ADDING, processName=self._txtProcessName.GetValue())
    
    def AddShape(self, shape, x, y, pen, brush, text):
        shape.SetDraggable(True, True)
        shape.SetCanvas(self._canvas)
        shape.SetX(x)
        shape.SetY(y)
        if pen:    shape.SetPen(pen)
        if brush:  shape.SetBrush(brush)
        if text:
            for line in text.split(' '):
                shape.AddText(line)
        #shape.SetShadowMode(ogl.SHADOW_RIGHT)
        shape.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.BOLD))
        self._diagram.AddShape(shape)
        shape.Show(True)        

        evthandler = evt.RESEvtHandler()
        evthandler.SetShape(shape)
        evthandler.SetPreviousHandler(shape.GetEventHandler())
        shape.SetEventHandler(evthandler)

        shape.SetId(len(self._shapes) + 1)        
        
        return shape
        
    def OnToolClick(self, event):
       #print("tool %s clicked\n" % event.GetId())
       commType = self._commodityImgs[event.GetId()]['Name']
       pub.sendMessage(EVENTS.COMMODITY_ADDING, commType=commType)
       
    def RefreshCanvas(self):
       dc = wx.ClientDC(self._canvas)
       self._canvas.PrepareDC(dc)
       self._canvas.Redraw(dc)
        
    def CommodityIsAdded(self, commId, commType):
        x, y, shape = 100, 50, None
        shapeList = self._canvas.GetDiagram().GetShapeList()
        if shapeList:
            shape = shapeList[-1]
        if shape:
            x += shape.GetX() + 50
            
        shape = self.AddShape(
            ogl.RectangleShape(130, 65),
            x, y, wx.BLACK_PEN, wx.CYAN_BRUSH, commType
            )
        
        #print(commId)
        self._shapes[shape.GetId()] = {'type': 'commodity', 'uId': commId, 'shape': shape}
        self.RefreshCanvas()
        
    def ProcessIsAdded(self, processId, processName):
        bs = ogl.BitmapShape()
        bs.SetBitmap(wx.Bitmap("./imgs/Process.png"))
        shape = self.AddShape(
            bs, 305, 200, None, None, processName
        )
        
        self._shapes[shape.GetId()] = {'type': 'process', 'uId': processId, 'shape': shape}
        self.RefreshCanvas()
        
    def ShapOnDoubleClick(self, shapeId):        
        shapeType = self._shapes[shapeId]['type']
        if shapeType == 'process':
            #print('Fire PROCESS_EDITING')
            pub.sendMessage(EVENTS.PROCESS_EDITING, processId=self._shapes[shapeId]['uId'])
        elif shapeType == 'commodity':
            #print('Fire COMMODITY_EDITING')
            pub.sendMessage(EVENTS.COMMODITY_EDITING, commId=self._shapes[shapeId]['uId'])
        elif shapeType == 'connection':
            #print('Fire COMMODITY_EDITING')
            pub.sendMessage(EVENTS.CONNECTION_EDITING, connId=self._shapes[shapeId]['uId'])
            
    def ShapeSelect(self, shapeId):
        shapeType = self._shapes[shapeId]['type']
        if shapeType == 'process':
            pub.sendMessage(EVENTS.PROCESS_SELECTED, processId=self._shapes[shapeId]['uId'])
        elif shapeType == 'commodity':
            pub.sendMessage(EVENTS.COMMODITY_SELECTED, commId=self._shapes[shapeId]['uId'])
    
    def ShapeDeselect(self, shapeId):
        shapeType = self._shapes[shapeId]['type']
        if shapeType == 'process':
            pub.sendMessage(EVENTS.PROCESS_DESELECTED, processId=self._shapes[shapeId]['uId'])
        elif shapeType == 'commodity':
            pub.sendMessage(EVENTS.COMMODITY_DESELECTED, commId=self._shapes[shapeId]['uId'])
            
    def GetShapeByUID(self, uId):
        for data in self._shapes.values():
            if data['uId'] == uId:
                return data['shape']
    
    def ConnectionIsAdded(self, direction, connId, commId, processId):
        print("AddConnection: ", direction, connId)
        fromShape, toShape = None, None
        
        if direction == "Inbound":
            fromShape = self.GetShapeByUID(commId)
            toShape = self.GetShapeByUID(processId)
        elif direction == "Outbound":
            fromShape = self.GetShapeByUID(processId)
            toShape = self.GetShapeByUID(commId)
        
        #print(fromShape, toShape)
        canvas = fromShape.GetCanvas()
        line = ogl.LineShape()
        line.SetCanvas(canvas)
        line = self.AddShape(line, 50, 50, wx.BLACK_PEN, wx.BLACK_BRUSH, None)
        line.AddArrow(ogl.ARROW_ARROW)
        line.MakeLineControlPoints(3)
        fromShape.AddLine(line, toShape)
        
        self._shapes[line.GetId()] = {'type': 'connection', 'uId': connId, 'shape': line}
