#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import  wx.lib.colourselect as  CS
import xml.etree.ElementTree as ET
import re
from colorsetting import colorSetting
from safety import Safety

class colorSelectValidator(wx.PyValidator):
    def __init__(self, parent):
        wx.PyValidator.__init__(self)

        self.parent = parent
        self.frame = self.parent.GetTopLevelParent()
        self.tree = self.frame.document
        self.item = self.tree.GetSelection()
        self.xml = self.tree.GetItemPyData(self.item)

        self.rgbRe = re.compile( ur"\A(\s*)rgb(\s*)(\(?)(\s*)([\d]{,3}\s*%?)(\s*,?\s*)([\d]{,3}\s*%?)(\s*,?\s*)([\d]{,3}\s*%?)(\s*)(\)?)(\s*)\Z", re.UNICODE|re.IGNORECASE)
        self.hexRe = re.compile( ur"\A(\s*)#(\s*)(\(?)(\s*)([\da-f]{2}\s*)(\s*,?\s*)([\da-f]{2}\s*)(\s*,?\s*)([\da-f]{2}\s*)(\s*)(\)?)(\s*)\Z", re.UNICODE|re.IGNORECASE)

        self.Bind(wx.EVT_KILL_FOCUS, self.OnKillFocus)
        self.Bind(CS.EVT_COLOURSELECT, self.OnText)

    def setOtherUnits(self):
        textCtrl = self.GetWindow()
        rgb = textCtrl.GetValue()
        colors = colorSetting(self.parent)
        colors.setColor("rgb(" + str(rgb[0]) + ", " + str(rgb[1]) + ", " + str(rgb[2]) + ")")
        colors.setRgb()
        colors.setCmyk()
        colors.setHex()

    def OnText(self, event=None):
        self.setOtherUnits()
        self.frame.OnEdit()
        #set temporary data for possible later saving
        self.TransferFromWindow()
        event.Skip()

    def OnKillFocus(self, event=None):
        self.setOtherUnits()
        return True

    def Clone(self):
         return colorSelectValidator(self.parent)

    def Validate(self):
        return True

    def TransferToWindow(self):
        return True

    def TransferFromWindow(self):
        textCtrl = self.GetWindow()
        choice = self.frame.FindWindowByName("colorUnitPanel").choice
        if choice.GetSelection() == 0:
            rgb = textCtrl.GetValue()
            self.frame.tempItemData["text"] = "rgb(" + str(rgb[0]) + ", " + str(rgb[1]) + ", " + str(rgb[2]) + ")"
        return True

class colorSelect(wx.Panel):

    """
The colorSelect class includes a drop down list to activate the systems default color chooser.
    """

    def __init__(self, parent, *args, **kwargs):
        wx.Panel.__init__(self, parent, *args, **kwargs)

        self.parent = self.GetTopLevelParent()
        self.tree = self.parent.document
        self.item = self.tree.GetSelection()
        self.xml = self.tree.GetItemPyData(self.item)

        self.staticBox = wx.StaticBox(self, -1, "Select")
        self.color = CS.ColourSelect(self, -1, label=_(u"Select color"))
        self.color.SetValidator(colorSelectValidator(self))

        self.__doProperties()
        self.__doLayout()
        self.InitDialog()
        Safety(self)

    def __doProperties(self):
        self.SetName("colorSelectPanel")

    def __doLayout(self):
        staticSizer = wx.StaticBoxSizer(self.staticBox, wx.VERTICAL)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.color, 1, wx.EXPAND, 0)
        staticSizer.Add(sizer, 1, wx.EXPAND, 0)
        self.SetSizerAndFit(staticSizer)
