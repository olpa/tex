#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
from designerinformation import designerInformation
from safety import Safety

class designer(wx.Panel):
    def __init__(self, parent, *args, **kwargs):
        wx.Panel.__init__(self, parent, *args, **kwargs)

        self.parent = self.GetTopLevelParent()
        self.tree = self.parent.document
        self.item = self.tree.GetSelection()
        self.xml = self.tree.GetItemPyData(self.item)

        self.information = designerInformation(self)

        self.__doProperties()
        self.__doLayout()
        self.InitDialog()
        Safety(self)

    def __doProperties(self):
        #Don't give a name here!
        pass

    def __doLayout(self):
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.information, 0, wx.EXPAND|wx.ALL, 8)
        self.SetSizerAndFit(self.sizer)

        self.Layout()
        self.parent.Layout()
        self.parent.propertiesPanel.Layout()