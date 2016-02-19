#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import xml.etree.ElementTree as ET
from safety import Safety

class paperLayoutValidator(wx.PyValidator):
    def __init__(self, parent):
        wx.PyValidator.__init__(self)

        self.parent = parent
        self.frame = self.parent.GetTopLevelParent()
        self.tree = self.frame.document
        self.item = self.tree.GetSelection()
        self.xml = self.tree.GetItemPyData(self.item)

        self.Bind(wx.EVT_RADIOBOX, self.OnText)

    def OnText(self, event=None):
        self.frame.OnEdit()
        #set temporary data for possible later saving
        self.TransferFromWindow()
        return True

    def Clone(self):
         return paperLayoutValidator(self.parent)

    def Validate(self):
        return True

    def TransferToWindow(self):
        textCtrl = self.GetWindow()
        xmlLay = self.xml.findall("{http://www.bitplant.de/template}parameter/{http://www.bitplant.de/template}paper")
        for lay in xmlLay:
            if lay.attrib["type"] == "layout" and lay.attrib["value"] == "oneside":
                textCtrl.SetSelection(0)
            if lay.attrib["type"] == "layout" and lay.attrib["value"] == "twoside":
                textCtrl.SetSelection(1)
        return True

    def TransferFromWindow(self):
        textCtrl = self.GetWindow()
        if textCtrl.GetSelection() == 0:
            self.frame.tempItemData["paperLayout"] = "oneside"
        if textCtrl.GetSelection() == 1:
            self.frame.tempItemData["paperLayout"] = "twoside"
        return True

class paperLayout(wx.Panel):
    def __init__(self, parent, *args, **kwargs):
        wx.Panel.__init__(self, parent, *args, **kwargs)

        self.parent = self.GetTopLevelParent()
        self.tree = self.parent.document
        self.item = self.tree.GetSelection()
        self.xml = self.tree.GetItemPyData(self.item)

        self.radio = wx.RadioBox(self, -1, "Layout", choices=[_(u"one side"), _(u"two side")], majorDimension=2, style=wx.RA_SPECIFY_COLS, name="paperLayout")
        self.radio.SetValidator(paperLayoutValidator(self))

        self.__doProperties()
        self.__doLayout()
        self.InitDialog()
        Safety(self)

    def __doProperties(self):
        self.SetName("paperLayoutPanel")

    def __doLayout(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.radio, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 0)
        self.SetSizerAndFit(sizer)
