#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
from information import information
from inheritance import inheritance
from settingstemplate import settingsTemplate
from safety import Safety

class page(wx.Panel):
    def __init__(self, parent, *args, **kwargs):
        wx.Panel.__init__(self, parent, *args, **kwargs)
        self.parent = self.GetTopLevelParent()
        self.tree = self.parent.document
        self.item = self.tree.GetSelection()
        self.xml = self.tree.GetItemPyData(self.item)

        self.information = information(self)
        self.settings = settingsTemplate(self)
        self.inheritance = inheritance(self)

        self.__doProperties()
        self.__doLayout()
        Safety(self)

    def __doProperties(self):
        #Don't give a name here!
        pass

    def __doLayout(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.information, 0, wx.EXPAND|wx.ALL, 8)
        sizer.Add(self.inheritance, 0, wx.EXPAND|wx.ALL, 8)
        sizer.Add(self.settings, 1, wx.EXPAND|wx.ALL, 8)
        self.SetSizerAndFit(sizer)

        self.Layout()
        self.parent.Layout()
        self.parent.propertiesPanel.Layout()
