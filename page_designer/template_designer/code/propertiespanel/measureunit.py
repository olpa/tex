#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import xml.etree.ElementTree as ET
from safety import Safety

class measureUnitValidator(wx.PyValidator):
    def __init__(self, parent):
        wx.PyValidator.__init__(self)

        self.parent = parent
        self.frame = self.parent.GetTopLevelParent()
        self.tree = self.frame.document
        self.item = self.tree.GetSelection()
        self.xml = self.tree.GetItemPyData(self.item)

        self.Bind(wx.EVT_CHOICE, self.OnText)
        self.Bind(wx.EVT_SET_FOCUS, self.OnText)

    def OnText(self, event=None):
        self.frame.OnEdit()
        #set temporary data for possible later saving
        self.TransferFromWindow()
        return True

    def Clone(self):
         return measureUnitValidator(self.parent)

    def Validate(self):
        return True

    def TransferToWindow(self):
        """
        The next code seems unlogical and it is but it is not.
        The Xml requires a own unit for every given value.
        The following code tries to take care on that, 
        although there is only one widget to set the base unit 
        and it is currently useless while import of data.
        If you decide to use a own base unit to every value, change only 
        the textCtrl.GetName() comparison to the required name.
        """
        if self.parent.GetParent().GetName() == "positionPanel":
            self.__transferToPositionWindow()
        elif self.parent.GetParent().GetName() == "dimensionPanel":
            self.__transferToDimensionWindow()
        return True

    def __transferToPositionWindow(self):
        textCtrl = self.GetWindow()
        xmlUnit = self.xml.findall("{http://www.bitplant.de/template}parameter/{http://www.bitplant.de/template}position")
        for unit in xmlUnit:
            if unit.attrib["type"] == "top" and textCtrl.GetName() == "measureUnit":
                textCtrl.SetStringSelection(str(unit.attrib["unit"]))
            if unit.attrib["type"] == "left" and textCtrl.GetName() == "measureUnit":
                textCtrl.SetStringSelection(str(unit.attrib["unit"]))
            if unit.attrib["type"] == "right" and textCtrl.GetName() == "measureUnit":
                textCtrl.SetStringSelection(str(unit.attrib["unit"]))
            if unit.attrib["type"] == "bottom" and textCtrl.GetName() == "measureUnit":
                textCtrl.SetStringSelection(str(unit.attrib["unit"]))

    def __transferToDimensionWindow(self):
        textCtrl = self.GetWindow()
        xmlUnit = self.xml.findall("{http://www.bitplant.de/template}parameter/{http://www.bitplant.de/template}dimension")
        for unit in xmlUnit:
            if unit.attrib["type"] == "width" and textCtrl.GetName() == "measureUnit":
                textCtrl.SetStringSelection(str(unit.attrib["unit"]))
            if unit.attrib["type"] == "height" and textCtrl.GetName() == "measureUnit":
                textCtrl.SetStringSelection(str(unit.attrib["unit"]))

    def TransferFromWindow(self):
        if self.parent.GetParent().GetName() == "positionPanel":
            self.__transferFromPositionWindow()
        elif self.parent.GetParent().GetName() == "dimensionPanel":
            self.__transferFromDimensionWindow()

    def __transferFromPositionWindow(self):
        textCtrl = self.GetWindow()
        self.frame.tempItemData["positionTopUnit"] = textCtrl.GetStringSelection()
        self.frame.tempItemData["positionLeftUnit"] = textCtrl.GetStringSelection()
        self.frame.tempItemData["positionRightUnit"] = textCtrl.GetStringSelection()
        self.frame.tempItemData["positionBottomUnit"] = textCtrl.GetStringSelection()
        return True

    def __transferFromDimensionWindow(self):
        textCtrl = self.GetWindow()
        self.frame.tempItemData["dimensionWidthUnit"] = textCtrl.GetStringSelection()
        self.frame.tempItemData["dimensionHeightUnit"] = textCtrl.GetStringSelection()
        return True

class measureUnit(wx.Panel):
    def __init__(self, parent, *args, **kwargs):
        wx.Panel.__init__(self, parent, *args, **kwargs)

        self.parent = self.GetTopLevelParent()
        self.tree = self.parent.document
        self.item = self.tree.GetSelection()
        self.xml = self.tree.GetItemPyData(self.item)

        self.label = wx.StaticText(self, -1, _(u"Base unit"))
        self.choice = wx.Choice(self, -1, choices=[_(u"mm"), _(u"cm"), _(u"inch"), _(u"point")], name="measureUnit")
        self.choice.SetValidator(measureUnitValidator(self))

        self.__doProperties()
        self.__doLayout()
        self.InitDialog()
        Safety(self)

    def __doProperties(self):
        self.SetName("measureUnitPanel")

    def __doLayout(self):
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.label, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 4)
        sizer.Add(self.choice, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        self.SetSizerAndFit(sizer)
