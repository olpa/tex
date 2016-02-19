#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import re
import xml.etree.ElementTree as ET
from colors.x11colorvalues import x11colorValues
from colorsetting import colorSetting
from safety import Safety

class colorUnitValidator(wx.PyValidator):
    def __init__(self, parent):
        wx.PyValidator.__init__(self)

        self.parent = parent
        self.frame = self.parent.GetTopLevelParent()
        self.tree = self.frame.document
        self.item = self.tree.GetSelection()
        self.xml = self.tree.GetItemPyData(self.item)

        self.cmykRe = re.compile( ur"\A(\s*)cmyk(\s*)(\(?)(\s*)([\d]{,3}\s*%?)(\s*,?\s*)([\d]{,3}\s*%?)(\s*,?\s*)([\d]{,3}\s*%?)(\s*,?\s*)([\d]{,3}\s*%?)(\s*)(\)?)(\s*)\Z", re.UNICODE|re.IGNORECASE)
        self.hexRe = re.compile( ur"\A(\s*)#(\s*)(\(?)(\s*)([\da-f]{2}\s*)(\s*,?\s*)([\da-f]{2}\s*)(\s*,?\s*)([\da-f]{2}\s*)(\s*)(\)?)(\s*)\Z", re.UNICODE|re.IGNORECASE)
        self.rgbRe = re.compile( ur"\A(\s*)rgb(\s*)(\(?)(\s*)([\d]{,3}\s*%?)(\s*,?\s*)([\d]{,3}\s*%?)(\s*,?\s*)([\d]{,3}\s*%?)(\s*)(\)?)(\s*)\Z", re.UNICODE|re.IGNORECASE)

        self.Bind(wx.EVT_CHOICE, self.OnText)
        self.Bind(wx.EVT_KILL_FOCUS, self.OnText)

    def setUnit(self):
        textCtrl = self.GetWindow()
        color = colorSetting(self.parent)
        window = ["select", "rgb", "cmyk", "hex"]
        for obj in window:
            self.frame.FindWindowByName("color" + obj.capitalize() + "Panel").Disable()
        if textCtrl.GetSelection() == 0:
            self.frame.FindWindowByName("colorSelectPanel").Enable()
            self.frame.FindWindowByName("colorRgbPanel").Enable()
        elif textCtrl.GetSelection() == 1:
            self.frame.FindWindowByName("colorCmykPanel").Enable()
        elif textCtrl.GetSelection() == 2:
            self.frame.FindWindowByName("colorHexPanel").Enable()

    def OnText(self, event=None):
        self.setUnit()
        self.frame.OnEdit()
        #set temporary data for possible later saving
        self.TransferFromWindow()
        return True

    def Clone(self):
         return colorUnitValidator(self.parent)

    def Validate(self):
        return True

    def TransferToWindow(self):
        textCtrl = self.GetWindow()
        colors = colorSetting(self.parent)
        content = self.xml.find("{http://www.bitplant.de/template}content")
        if re.match(self.rgbRe, content.text):
            textCtrl.SetSelection(0)
        elif re.match(self.cmykRe, content.text):
            textCtrl.SetSelection(1)
        elif re.match(self.hexRe, content.text):
            textCtrl.SetSelection(2)
        colors.setColor(content.text)
        colors.setRgb()
        colors.setHex()
        colors.setCmyk()
        colors.setSelect()
        self.setUnit()
        self.frame.tempItemData["contentType"] = "color"
        return True

    def TransferFromWindow(self):
        textCtrl = self.GetWindow()
        self.frame.tempItemData["text"] = ""
        if textCtrl.GetSelection() == 0:
            self.frame.tempItemData["text"] = self.getRgb()
        elif textCtrl.GetSelection() == 1:
            self.frame.tempItemData["text"] = self.getCmyk()
        elif textCtrl.GetSelection() == 2:
            self.frame.tempItemData["text"] = self.getHex()
        return True

    def getRgb(self):
        rgb = self.frame.FindWindowByName("colorRgbPanel")
        return "rgb(" + str(rgb.rSpin.GetValue()) + ", " + str(rgb.gSpin.GetValue()) + ", " + str(rgb.bSpin.GetValue()) + ")"

    def getCmyk(self):
        cmyk = self.frame.FindWindowByName("colorCmykPanel")
        return "cmyk(" + str(cmyk.cSpin.GetValue()) + ", " + str(cmyk.mSpin.GetValue()) + ", " + str(cmyk.ySpin.GetValue()) + ", "  + str(cmyk.kSpin.GetValue()) + ")"

    def getHex(self):
        hex = self.frame.FindWindowByName("colorHexPanel")
        return "#" + hex.input.GetValue()

class colorUnit(wx.Panel):
    """The color class is derived from wx.Panel and includes 
    the widget to select the desired color space.
    
    """
    def __init__(self, parent, *args, **kwargs):
        wx.Panel.__init__(self, parent, *args, **kwargs)

        self.parent = self.GetTopLevelParent()
        self.tree = self.parent.document
        self.item = self.tree.GetSelection()
        self.xml = self.tree.GetItemPyData(self.item)

        self.label = wx.StaticText(self, -1, _(u"Define input method"))
        self.choice = wx.Choice(self, -1, choices=[_(u"Rgb"), _(u"Cmyk"), _(u"Hex")])
        self.choice.SetValidator(colorUnitValidator(self))

        self.__doProperties()
        self.__doLayout()
        self.InitDialog()
        Safety(self)

    def __doProperties(self):
        self.SetName("colorUnitPanel")

    def __doLayout(self):
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.label, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 8)
        sizer.Add(self.choice, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        self.SetSizerAndFit(sizer)
