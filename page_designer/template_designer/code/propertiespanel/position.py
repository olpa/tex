#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import re
from measureunit import measureUnit
from posdimstatus import posDimStatus
import xml.etree.ElementTree as ET
from safety import Safety

class positionValidator(wx.PyValidator):
    def __init__(self, parent):
        wx.PyValidator.__init__(self)

        self.parent = parent
        self.frame = self.parent.GetTopLevelParent()
        self.tree = self.frame.document
        self.item = self.tree.GetSelection()
        self.xml = self.tree.GetItemPyData(self.item)

        self.Bind(wx.EVT_KILL_FOCUS, self.OnKillFocus)
        self.Bind(wx.EVT_COMBOBOX, self.OnText)
        self.Bind(wx.EVT_TEXT, self.OnText)
        self.Bind(wx.EVT_TEXT_ENTER, self.OnText)
        self.Bind(wx.EVT_CHAR, self.OnChar)
        self.Bind(wx.EVT_CHAR_HOOK, self.OnChar)

    def OnChar(self, event=None):
        posDimStatus(self)
        key = chr(event.GetKeyCode())
        REGEXP = re.compile( ur"\d|\.|auto", re.UNICODE|re.IGNORECASE)
        if re.match(REGEXP, key) or event.GetKeyCode() in (8, 127):
            event.Skip()
        return

    def OnText(self, event=None):
        posDimStatus(self)
        self.frame.OnEdit()
        #set temporary data for possible later saving
        self.TransferFromWindow()
        return True

    def OnKillFocus(self, event=None):
        posDimStatus(self)
        return True

    def Clone(self):
         return positionValidator(self.parent)

    def Validate(self):
        posDimStatus(self)
        return True

    def TransferToWindow(self):
        textCtrl = self.GetWindow()
        xmlMar = self.xml.findall("{http://www.bitplant.de/template}parameter/{http://www.bitplant.de/template}position")
        mylist = ["0.0", "auto"]
        for mar in xmlMar:
            for pos in ["top", "left", "right", "bottom"]:
                if textCtrl.GetName() == "position" + pos.capitalize():
                    if mar.attrib["type"] == pos:
                        mylist.append(mar.attrib["value"])
                        textCtrl.SetValue(mar.attrib["value"])
        mylist=list(set(mylist))
        mylist.sort()
        textCtrl.SetItems(mylist)
        return True

    def TransferFromWindow(self):
        textCtrl = self.GetWindow()
        REGEXP = re.compile( ur"\d|\.|auto", re.UNICODE|re.IGNORECASE)
        if re.match(REGEXP, textCtrl.GetValue()):
            self.frame.tempItemData[textCtrl.GetName()] = textCtrl.GetValue()
        else:
            self.frame.tempItemData[textCtrl.GetName()] = "auto"
        return True

class position(wx.Panel):
    def __init__(self, parent, *args, **kwargs):
        wx.Panel.__init__(self, parent, *args, **kwargs)

        self.parent = self.GetTopLevelParent()
        self.tree = self.parent.document
        self.item = self.tree.GetSelection()
        self.xml = self.tree.GetItemPyData(self.item)

        self.staticBox = wx.StaticBox(self, -1, _(u"Position"))

        self.topLabel = wx.StaticText(self, -1, _(u"top"))
        self.topSpin = wx.ComboBox(self, -1, "", wx.DefaultPosition, (90, -1), style=wx.CB_DROPDOWN, name="positionTop")
        self.topSpin.SetValue(u"auto")
        self.topSpin.SetValidator(positionValidator(self))
        self.leftLabel = wx.StaticText(self, -1, _(u"left"))
        self.leftSpin = wx.ComboBox(self, -1, "", wx.DefaultPosition, (90, -1), style=wx.CB_DROPDOWN, name="positionLeft")
        self.leftSpin.SetValue(u"auto")
        self.leftSpin.SetValidator(positionValidator(self))
        self.rightLabel = wx.StaticText(self, -1, _(u"right"))
        self.rightSpin = wx.ComboBox(self, -1, "", wx.DefaultPosition, (90, -1), style=wx.CB_DROPDOWN, name="positionRight")
        self.rightSpin.SetValue(u"auto")
        self.rightSpin.SetValidator(positionValidator(self))
        self.bottomLabel = wx.StaticText(self, -1, _(u"bottom"))
        self.bottomSpin = wx.ComboBox(self, -1, "", wx.DefaultPosition, (90, -1), style=wx.CB_DROPDOWN, name="positionBottom")
        self.bottomSpin.SetValue(u"auto")
        self.bottomSpin.SetValidator(positionValidator(self))
        self.unitBox = measureUnit(self)

        self.__doProperties()
        self.__doLayout()
        self.InitDialog()
        Safety(self)

    def __doProperties(self):
        self.SetName("positionPanel")

    def __doLayout(self):
        staticSizer = wx.StaticBoxSizer(self.staticBox, wx.VERTICAL)
        sizer = wx.FlexGridSizer(5, 5, 0, 0)

        sizer.Add(wx.Panel(self), 0, wx.EXPAND, 0)
        sizer.Add(wx.Panel(self), 0, wx.EXPAND, 0)
        sizer.Add(self.topLabel, 0, wx.ALIGN_BOTTOM, 0)
        sizer.Add(wx.Panel(self), 0, wx.EXPAND, 0)
        sizer.Add(wx.Panel(self), 0, wx.EXPAND, 0)

        sizer.Add(wx.Panel(self), 0, wx.EXPAND, 0)
        sizer.Add(wx.Panel(self), 0, wx.EXPAND, 0)
        sizer.Add(self.topSpin, 0, 0, 0)
        sizer.Add(wx.Panel(self), 0, wx.EXPAND, 0)
        sizer.Add(wx.Panel(self), 0, wx.EXPAND, 0)

        sizer.Add(self.leftLabel, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 0)
        sizer.Add(self.leftSpin, 0, 0, 0)
        sizer.Add(wx.Panel(self), 0, wx.EXPAND, 0)
        sizer.Add(self.rightSpin, 0, wx.ALIGN_RIGHT, 0)
        sizer.Add(self.rightLabel, 0, wx.ALIGN_CENTER_VERTICAL, 0)

        sizer.Add(wx.Panel(self), 0, wx.EXPAND, 0)
        sizer.Add(wx.Panel(self), 0, wx.EXPAND, 0)
        sizer.Add(self.bottomSpin, 0, 0, 0)
        sizer.Add(wx.Panel(self), 0, wx.EXPAND, 0)
        sizer.Add(wx.Panel(self), 0, wx.EXPAND, 0)

        sizer.Add(wx.Panel(self), 0, wx.EXPAND, 0)
        sizer.Add(wx.Panel(self), 0, wx.EXPAND, 0)
        sizer.Add(self.bottomLabel, 0, 0, 0)
        sizer.Add(wx.Panel(self), 0, wx.EXPAND, 0)
        sizer.Add(wx.Panel(self), 0, wx.EXPAND, 0)

        sizer.AddGrowableCol(4)

        staticSizer.Add(self.unitBox, 0, wx.BOTTOM, 8)
        staticSizer.Add(sizer, 1, wx.EXPAND|wx.ALL, 0)
        self.SetSizerAndFit(staticSizer)
