#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import wx.gizmos
import datetimetree
from safety import Safety

class dateTimeFrame(wx.MiniFrame):
    def __init__(self, parent, *args, **kwds):
        wx.MiniFrame.__init__(self, parent, -1, _(u"Date/Time Placeholders"), style=wx.ICONIZE|wx.MINIMIZE|wx.MAXIMIZE|wx.CLOSE_BOX|wx.STAY_ON_TOP|wx.DEFAULT_MINIFRAME_STYLE)

        self.parent = parent
        self.frame = self.parent.parent
        self.safetyMode = self.parent.parent.safetyMode

        self.tree = datetimetree.dateTimeTree(self)

        img = wx.Image(self.frame.programGraphics() + "/edit_add.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        self.addButton = wx.BitmapButton(self, -1, img)
        self.Bind(wx.EVT_BUTTON, self.tree.OnActivated, self.addButton)

        img = wx.Image(self.frame.programGraphics() + "/2downarrow.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        self.expandAllButton = wx.BitmapButton(self, -1, img)
        self.Bind(wx.EVT_BUTTON, self.tree.OnExpandAll, self.expandAllButton)

        img = wx.Image(self.frame.programGraphics() + "/2uparrow.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        self.collapseAllButton = wx.BitmapButton(self, -1, img)
        self.Bind(wx.EVT_BUTTON, self.tree.OnCollapseAll, self.collapseAllButton)

        img = wx.Image(self.frame.programGraphics() + "/1uparrow.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        self.collapseAllButCurrentButton = wx.BitmapButton(self, -1, img)
        self.Bind(wx.EVT_BUTTON, self.tree.OnCollapseAllButCurrent, self.collapseAllButCurrentButton)

        self.slider = wx.Slider(self, -1, 255, 0, 255, style=wx.SL_HORIZONTAL)
        self.Bind(wx.EVT_SLIDER, self.OnSlide, self.slider)

        img = wx.Image(self.frame.programGraphics() + "/button_ok.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        self.closeButton = wx.BitmapButton(self, -1, img)
        self.Bind(wx.EVT_BUTTON, self.OnClose, self.closeButton)

        self.__doProperties()
        self.__doLayout()
        self.InitDialog()
        Safety(self)

    def __doProperties(self):
        self.SetName("timeVarMiniFrame")

    def __doLayout(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
        buttonSizer.Add(self.addButton, 0, wx.ALL, 4)
        buttonSizer.Add(self.expandAllButton, 0, wx.ALL, 4)
        buttonSizer.Add(self.collapseAllButton, 0, wx.ALL, 4)
        buttonSizer.Add(self.collapseAllButCurrentButton, 0, wx.ALL, 4)
        buttonSizer.Add(self.slider, 0, wx.ALL|wx.ALIGN_LEFT, 4)
        buttonSizer.Add(wx.Panel(self), 1, wx.ALL, 4)
        buttonSizer.Add(self.closeButton, 0, wx.ALL|wx. ALIGN_RIGHT, 4)

        sizer.Add(self.tree, 1, wx.EXPAND, 0)
        sizer.Add(buttonSizer, 0, wx.EXPAND, 0)
        self.SetSizerAndFit(sizer)

    def OnSlide(self, event=None):
        self.SetTransparent(self.slider.GetValue())

    def OnClose(self, event=None):
        self.Close()
