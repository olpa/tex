#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx

from colorcmyk import colorCmyk
from colorrgb import colorRgb
from colorhex import colorHex
from colorselect import colorSelect
from colorunit import colorUnit
from safety import Safety

class color(wx.Panel):

    """
The color class includes all widget compositions that handle color values.
    """

    def __init__(self, parent, *args, **kwargs):
        wx.Panel.__init__(self, parent, style=wx.WS_EX_VALIDATE_RECURSIVELY, *args, **kwargs)

        self.parent = self.GetTopLevelParent()
        self.tree = self.parent.document
        self.item = self.tree.GetSelection()
        self.xml = self.tree.GetItemPyData(self.item)

        self.staticBox = wx.StaticBox(self, -1, _(u"Color"))
        self.rgb = colorRgb(self)
        self.hex = colorHex(self)
        self.cmyk = colorCmyk(self)
        self.select = colorSelect(self)
        self.unit = colorUnit(self)

        self.__doProperties()
        self.__doLayout()
        wx.CallAfter(self.InitDialog)
        Safety(self)

    def __doProperties(self):
        self.SetName("colorPanel")

    def __doLayout(self):
        staticSizer = wx.StaticBoxSizer(self.staticBox, wx.VERTICAL)
        staticSizer.Add(self.unit, 0, wx.BOTTOM, 8)
        colorSizer = wx.BoxSizer(wx.HORIZONTAL)
        rgbHexSizer = wx.BoxSizer(wx.VERTICAL)
        rgbHexSizer.Add(self.rgb, 1, wx.EXPAND|wx.ALL, 4)
        rgbHexSizer.Add(self.hex, 0, wx.EXPAND|wx.ALL, 4)

        colorSizer.Add(self.select, 1, wx.EXPAND|wx.ALL, 4)
        colorSizer.Add(rgbHexSizer, 1, wx.EXPAND, 0)
        colorSizer.Add(self.cmyk, 1, wx.EXPAND|wx.ALL, 4)
        staticSizer.Add(colorSizer, 1, wx.EXPAND, 0)

        self.SetSizerAndFit(staticSizer)
