#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import xml.etree.ElementTree as ET
import re
from colorsetting import colorSetting
from safety import Safety

class colorHexValidator(wx.PyValidator):
    def __init__(self, parent):
        wx.PyValidator.__init__(self)

        self.parent = parent
        self.frame = self.parent.GetTopLevelParent()
        self.tree = self.frame.document
        self.item = self.tree.GetSelection()
        self.xml = self.tree.GetItemPyData(self.item)

        self.hexRe = re.compile( ur"\A(\s*)#(\s*)(\(?)(\s*)([\da-f]{2}\s*)(\s*,?\s*)([\da-f]{2}\s*)(\s*,?\s*)([\da-f]{2}\s*)(\s*)(\)?)(\s*)\Z", re.UNICODE|re.IGNORECASE)

        self.Bind(wx.EVT_KILL_FOCUS, self.OnKillFocus)
        self.Bind(wx.EVT_CHAR, self.OnText)
        self.Bind(wx.EVT_CHAR_HOOK, self.OnText)
        self.Bind(wx.EVT_TEXT, self.OnTextFocus)

    def OnTextFocus(self, event=None):
        textCtrl = self.GetWindow()
        if textCtrl == self.parent.FindFocus():
            self.OnText(event)

    def setOtherUnits(self):
        colors = colorSetting(self.parent)
        colors.setColor("#" + self.parent.input.GetValue())
        colors.setRgb()
        colors.setCmyk()
        colors.setSelect()

    def OnText(self, event=None):
        self.setOtherUnits()
        self.frame.OnEdit()
        #set temporary data for possible later saving
        self.TransferFromWindow()
        if event:
            event.Skip()

    def OnKillFocus(self, event=None):
        self.setOtherUnits()
        return True

    def Clone(self):
         return colorHexValidator(self.parent)

    def Validate(self):
        return True

    def TransferToWindow(self):
        return True

    def TransferFromWindow(self):
        textCtrl = self.GetWindow()
        choice = self.frame.FindWindowByName("colorUnitPanel").choice
        if choice.GetSelection() == 2:
            rgb = textCtrl.GetValue()
            self.frame.tempItemData["text"] = "#" + self.parent.input.GetValue()
        return True

class colorHex(wx.Panel):

    """
The colorHex class is derived from wx.Panel and includes 
all widgets that handle hex color values.
    """

    def __init__(self, parent, *args, **kwargs):
        wx.Panel.__init__(self, parent, *args, **kwargs)

        self.parent = self.GetTopLevelParent()
        self.tree = self.parent.document
        self.item = self.tree.GetSelection()
        self.xml = self.tree.GetItemPyData(self.item)

        self.staticBox = wx.StaticBox(self, -1, _(u"Hex"))
        self.label = wx.StaticText(self, -1, "#")
        self.input = wx.TextCtrl(self, -1, "000000")
        self.input.SetValidator(colorHexValidator(self))

        self.__doProperties()
        self.__doLayout()
        self.InitDialog()
        Safety(self)

    def __doProperties(self):
        self.SetName("colorHexPanel")

    def __doLayout(self):
        staticSizer = wx.StaticBoxSizer(self.staticBox, wx.VERTICAL)
        gridSizer = wx.FlexGridSizer(1, 2, 0, 0)
        gridSizer.Add(self.label, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        gridSizer.Add(self.input, 0, wx.EXPAND, 0)
        gridSizer.AddGrowableCol(1)
        staticSizer.Add(gridSizer, 1, wx.EXPAND, 0)
        self.SetSizerAndFit(staticSizer)

    def enable(self, bool=True):
        if bool == True:
            self.input.Enable()
        else:
            self.input.Disable()

    def disable(self, bool=True):
        if bool == True:
            self.enable(False)
        else:
            self.enable(True)
