#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import xml.etree.ElementTree as ET
from safety import Safety

class paperOrientationValidator(wx.PyValidator):
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
         return paperOrientationValidator(self.parent)

    def Validate(self):
        return True

    def TransferToWindow(self):
        textCtrl = self.GetWindow()
        xmlOri = self.xml.findall("{http://www.bitplant.de/template}parameter/{http://www.bitplant.de/template}paper")
        for ori in xmlOri:
            if ori.attrib["type"] == "orientation" and ori.attrib["value"] == "portrait":
                textCtrl.SetSelection(0)
            if ori.attrib["type"] == "orientation" and ori.attrib["value"] == "landscape":
                textCtrl.SetSelection(1)
        return True

    def TransferFromWindow(self):
        textCtrl = self.GetWindow()
        if textCtrl.GetSelection() == 0:
            self.frame.tempItemData["paperOrientation"] = "portrait"
        if textCtrl.GetSelection() == 1:
            self.frame.tempItemData["paperOrientation"] = "landscape"
        return True

class paperOrientation(wx.Panel):
    def __init__(self, parent, *args, **kwargs):
        wx.Panel.__init__(self, parent, *args, **kwargs)

        self.parent = self.GetTopLevelParent()
        self.tree = self.parent.document
        self.item = self.tree.GetSelection()
        self.xml = self.tree.GetItemPyData(self.item)

        self.radio = wx.RadioBox(self, -1, _(u"Orientation"), choices=[_(u"portrait"), _(u"landscape")], majorDimension=2, style=wx.RA_SPECIFY_COLS, name="paperOrientation")
        self.radio.SetValidator(paperOrientationValidator(self))

        self.__doProperties()
        self.__doLayout()
        self.InitDialog()
        Safety(self)

    def __doProperties(self):
        self.SetName("paperOrientationPanel")

    def __doLayout(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.radio, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 0)
        self.SetSizerAndFit(sizer)
