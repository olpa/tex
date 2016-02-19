#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import xml.etree.ElementTree as ET
import re
from colorsetting import colorSetting
from safety import Safety

class colorCmykValidator(wx.PyValidator):
    def __init__(self, parent):
        wx.PyValidator.__init__(self)

        self.parent = parent
        self.frame = self.parent.GetTopLevelParent()
        self.tree = self.frame.document
        self.item = self.tree.GetSelection()
        self.xml = self.tree.GetItemPyData(self.item)

        self.cmykRe = re.compile( ur"\A(\s*)cmyk(\s*)(\(?)(\s*)([\d]{,3}\s*%?)(\s*,?\s*)([\d]{,3}\s*%?)(\s*,?\s*)([\d]{,3}\s*%?)(\s*,?\s*)([\d]{,3}\s*%?)(\s*)(\)?)(\s*)\Z", re.UNICODE|re.IGNORECASE)

        self.Bind(wx.EVT_KILL_FOCUS, self.OnKillFocus)
        self.Bind(wx.EVT_SPINCTRL, self.OnText)
        self.Bind(wx.EVT_CHAR, self.OnText)

    def setOtherUnits(self):
        colors = colorSetting(self.parent)
        colors.setColor("cmyk(" + str(self.parent.cSpin.GetValue()) + ", " + str(self.parent.mSpin.GetValue()) + ", " + str(self.parent.ySpin.GetValue()) +", " + str(self.parent.kSpin.GetValue()) + ")")
        colors.setRgb()
        colors.setHex()
        colors.setSelect()

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
         return colorCmykValidator(self.parent)

    def Validate(self):
        return True

    def TransferToWindow(self):
        return True

    def TransferFromWindow(self):
        textCtrl = self.GetWindow()
        choice = self.frame.FindWindowByName("colorUnitPanel").choice
        if choice.GetSelection() == 1:
            self.frame.tempItemData["text"] = "cmyk(" + str(self.parent.cSpin.GetValue()) + ", " + str(self.parent.mSpin.GetValue()) + ", " + str(self.parent.ySpin.GetValue()) +", " + str(self.parent.kSpin.GetValue()) + ")"
        return True

class colorCmyk(wx.Panel):
    """The colorCmyk class is derived from wx.Panel and includes 
    all widgets that handle cmyk color values.
    
    """
    def __init__(self, parent, *args, **kwargs):
        wx.Panel.__init__(self, parent, *args, **kwargs)

        self.parent = self.GetTopLevelParent()
        self.tree = self.parent.document
        self.item = self.tree.GetSelection()
        self.xml = self.tree.GetItemPyData(self.item)

        self.staticBox = wx.StaticBox(self, -1, _(u"Cmyk"))
        self.cLabel = wx.StaticText(self, -1, _(u"C"))
        self.cSpin = wx.SpinCtrl(self, -1, "0", min=0, max=255, name="cColor")
        self.cSpin.SetValidator(colorCmykValidator(self))
        self.mLabel = wx.StaticText(self, -1, _(u"M"))
        self.mSpin = wx.SpinCtrl(self, -1, "0", min=0, max=255, name="mColor")
        self.mSpin.SetValidator(colorCmykValidator(self))
        self.yLabel = wx.StaticText(self, -1, _(u"Y"))
        self.ySpin = wx.SpinCtrl(self, -1, "0", min=0, max=255, name="yColor")
        self.ySpin.SetValidator(colorCmykValidator(self))
        self.kLabel = wx.StaticText(self, -1, _(u"K"))
        self.kSpin = wx.SpinCtrl(self, -1, "255", min=0, max=255, name="kColor")
        self.kSpin.SetValidator(colorCmykValidator(self))

        self.__doProperties()
        self.__doLayout()
        self.InitDialog()
        Safety(self)

    def __doProperties(self):
        self.SetName("colorCmykPanel")

    def __doLayout(self):
        self.staticSizer = wx.StaticBoxSizer(self.staticBox, wx.VERTICAL)
        self.gridSizer = wx.FlexGridSizer(4, 2, 0, 0)
        self.gridSizer.Add(self.cLabel, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        self.gridSizer.Add(self.cSpin, 0, wx.EXPAND, 0)
        self.gridSizer.Add(self.mLabel, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        self.gridSizer.Add(self.mSpin, 0, wx.EXPAND, 0)
        self.gridSizer.Add(self.yLabel, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        self.gridSizer.Add(self.ySpin, 0, wx.EXPAND, 0)
        self.gridSizer.Add(self.kLabel, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        self.gridSizer.Add(self.kSpin, 0, wx.EXPAND, 0)
        self.gridSizer.AddGrowableCol(1)
        self.staticSizer.Add(self.gridSizer, 1, wx.EXPAND, 0)
        self.SetSizerAndFit(self.staticSizer)

    def enable(self, bool=True):
        if bool == True:
            self.cSpin.Enable()
            self.mSpin.Enable()
            self.ySpin.Enable()
            self.kSpin.Enable()
        else:
            self.cSpin.Disable()
            self.mSpin.Disable()
            self.ySpin.Disable()
            self.kSpin.Disable()

    def disable(self, bool=True):
        if bool == True:
            self.enable(False)
        else:
            self.enable(True)
