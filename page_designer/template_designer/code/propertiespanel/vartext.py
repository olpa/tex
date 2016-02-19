
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import documentframe
import datetimeframe
import xml.etree.ElementTree as ET
from safety import Safety

class vartextValidator(wx.PyValidator):
    def __init__(self, parent, message=""):
        wx.PyValidator.__init__(self)

        self.parent = parent
        self.frame = self.parent.GetTopLevelParent()
        self.tree = self.frame.document
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
        if textCtrl.GetName() == "vartext" and len(textCtrl.GetValue()) == 0:
            self.status.SetLabel(_(u"Please enter some text!"))
            return True
        self.TransferFromWindow()
        self.status.SetLabel("")
        return True

    def OnKillFocus(self, event=None):
        #set temporary data for possible later saving
        self.TransferFromWindow()
        self.Validate()

    def Clone(self):
         return vartextValidator(self.parent, self.message)

    def Validate(self):
        textCtrl = self.GetWindow()
        if textCtrl.GetName() == "vartext" and len(textCtrl.GetValue()) == 0:
            self.status.SetLabel(_(u"Please enter some text!"))
            return False
        self.status.SetLabel("")
        return True

    def TransferToWindow(self):
        textCtrl = self.GetWindow()
        if textCtrl.GetName() == "vartext":
            xmlVar = self.xml.find("{http://www.bitplant.de/template}content")
            textCtrl.SetValue(xmlVar.text)
        self.frame.tempItemData["contentType"] = "vartext"
        return True

    def TransferFromWindow(self):
        textCtrl = self.GetWindow()
        self.frame.tempItemData["text"] = textCtrl.GetValue()
        return True

class vartext(wx.Panel):
    def __init__(self, parent, *args, **kwargs):
        wx.Panel.__init__(self, parent, *args, **kwargs)

        self.parent = self.GetTopLevelParent()
        self.tree = self.parent.document
        self.item = self.tree.GetSelection()
        self.xml = self.tree.GetItemPyData(self.item)

        self.staticBox = wx.StaticBox(self, -1, _(u"Contents"))

        self.status = wx.StaticText(self, -1, "")
        self.status.SetForegroundColour(wx.Color(255,0,0,0))

        self.text = wx.TextCtrl(self, -1, "", style=wx.TE_MULTILINE|wx.TE_NO_VSCROLL, name="vartext")
        self.text.SetValidator(vartextValidator(self, _(u"Please enter some text!")))
        self.dateButton = wx.Button(self, -1, _(u"Date/Time"))
        self.Bind(wx.EVT_BUTTON, self.OnDateButton, self.dateButton)
        self.documentButton = wx.Button(self, -1, _(u"Document"))
        self.Bind(wx.EVT_BUTTON, self.OnDocumentButton, self.documentButton)

        self.__doProperties()
        self.__doLayout()
        self.InitDialog()
        Safety(self)

    def __doProperties(self):
        self.SetName("vartextPanel")

    def OnDateButton(self, event=None):
        miniframe = datetimeframe.dateTimeFrame(self)
        miniframe.Show()
        return True

    def OnDocumentButton(self, event=None):
        miniframe = documentframe.documentFrame(self)
        miniframe.Show()
        return True

    def __doLayout(self):
        staticSizer = wx.StaticBoxSizer(self.staticBox, wx.VERTICAL)
        sizer = wx.BoxSizer(wx.VERTICAL)
        buttonSizer = wx.BoxSizer(wx.HORIZONTAL)

        buttonSizer.Add(self.dateButton, 0, wx.ALL, 4)
        buttonSizer.Add(self.documentButton, 0, wx.ALL, 4)

        sizer.Add(self.text, 1, wx.EXPAND, 0)
        sizer.Add(buttonSizer, 0, wx.EXPAND, 0)
        sizer.Add(self.status, 0, wx.EXPAND, 0)

        staticSizer.Add(sizer, 1, wx.EXPAND|wx.ALL, 0)
        self.SetSizerAndFit(staticSizer)
