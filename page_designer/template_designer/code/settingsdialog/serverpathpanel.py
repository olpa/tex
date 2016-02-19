#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx

from pathvalidator import PathValidator
from safety import Safety

class ServerPathPanel(wx.Panel):
    """ServerPathPanel builds the panel 
    to configure the client side paths
    
    """
    def __init__(self, parent, noteBook):
        wx.Panel.__init__(self, noteBook)

        self.parent = parent
        self.frame = self.parent.parent

        self.serverTemplateDirLabel = wx.StaticText(self, -1, 
                                                    _(u"Server Templates"))
        self.serverTemplateDirInput = wx.DirPickerCtrl(self, 
                                                       message=_(u"Select the servers template directory"), 
                                                       name="serverTemplates")
        self.serverTemplateDirInput.SetValidator(PathValidator(self.parent, 
                                                               _(u"Please enter a valid server template path!")))
        self.serverTemplateDirInput.SetPath(self.frame.serverTemplates())

        self.serverImageDirLabel = wx.StaticText(self, -1, 
                                                 _(u"Server Images"))
        self.serverImageDirInput = wx.DirPickerCtrl(self, 
                                                    message=(u"Select the servers image directory"), 
                                                    name="serverImages")
        self.serverImageDirInput.SetValidator(PathValidator(self.parent, 
                                                            _(u"Please enter a valid server image path!")))
        self.serverImageDirInput.SetPath(self.frame.serverImages())

        self.__doProperties()
        self.__doLayout()
        Safety(self)

    def __doProperties(self):
        self.SetName("serverPathPanel")

    def __doLayout(self):
        pathSizer = wx.FlexGridSizer(rows=2, cols=2, hgap=0, vgap=0)

        pathSizer.Add(self.serverTemplateDirLabel, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        pathSizer.Add(self.serverTemplateDirInput, 0, wx.EXPAND|wx.ALL, 0)

        pathSizer.Add(self.serverImageDirLabel, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        pathSizer.Add(self.serverImageDirInput, 0, wx.EXPAND|wx.ALL, 0)

        pathSizer.AddGrowableCol(1)
        self.SetSizer(pathSizer)
        self.Layout()
