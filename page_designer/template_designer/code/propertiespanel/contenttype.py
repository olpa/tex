#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import xml.etree.ElementTree as ET
from safety import Safety

class contentTypeValidator(wx.PyValidator):
    def __init__(self, parent):
        wx.PyValidator.__init__(self)

        self.parent = parent
        self.frame = self.parent.GetTopLevelParent()
        self.tree = self.frame.document
        self.item = self.tree.GetSelection()
        self.xml = self.tree.GetItemPyData(self.item)

        self.Bind(wx.EVT_CHOICE, self.OnChoice)

    def OnChoice(self, event=None):
        textCtrl = self.GetWindow()
        self.frame.OnEdit()
        #set temporary data for possible later saving
        self.TransferFromWindow()

        choice = self.GetWindow()
        frame = self.parent.GetParent()
        #Call the method that en- and disables the required widgets
        if textCtrl.GetSelection() == 0:
            frame.setType("color")
        elif textCtrl.GetSelection() == 1:
            frame.setType("image")
        elif textCtrl.GetSelection() == 2:
            frame.setType("text")
        elif textCtrl.GetSelection() == 3:
            frame.setType("vartext")
        return True

    def Clone(self):
         return contentTypeValidator(self.parent)

    def Validate(self, win):
        return True

    def TransferToWindow(self):
        textCtrl = self.GetWindow()
        cont = self.xml.find("{http://www.bitplant.de/template}content")
        if cont.attrib["type"] == "color":
            textCtrl.SetSelection(0)
        elif cont.attrib["type"] == "image":
            textCtrl.SetSelection(1)
        elif cont.attrib["type"] == "text":
            textCtrl.SetSelection(2)
        elif cont.attrib["type"] == "vartext":
            textCtrl.SetSelection(3)
        return True

    def TransferFromWindow(self):
        textCtrl = self.GetWindow()
        if textCtrl.GetSelection() == 0:
            self.frame.tempItemData["contentType"] = "color"
        elif textCtrl.GetSelection() == 1:
            self.frame.tempItemData["contentType"] = "image"
        elif textCtrl.GetSelection() == 2:
            self.frame.tempItemData["contentType"] = "text"
        elif textCtrl.GetSelection() == 3:
            self.frame.tempItemData["contentType"] = "vartext"
        return True

class contentType(wx.Panel):
    def __init__(self, parent, *args, **kwargs):
        wx.Panel.__init__(self, parent, *args, **kwargs)

        self.parent = self.GetTopLevelParent()
        self.tree = self.parent.document
        self.item = self.tree.GetSelection()
        self.xml = self.tree.GetItemPyData(self.item)

        self.label = wx.StaticText(self, -1, _(u"Define the content type of this frame"))
        self.choice = wx.Choice(self, -1, choices=[_(u"color frame"), _(u"image frame"), _(u"static text frame"), _(u"variable text frame")], name="contentType")
        self.choice.SetValidator(contentTypeValidator(self))

        self.__doProperties()
        self.__doLayout()
        self.InitDialog()
        Safety(self)

    def __doProperties(self):
        self.SetName("contentTypePanel")

    def __doLayout(self):
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.label, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 4)
        sizer.Add(self.choice, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        self.SetSizerAndFit(sizer)
