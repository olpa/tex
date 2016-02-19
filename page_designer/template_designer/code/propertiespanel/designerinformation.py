#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import xml.etree.ElementTree as ET
from safety import Safety

class designerInformationValidator(wx.PyValidator):
    def __init__(self, parent, message=""):
        wx.PyValidator.__init__(self)

        self.parent = parent
        self.frame = self.parent.GetTopLevelParent()
        self.tree = self.frame.FindWindowByName("dataTree")
        self.item = self.tree.GetSelection()
        self.xml = self.tree.GetItemPyData(self.item)
        self.status = self.parent.status
        self.message = message

        self.Bind(wx.EVT_TEXT, self.OnText)
        self.Bind(wx.EVT_CHAR, self.OnChar)
        self.Bind(wx.EVT_KILL_FOCUS, self.OnKillFocus)

    def OnChar(self, event=None):
        self.frame.OnEdit()
        #set temporary data for possible later saving
        self.TransferFromWindow()
        event.Skip()

    def OnText(self, event=None):
        textCtrl = self.GetWindow()
        if textCtrl.GetName() == "informationName":
            self.tree.SetItemText(self.item, textCtrl.GetValue())
        if textCtrl.GetName() == "informationName" and len(textCtrl.GetValue()) == 0:
            self.status.SetLabel(_(u"Please enter a valid name!"))
            return True
        self.TransferFromWindow()
        self.status.SetLabel("")
        return True

    def OnKillFocus(self, event=None):
        #set temporary data for possible later saving
        self.TransferFromWindow()
        self.Validate()
        return True

    def Clone(self):
         return designerInformationValidator(self.parent, self.message)

    def Validate(self):
        textCtrl = self.GetWindow()
        if textCtrl.GetName() == "informationName" and len(textCtrl.GetValue()) == 0:
            self.status.SetLabel(_(u"Please enter a valid name!"))
            return False
        if self.parent.FindWindowByName("informationStatus"):
            self.parent.FindWindowByName("informationStatus").SetLabel("")
        return True

    def TransferToWindow(self):
        textCtrl = self.GetWindow()
        if textCtrl.GetName() == "informationName":
            textCtrl.SetValue(self.xml.attrib["name"])
        return True

    def TransferFromWindow(self):
        textCtrl = self.GetWindow()
        self.frame.tempItemData[textCtrl.GetName()] = textCtrl.GetValue()
        return True

class designerInformation(wx.Panel):
    def __init__(self, parent, *args, **kwargs):
        wx.Panel.__init__(self, parent, *args, **kwargs)

        self.parent = self.GetTopLevelParent()
        self.tree = self.parent.document
        self.item = self.tree.GetSelection()
        self.xml = self.tree.GetItemPyData(self.item)

        self.staticBox = wx.StaticBox(self, -1, _(u"Information"))

        self.status = wx.StaticText(self, -1, "", name="informationStatus")
        self.status.SetForegroundColour(wx.Color(255,0,0,0))

        self.labelName = wx.StaticText(self, -1, _(u"Name"))
        self.inputName = wx.TextCtrl(self, -1, "", name="informationName")
        self.inputName.SetValidator(designerInformationValidator(self, _(u"Please enter a valid name!")))

        self.__doProperties()
        self.__doLayout()
        self.InitDialog()
        Safety(self)

    def __doProperties(self):
        self.SetName("designerInformationPanel")
        #Set focus to items description
        #This does not work under Python 2.6
        #wx.CallAfter(self.inputName.SetFocus)

    def __doLayout(self):
        staticSizer = wx.StaticBoxSizer(self.staticBox, wx.VERTICAL)
        sizer = wx.BoxSizer(wx.VERTICAL)

        infoSizer = wx.FlexGridSizer(2, 2, 8, 8)
        infoSizer.Add(self.labelName, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        infoSizer.Add(self.inputName, 0, wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 0)
        infoSizer.AddGrowableRow(0)
        infoSizer.AddGrowableCol(1)

        statusSizer = wx.BoxSizer(wx.HORIZONTAL)
        statusSizer.Add(self.status, 1, wx.EXPAND, 0)

        sizer.Add(infoSizer, 1, wx.EXPAND, 0)
        sizer.Add(statusSizer, 0, wx.EXPAND|wx.TOP, 4)

        staticSizer.Add(sizer, 1, wx.EXPAND|wx.ALL, 0)
        self.SetSizerAndFit(staticSizer)
