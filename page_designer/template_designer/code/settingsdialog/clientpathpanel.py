#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx

from pathvalidator import PathValidator
from safety import Safety

class ClientPathPanel(wx.Panel):
    """ClientPathPanel builds the panel 
    to configure the client side paths
    
    """
    def __init__(self, parent, noteBook):
        wx.Panel.__init__(self, noteBook)

        self.parent = parent
        self.frame = self.parent.parent

        self.clientTemplateDirLabel = wx.StaticText(self, -1, 
                                                    _(u"Client Templates"))
        self.clientTemplateDirInput = wx.DirPickerCtrl(self, 
                                                       message=_(u"Select the clients template directory"), 
                                                       name="clientTemplates")
        self.clientTemplateDirInput.SetValidator(PathValidator(self.parent, 
                                                               _(u"Please enter a valid client template path!")))
        self.clientTemplateDirInput.SetPath(self.frame.clientTemplates())

        self.clientImageDirLabel = wx.StaticText(self, -1, 
                                                 _(u"Client Images"))
        self.clientImageDirInput = wx.DirPickerCtrl(self, 
                                                    message=_(u"Select the clients image directory"), 
                                                    name="clientImages")
        self.clientImageDirInput.SetValidator(PathValidator(self.parent, 
                                                            _(u"Please enter a valid client image path!")))
        self.clientImageDirInput.SetPath(self.frame.clientImages())

        self.__doProperties()
        self.__doLayout()
        Safety(self)

    def __doProperties(self):
        self.SetName("clientPathPanel")

    def __doLayout(self):
        pathSizer = wx.FlexGridSizer(rows=4, cols=2, hgap=0, vgap=0)

        pathSizer.Add(self.clientTemplateDirLabel, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        pathSizer.Add(self.clientTemplateDirInput, 0, wx.EXPAND|wx.ALL, 0)

        pathSizer.Add(self.clientImageDirLabel, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        pathSizer.Add(self.clientImageDirInput, 0, wx.EXPAND|wx.ALL, 0)

        pathSizer.AddGrowableCol(1)
        self.SetSizer(pathSizer)
        self.Layout()
