#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import re
from measureunit import measureUnit
from posdimstatus import posDimStatus
import xml.etree.ElementTree as ET
from safety import Safety

class dimensionValidator(wx.PyValidator):
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
         return dimensionValidator(self.parent)

    def Validate(self):
        posDimStatus(self)
        return True

    def TransferToWindow(self):
        textCtrl = self.GetWindow()
        xmlDim = self.xml.findall("{http://www.bitplant.de/template}parameter/{http://www.bitplant.de/template}dimension")
        mylist = ["0.0", "auto"]
        for dim in xmlDim:
            for pos in ["width", "height"]:
                if textCtrl.GetName() == "dimension" + pos.capitalize():
                    if dim.attrib["type"] == pos:
                        mylist.append(dim.attrib["value"])
                        textCtrl.SetValue(dim.attrib["value"])
        mylist=list(set(mylist))
        mylist.sort()
        textCtrl.SetItems(mylist)
        return True

    def TransferFromWindow(self):
        textCtrl = self.GetWindow()
        REGEXP = re.compile(ur"\d|\.", re.UNICODE|re.IGNORECASE)
        if re.match(REGEXP, textCtrl.GetValue()):
            self.frame.tempItemData[textCtrl.GetName()] = textCtrl.GetValue()
        else:
            self.frame.tempItemData[textCtrl.GetName()] = "auto"
        return True

class dimension(wx.Panel):
    def __init__(self, parent, *args, **kwargs):
        wx.Panel.__init__(self, parent, *args, **kwargs)

        self.parent = self.GetTopLevelParent()
        self.tree = self.parent.document
        self.item = self.tree.GetSelection()
        self.xml = self.tree.GetItemPyData(self.item)

        self.staticBox = wx.StaticBox(self, -1, _(u"Dimensions"))
        self.labelWidth = wx.StaticText(self, -1, _(u"Width"))
        self.spinWidth = wx.ComboBox(self, -1, "", wx.DefaultPosition, (90, -1), style=wx.CB_DROPDOWN, name="dimensionWidth")
        self.spinWidth.SetValue(u"auto")
        self.spinWidth.SetValidator(dimensionValidator(self))
        self.labelHeight = wx.StaticText(self, -1, _(u"Height"))
        self.spinHeight = wx.ComboBox(self, -1, "", wx.DefaultPosition, (90, -1), style=wx.CB_DROPDOWN, name="dimensionHeight")
        self.spinHeight.SetValue(u"auto")
        self.spinHeight.SetValidator(dimensionValidator(self))
        self.unitBox = measureUnit(self)

        self.__doProperties()
        self.__doLayout()
        self.InitDialog()
        Safety(self)

    def __doProperties(self):
        self.SetName("dimensionPanel")

    def __doLayout(self):
        staticSizer = wx.StaticBoxSizer(self.staticBox, wx.VERTICAL)

        sizer = wx.FlexGridSizer(2, 2, 8, 8)
        sizer.Add(self.labelWidth, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        sizer.Add(self.spinWidth, 1,wx.EXPAND, 0)
        sizer.Add(self.labelHeight, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        sizer.Add(self.spinHeight, 1,wx.EXPAND, 0)
        sizer.AddGrowableCol(1)

        staticSizer.Add(self.unitBox, 0, wx.BOTTOM, 8)
        staticSizer.Add(sizer, 1, wx.EXPAND|wx.ALL, 0)
        self.SetSizerAndFit(staticSizer)
