# -*- coding: utf-8 -*-
"""
Created on Wed Oct 31 16:57:58 2018

@author: aelshaha
"""
import wx.lib.ogl as ogl

from Events import EVENTS
from pubsub import pub

class RESEvtHandler(ogl.ShapeEvtHandler):
    
    def __init__(self):
        ogl.ShapeEvtHandler.__init__(self)
        
    def OnLeftDoubleClick(self, x, y, keys=0, attachment=0):
        #print('OnLeftDoubleClick')
        shape = self.GetShape()
        shapeId = shape.GetId();
        pub.sendMessage(EVENTS.ITEM_DOUBLE_CLICK, itemId=shapeId, itemType=shape.GetType())
