#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
from information import information
from contenttype import contentType

from position import position
from dimension import dimension

from color import color
from image import image
from rotation import rotation
from text import text
from vartext import vartext
from safety import Safety

class frame(wx.Panel):
    def __init__(self, parent, *args, **kwargs):
        wx.Panel.__init__(self, parent, style=wx.WS_EX_VALIDATE_RECURSIVELY, *args, **kwargs)

        self.parent = self.GetTopLevelParent()
        self.tree = self.parent.document
        self.item = self.tree.GetSelection()
        self.xml = self.tree.GetItemPyData(self.item)

        self.information = information(self)
        self.contentType = contentType(self)

        self.status = wx.StaticText(self, -1, "", name="dimPosStatus")
        self.status.SetForegroundColour(wx.Color(255,0,0,0))

        self.dimension = dimension(self)
        self.position = position(self)

        self.__doProperties()
        self.__doLayout()
        self.InitDialog()
        Safety(self)

    def __doProperties(self):
        #Don't give a name here!
        pass

    def __doLayout(self):
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.marDimSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.statusSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.customSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.sizer.Add(self.information, 0, wx.EXPAND|wx.ALL, 8)
        self.sizer.Add(self.contentType, 0, wx.EXPAND|wx.ALL, 8)

        self.marDimSizer.Add(self.dimension, 0, wx.EXPAND|wx.ALL, 4)
        self.marDimSizer.Add(self.position, 1, wx.EXPAND|wx.ALL, 4)

        self.statusSizer.Add(self.status, 0, wx.EXPAND|wx.ALL, 8)

        self.customSizer.Add(wx.Panel(self, name="customPanel"), 1, wx.EXPAND|wx.ALL, 0)

        self.getType()

        self.sizer.Add(self.marDimSizer, 0, wx.EXPAND|wx.ALL, 4)
        self.sizer.Add(self.statusSizer, 0, wx.EXPAND|wx.ALL, 0)
        self.sizer.Add(self.customSizer, 0, wx.EXPAND|wx.ALL, 4)

        self.SetSizerAndFit(self.sizer)

        self.Layout()
        self.parent.Layout()
        self.parent.propertiesPanel.Layout()

    def getType(self):
        cont = self.xml.find("{http://www.bitplant.de/template}content")
        self.setType(cont.attrib["type"])

    def setType(self, type):

        #Delete old panels
        for i in self.GetChildren():
            if i.GetName() in ["imagePanel", "customPanel", "colorPanel", "rotationPanel", "textPanel", "vartextPanel"]:
                i.Destroy()

        if type == "color":
            self.color = color(self)
            self.customSizer.Add(self.color, 1, wx.EXPAND|wx.ALL, 4)
        if type == "image":
            self.image = image(self)
            self.customSizer.Add(self.image, 1, wx.EXPAND|wx.ALL, 4)
        if type == "text":
            self.rotation = rotation(self)
            self.customSizer.Add(self.rotation, 0, wx.EXPAND|wx.ALL, 4)
            self.text = text(self)
            self.customSizer.Add(self.text, 1, wx.EXPAND|wx.ALL, 4)
        if type == "vartext":
            self.rotation = rotation(self)
            self.customSizer.Add(self.rotation, 0, wx.EXPAND|wx.ALL, 4)
            self.vartext = vartext(self)
            self.customSizer.Add(self.vartext, 1, wx.EXPAND|wx.ALL, 4)

        self.SetSizerAndFit(self.sizer)

        self.Layout()
        self.parent.Layout()
        self.parent.propertiesPanel.Layout()
