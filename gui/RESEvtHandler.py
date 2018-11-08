# -*- coding: utf-8 -*-
"""
Created on Wed Oct 31 16:57:58 2018

@author: aelshaha
"""
import wx
import wx.lib.ogl as ogl

from Events import EVENTS
from pubsub import pub

class RESEvtHandler(ogl.ShapeEvtHandler):
    
    def __init__(self):
        ogl.ShapeEvtHandler.__init__(self)

    def UpdateStatusBar(self, shape):
        canvas = shape.GetCanvas()
        dc = wx.ClientDC(canvas)
        canvas.PrepareDC(dc)
        canvas.Redraw(dc)
        canvas.Refresh(False)
        return


    def OnLeftClick(self, x, y, keys=0, attachment=0):
        #print('OnLeftClick')
        shape = self.GetShape()
        canvas = shape.GetCanvas()
        dc = wx.ClientDC(canvas)
        canvas.PrepareDC(dc)

        if shape.Selected():
            #print('Deselect!')
            shape.Select(False, dc)
            #canvas.Redraw(dc)
            canvas.Refresh(False)
            pub.sendMessage(EVENTS.SHAPE_DESELECTED, shapeId=shape.GetId())
        else:            
            #print('Select a shape!')
            shapeList = canvas.GetDiagram().GetShapeList()
            toUnselect = []

            for s in shapeList:
                if s.Selected():
                    # If we unselect it now then some of the objects in
                    # shapeList will become invalid (the control points are
                    # shapes too!) and bad things will happen...
                    toUnselect.append(s)

            shape.Select(True, dc)
            pub.sendMessage(EVENTS.SHAPE_SELECTED, shapeId=shape.GetId())
            
            if toUnselect:
                for s in toUnselect:
                    s.Select(False, dc)

                ##canvas.Redraw(dc)
                canvas.Refresh(False)

        self.UpdateStatusBar(shape)
    
    def OnLeftDoubleClick(self, x, y, keys=0, attachment=0):
        #print('OnLeftDoubleClick')
        shape = self.GetShape()
        shapeId = shape.GetId();
        pub.sendMessage(EVENTS.SHAPE_DOUBLE_CLICK, shapeId=shapeId)
        

    def OnSizingEndDragLeft(self, pt, x, y, keys, attch):
        #print('OnSizingEndDragLeft')
        ogl.ShapeEvtHandler.OnSizingEndDragLeft(self, pt, x, y, keys, attch)
        self.UpdateStatusBar(self.GetShape())
