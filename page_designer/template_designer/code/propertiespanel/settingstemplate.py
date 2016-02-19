#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
from paperorientation import paperOrientation
from paperlayout import paperLayout
from paperformat import paperFormat
from dimension import dimension
from position import position
from safety import Safety

class settingsTemplate(wx.Panel):

    def __init__(self, parent, *args, **kwargs):
        wx.Panel.__init__(self, parent, *args, **kwargs)

        self.parent = self.GetTopLevelParent()
        self.tree = self.parent.document
        self.item = self.tree.GetSelection()
        self.xml = self.tree.GetItemPyData(self.item)

        self.orientation = paperOrientation(self)
        self.layout = paperLayout(self)
        self.format = paperFormat(self)

        self.status = wx.StaticText(self, -1, "", name="dimPosStatus")
        self.status.SetForegroundColour(wx.Color(255,0,0,0))

        self.dimension = dimension(self)
        self.position = position(self)

        self.__doProperties()
        self.__doLayout()
        Safety(self)

    def __doProperties(self):
        self.SetName("settingsTemplatePanel")

    def __doLayout(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        oriLaySizer = wx.BoxSizer(wx.HORIZONTAL)
        marDimSizer = wx.BoxSizer(wx.HORIZONTAL)
        statusSizer = wx.BoxSizer(wx.HORIZONTAL)

        oriLaySizer.Add(self.orientation, 0, wx.EXPAND|wx.TOP|wx.BOTTOM, 8)
        oriLaySizer.Add(self.layout, 0, wx.EXPAND|wx.TOP|wx.BOTTOM|wx.LEFT, 8)

        marDimSizer.Add(self.dimension, 0, wx.EXPAND|wx.TOP|wx.BOTTOM, 8)
        marDimSizer.Add(self.position, 1, wx.EXPAND|wx.TOP|wx.BOTTOM|wx.LEFT, 8)

        statusSizer.Add(self.status, 0, wx.EXPAND|wx.ALL, 4)

        sizer.Add(self.format, 0, 0, 0)
        sizer.Add(oriLaySizer, 0, wx.EXPAND|wx.ALL, 0)
        sizer.Add(marDimSizer, 0, wx.EXPAND|wx.ALL, 0)
        sizer.Add(statusSizer, 0, wx.EXPAND|wx.ALL, 0)

        self.SetSizerAndFit(sizer)
