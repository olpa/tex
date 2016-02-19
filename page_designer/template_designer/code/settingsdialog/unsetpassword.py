#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx

from mykeychain import MyKeyChain
from safety import Safety

class UnsetPasswordValidator(wx.PyValidator):
    def __init__(self, parent):
        wx.PyValidator.__init__(self)

        self.parent = parent
        self.frame = self.parent.GetTopLevelParent()
        self.keychain = MyKeyChain()
        self.type = self.getType()

        self.Bind(wx.EVT_TEXT, self.OnText)

    def camelize(self, type):
        return str(type[0].lower() + type[1:])

    def getType(self):
        if self.parent.type[:3] == "set":
            return self.camelize(self.parent.type[3:])
        else:
            return self.camelize(self.parent.type[5:])

    def OnText(self, event=None):
        old = self.parent.FindWindowByName("oldPassword")
        if self.keychain.isKey(self.type) == True:
            if self.keychain.comparePassword(self.type, old.GetValue()) == True:
                    self.parent.FindWindowByName("goButton").Enable()
                    return True
        self.parent.FindWindowByName("goButton").Disable()
        return False

    def Clone(self):
         return UnsetPasswordValidator(self.parent)

    def Validate(self, event=None):
        return True

    def TransferToWindow(self):
        textCtrl = self.GetWindow()
        if self.keychain.isKey(self.type) == False:
            self.parent.FindWindowByName("oldPasswordLabel").Disable()
            self.parent.FindWindowByName("oldPassword").Disable()

    def TransferFromWindow(self):
        if self.OnText() == True:
            if self.keychain.isKey(self.type) == True:
                self.keychain.removePassword(self.type)
        return True

class UnsetPassword(wx.Dialog):
    """UnsetPassword builds the dialog where the user is able 
    to unset or modify a password
    
    """
    def __init__(self, parent, title, type):
        wx.Dialog.__init__(self, parent, -1, title, 
                           size=(600, 250), 
                           style=wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER)

        self.parent = parent
        self.frame = self.parent.parent.parent
        self.title = title
        self.type = type

        self.logoPanel = wx.Panel(self, -1)
        self.settingsPanel = wx.Panel(self, -1)

        self.description = wx.StaticText(self, -1, 
                                         _(u"This dialog gives you the opportunity to " + title.lower()))

        self.oldLabel = wx.StaticText(self, -1, _(u"Old password"))
        self.oldInput = wx.TextCtrl(self, -1, "", 
                                    style=wx.TE_PASSWORD, 
                                    name="oldPassword")
        self.oldInput.SetValidator(UnsetPasswordValidator(self))

        self.placeholderPanel = wx.Panel(self.settingsPanel, -1)

        logo = wx.Bitmap(self.frame.skinGraphics() + "/kgpg_key1_kgpg.png", wx.BITMAP_TYPE_PNG)
        self.logoBitmap = wx.StaticBitmap(self.logoPanel, -1, logo)
        self.staticLine = wx.StaticLine(self, -1)

        self.goButton = wx.Button(self, wx.ID_OK, _(u"OK"), name="goButton")
        self.goButton.SetValidator(UnsetPasswordValidator(self))
        self.exitButton = wx.Button(self, wx.ID_CANCEL, _(u"Cancel"), name="cancelButton")

        self.__doProperties()
        self.__doLayout()
        Safety(self.frame)

    def __doProperties(self):
        self.SetTitle(self.title)
        self.SetMinSize((600, 250))
        self.CenterOnParent()
        self.logoPanel.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.goButton.Disable()

    def __doLayout(self):
        sizerStyle = wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL

        passwordSizer = wx.FlexGridSizer(1, 2, 0, 0)
        passwordSizer.Add(self.oldLabel, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 4)
        passwordSizer.Add(self.oldInput, 1, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 4)
        passwordSizer.AddGrowableCol(1)

        settingsSizer = wx.BoxSizer(wx.VERTICAL)
        settingsSizer.Add(self.description, 0, wx.ALL|wx.EXPAND, 4)
        settingsSizer.Add(passwordSizer, 0, sizerStyle, 4)
        settingsSizer.Add(self.placeholderPanel, 1, wx.ALL|wx.EXPAND, 4)

        self.settingsPanel.SetSizer(settingsSizer)

        logoSizer = wx.BoxSizer(wx.HORIZONTAL)
        logoSizer.Add(self.logoBitmap, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 24)
        self.logoPanel.SetSizer(logoSizer)

        settingsLogoSizer = wx.BoxSizer(wx.HORIZONTAL)
        settingsLogoSizer.Add(self.settingsPanel, 1, wx.ALL|wx.EXPAND, 4)
        settingsLogoSizer.Add(self.logoPanel, 0, sizerStyle, 0)

        buttonBoxSizer = wx.BoxSizer(wx.HORIZONTAL)
        buttonBoxSizer.Add(self.goButton, 0, wx.ALL|wx.ALIGN_RIGHT, 4)
        buttonBoxSizer.Add(self.exitButton, 0, wx.ALL|wx.ALIGN_RIGHT, 4)

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(settingsLogoSizer, 1, wx.ALL|wx.EXPAND, 0)
        mainSizer.Add(self.staticLine, 0, wx.ALL|wx.EXPAND, 4)
        mainSizer.Add(buttonBoxSizer, 0, wx.ALL|wx.ALIGN_RIGHT, 4)
        self.SetSizer(mainSizer)

        mainSizer.Fit(self)
        self.Layout()
