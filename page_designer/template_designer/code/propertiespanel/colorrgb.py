#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import xml.etree.ElementTree as ET
import re
from colorsetting import colorSetting
from safety import Safety

class colorRgbValidator(wx.PyValidator):
    def __init__(self, parent):
        wx.PyValidator.__init__(self)

        self.parent = parent
        self.frame = self.parent.GetTopLevelParent()
        self.tree = self.frame.document
        self.item = self.tree.GetSelection()
        self.xml = self.tree.GetItemPyData(self.item)

        self.rgbRe = re.compile( ur"\A(\s*)rgb(\s*)(\(?)(\s*)([\d]{,3}\s*%?)(\s*,?\s*)([\d]{,3}\s*%?)(\s*,?\s*)([\d]{,3}\s*%?)(\s*)(\)?)(\s*)\Z", re.UNICODE|re.IGNORECASE)

        self.Bind(wx.EVT_KILL_FOCUS, self.OnKillFocus)
        self.Bind(wx.EVT_SPINCTRL, self.OnText)
        self.Bind(wx.EVT_CHAR, self.OnText)

    def setOtherUnits(self):
        color = colorSetting(self.parent)
        color.setColor("rgb(" + str(self.parent.rSpin.GetValue()) + ", " + str(self.parent.gSpin.GetValue()) + ", " + str(self.parent.bSpin.GetValue()) + ")")
        color.setCmyk()
        color.setHex()
        color.setSelect()

    def OnText(self, event=None):
        self.setOtherUnits()
        self.frame.OnEdit()
        #set temporary data for possible later saving
        self.TransferFromWindow()
        return True

    def OnKillFocus(self, event=None):
        self.setOtherUnits()
        return True

    def Clone(self):
         return colorRgbValidator(self.parent)

    def Validate(self):
        return True

    def TransferToWindow(self):
        return True

    def TransferFromWindow(self):
        textCtrl = self.GetWindow()
        choice = self.frame.FindWindowByName("colorUnitPanel").choice
        if choice.GetSelection() == 0:
            self.frame.tempItemData["text"] = "rgb(" + str(self.parent.rSpin.GetValue()) + ", " + str(self.parent.gSpin.GetValue()) + ", " + str(self.parent.bSpin.GetValue()) + ")"
        return True

class colorRgb(wx.Panel):

    """
The colorRgb class is derived from wx.Panel and includes 
all widgets that handle rgb color values.
    """

    def __init__(self, parent, *args, **kwargs):
        wx.Panel.__init__(self, parent, *args, **kwargs)

        self.parent = self.GetTopLevelParent()
        self.tree = self.parent.document
        self.item = self.tree.GetSelection()
        self.xml = self.tree.GetItemPyData(self.item)

        self.staticBox = wx.StaticBox(self, -1, _(u"Rgb"))
        self.rLabel = wx.StaticText(self, -1, _(u"R"))
        self.rSpin = wx.SpinCtrl(self, -1, "0", min=0, max=255, name="rColor")
        self.rSpin.SetValidator(colorRgbValidator(self))
        self.gLabel = wx.StaticText(self, -1, _(u"G"))
        self.gSpin = wx.SpinCtrl(self, -1, "0", min=0, max=255, name="gColor")
        self.gSpin.SetValidator(colorRgbValidator(self))
        self.bLabel = wx.StaticText(self, -1, _(u"B"))
        self.bSpin = wx.SpinCtrl(self, -1, "0", min=0, max=255, name="bColor")
        self.bSpin.SetValidator(colorRgbValidator(self))

        self.__doProperties()
        self.__doLayout()
        self.InitDialog()
        Safety(self)

    def __doProperties(self):
        self.SetName("colorRgbPanel")

    def __doLayout(self):
        staticSizer = wx.StaticBoxSizer(self.staticBox, wx.VERTICAL)
        gridSizer = wx.FlexGridSizer(3, 2, 0, 0)
        gridSizer.Add(self.rLabel, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        gridSizer.Add(self.rSpin, 0, wx.EXPAND, 0)
        gridSizer.Add(self.gLabel, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        gridSizer.Add(self.gSpin, 0, wx.EXPAND, 0)
        gridSizer.Add(self.bLabel, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        gridSizer.Add(self.bSpin, 0, wx.EXPAND, 0)
        gridSizer.AddGrowableCol(1)
        staticSizer.Add(gridSizer, 1, wx.EXPAND, 0)
        self.SetSizerAndFit(staticSizer)
