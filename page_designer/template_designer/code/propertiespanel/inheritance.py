#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import xml.etree.ElementTree as ET
from safety import Safety

class inheritanceValidator(wx.PyValidator):
    def __init__(self, parent):
        wx.PyValidator.__init__(self)

        self.parent = parent
        self.frame = self.parent.GetTopLevelParent()
        self.tree = self.frame.document
        self.item = self.tree.GetSelection()
        self.xml = self.tree.GetItemPyData(self.item)

        self.Bind(wx.EVT_CHECKBOX, self.OnText)
        self.Bind(wx.EVT_KILL_FOCUS, self.OnText)

    def setInheritance(self):
        textCtrl = self.GetWindow()
        if textCtrl.GetValue() == True:
            self.frame.FindWindowByName("settingsTemplatePanel").Enable()
        else:
            self.frame.FindWindowByName("settingsTemplatePanel").Disable()

    def OnText(self, event=None):
        self.setInheritance()
        self.frame.OnEdit()
        #set temporary data for possible later saving
        self.TransferFromWindow()
        return True

    def Clone(self):
         return inheritanceValidator(self.parent)

    def Validate(self):
        return True

    def TransferToWindow(self):
        textCtrl = self.GetWindow()
        if self.xml.attrib.has_key("inherit") == False:
            self.xml.attrib["inherit"] = "enable"
        if self.xml.attrib["inherit"] == "enable":
            textCtrl.SetValue(False)
        if self.xml.attrib["inherit"] == "disable":
            textCtrl.SetValue(True)
        self.setInheritance()
        return True

    def TransferFromWindow(self):
        textCtrl = self.GetWindow()
        self.frame.tempItemData[textCtrl.GetName()] = textCtrl.GetValue()
        return True

class inheritance(wx.Panel):
    def __init__(self, parent, *args, **kwargs):
        wx.Panel.__init__(self, parent, *args, **kwargs)

        self.parent = self.GetTopLevelParent()
        self.tree = self.parent.document
        self.item = self.tree.GetSelection()
        self.xml = self.tree.GetItemPyData(self.item)

        self.inheritance = wx.CheckBox(self, -1, _(u"Disable inheritance of the template settings"), name="inheritance")
        self.inheritance.SetValidator(inheritanceValidator(self))

        self.__doProperties()
        self.__doLayout()
        self.InitDialog()
        Safety(self)

    def __doProperties(self):
        self.SetName("inheritancePanel")

    def __doLayout(self):
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer.Add(self.inheritance, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        self.SetSizerAndFit(self.sizer)
