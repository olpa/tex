#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx

from clientpathpanel import ClientPathPanel
from serverpathpanel import ServerPathPanel
from passwordpanel import PasswordPanel
from safety import Safety

class SettingsDialog(wx.Dialog):
    """The class settingsDialog is derived from wx.Dialog and builds 
    a dialog to configure the applications settings

    """
    def __init__(self, parent, id, title):
        wx.Dialog.__init__(self, parent, id, title, size=(600, 250), 
                           style=wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER, 
                           pos=wx.DefaultPosition)

        self.parent = parent
        self.safetyMode = self.parent.safetyMode

        self.OverviewText = wx.StaticText(self, -1, 
                                          _(u"This dialog gives you the possibility to set up Template-Designer. " + \
                                          u"Please take the desired settings."))
        self.okayButton = wx.Button(self, wx.ID_OK, name="settingsOkButton")
        self.okayButton.SetDefault()
        self.okayButton.Disable()
        self.cancelButton = wx.Button(self, wx.ID_CANCEL, 
                                      name="settingsCancelButton")

        self.__doProperties()
        self.__doLayout()
        Safety(self)

    def __doProperties(self):
        self.SetExtraStyle(wx.WS_EX_VALIDATE_RECURSIVELY)
        self.SetName("settingsDialog")
        self.SetMinSize((600, 250))

    def __doLayout(self):
        buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
        buttonSizer.Add(self.okayButton, 0, wx.ALL, 4)
        buttonSizer.Add(self.cancelButton, 0, wx.ALL, 4)

        noteBook = wx.Notebook(self)
        noteBook.AddPage(ClientPathPanel(self, noteBook), _(u"Client Paths"))
        noteBook.AddPage(ServerPathPanel(self, noteBook), _(u"Server Paths"))
        noteBook.AddPage(PasswordPanel(self, noteBook), _(u"Passwords"))

        allSizer = wx.BoxSizer(wx.VERTICAL)
        allSizer.Add(self.OverviewText, 0, wx.EXPAND|wx.ALL, 4)
        allSizer.Add(noteBook, 1, wx.EXPAND|wx.ALL, 4)
        allSizer.Add(wx.StaticLine(self), 0, wx.EXPAND|wx.ALL, 4)
        allSizer.Add(buttonSizer, 0, wx.ALL|wx.ALIGN_RIGHT, 4)

        self.SetSizer(allSizer)
        self.Layout()
        self.CenterOnParent()

class Settings:

    def __init__(self, *args, **kwargs):
        pass

    def OnSettings(self, event=None):
        self.settingsDialog = SettingsDialog(self, -1, _(u"Settings"))
        self.settingsDialog.ShowModal()
        self.settingsDialog.Destroy()

