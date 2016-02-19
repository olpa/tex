#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
from __rotatetext import rotateText
import xml.etree.ElementTree as ET
from safety import Safety

class rotationValidator(wx.PyValidator):
    def __init__(self, parent):
        wx.PyValidator.__init__(self)

        self.parent = parent
        self.frame = self.parent.GetTopLevelParent()
        self.tree = self.frame.document
        self.item = self.tree.GetSelection()
        self.xml = self.tree.GetItemPyData(self.item)

        self.Bind(wx.EVT_RADIOBUTTON, self.OnText)

    def OnText(self, event=None):
        self.frame.OnEdit()
        #set temporary data for possible later saving
        self.TransferFromWindow()
        return True

    def Clone(self):
         return rotationValidator(self.parent)

    def Validate(self):
        return True

    def TransferToWindow(self):
        textCtrl = self.GetWindow()
        rot = self.xml.find("{http://www.bitplant.de/template}content")

        if rot.attrib.has_key("angle") == False:
            rot.attrib["angle"] = "0"

        if rot.attrib["angle"] == "0" and textCtrl.GetName() == "contentAngle0":
            textCtrl.SetValue(True)
        if rot.attrib["angle"] == "90" and textCtrl.GetName() == "contentAngle90":
            textCtrl.SetValue(True)
        if rot.attrib["angle"] == "180" and textCtrl.GetName() == "contentAngle180":
            textCtrl.SetValue(True)
        if rot.attrib["angle"] == "270" and textCtrl.GetName() == "contentAngle270":
            textCtrl.SetValue(True)
        return True

    def TransferFromWindow(self):
        textCtrl = self.GetWindow()
        self.frame.tempItemData["contentAngle"] = textCtrl.GetName().lstrip("contentAngle")
        return True

class rotation(wx.Panel):
    def __init__(self, parent, *args, **kwargs):
        wx.Panel.__init__(self, parent, *args, **kwargs)

        self.parent = self.GetTopLevelParent()
        self.tree = self.parent.document
        self.item = self.tree.GetSelection()
        self.xml = self.tree.GetItemPyData(self.item)

        self.staticBox = wx.StaticBox(self, -1, _(u"Rotation"))
        self.topSpin = wx.RadioButton(self, -1, "", name="contentAngle0")
        self.topSpin.SetValidator(rotationValidator(self))
        self.leftSpin = wx.RadioButton(self, -1, "", name="contentAngle270")
        self.leftSpin.SetValidator(rotationValidator(self))
        self.rightSpin = wx.RadioButton(self, -1, "", name="contentAngle90")
        self.rightSpin.SetValidator(rotationValidator(self))
        self.bottomSpin = wx.RadioButton(self, -1, "", name="contentAngle180")
        self.bottomSpin.SetValidator(rotationValidator(self))

        self.__doProperties()
        self.__doLayout()
        self.InitDialog()
        Safety(self)

    def __doProperties(self):
        self.SetName("rotationPanel")

    def __doLayout(self):
        staticSizer = wx.StaticBoxSizer(self.staticBox, wx.VERTICAL)

        sizer = wx.FlexGridSizer(5, 5, 0, 0)

        sizer.Add(wx.Panel(self), 0, wx.EXPAND, 0)
        sizer.Add(wx.Panel(self), 0, wx.EXPAND, 0)
        sizer.Add(rotateText(self, _(u"non-rotated"), 0), 0, wx.ALIGN_CENTER_HORIZONTAL, 0)
        sizer.Add(wx.Panel(self), 0, wx.EXPAND, 0)
        sizer.Add(wx.Panel(self), 0, wx.EXPAND, 0)

        sizer.Add(wx.Panel(self), 0, wx.EXPAND, 0)
        sizer.Add(wx.Panel(self), 0, wx.EXPAND, 0)
        sizer.Add(self.topSpin, 0, wx.ALIGN_TOP|wx.ALIGN_CENTER_HORIZONTAL, 0)
        sizer.Add(wx.Panel(self), 0, wx.EXPAND, 0)
        sizer.Add(wx.Panel(self), 0, wx.EXPAND, 0)

        sizer.Add(rotateText(self, _(u"counter rotated"), 90), 0, wx.ALIGN_CENTER_VERTICAL, 0)
        sizer.Add(self.leftSpin, 0, wx.EXPAND, 0)
        sizer.Add(wx.Panel(self), 0, wx.EXPAND, 0)
        sizer.Add(self.rightSpin, 0, wx.EXPAND, 0)
        sizer.Add(rotateText(self, _(u"clockwise rotated"), 270), 0, wx.ALIGN_CENTER_VERTICAL, 0)

        sizer.Add(wx.Panel(self), 0, wx.EXPAND, 0)
        sizer.Add(wx.Panel(self), 0, wx.EXPAND, 0)
        sizer.Add(self.bottomSpin, 0, wx.ALIGN_BOTTOM|wx.ALIGN_CENTER_HORIZONTAL, 0)
        sizer.Add(wx.Panel(self), 0, wx.EXPAND, 0)
        sizer.Add(wx.Panel(self), 0, wx.EXPAND, 0)

        sizer.Add(wx.Panel(self), 0, wx.EXPAND, 0)
        sizer.Add(wx.Panel(self), 0, wx.EXPAND, 0)
        sizer.Add(rotateText(self, _(u"rotated"), 180), 0, wx.ALIGN_CENTER_HORIZONTAL, 0)
        sizer.Add(wx.Panel(self), 0, wx.EXPAND, 0)
        sizer.Add(wx.Panel(self), 0, wx.EXPAND, 0)

        sizer.AddGrowableCol(2)
        sizer.AddGrowableRow(2)

        staticSizer.Add(sizer, 1, wx.EXPAND|wx.ALL, 8)
        self.SetSizerAndFit(staticSizer)
