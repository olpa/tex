#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx

from config import ConfigData
from mykeychain import MyKeyChain
from mainframe import TemplateDesignerFrame

class WelcomeValidator(wx.PyValidator):
    """Validates all widgets of class TemplateDesignerWelcome
    
    The validator checks, of password is required and calls
    class TemplateDesignerFrame if all checks run successfully
    
    """
    def __init__(self, parent):
        wx.PyValidator.__init__(self)

        self.parent = parent
        self.frame = self.parent.GetTopLevelParent()
        self.keychain = MyKeyChain()

        self.Bind(wx.EVT_RADIOBUTTON, self.OnRadio)
        self.Bind(wx.EVT_BUTTON, self.OnButton)
        self.Bind(wx.EVT_TEXT, self.OnText)

    def OnText(self, event=None):
        """Checks if entered password is correct
        
        If password is correct, ok button becomes enabled
        
        """
        textCtrl = self.GetWindow()
        for selection in ["fullAccess", "restrictedAccess", "viewAccess"]:
            radio = self.parent.FindWindowByName(selection)
            compare = self.keychain.comparePassword(selection, textCtrl.GetValue())
            if radio.GetValue() == True and compare == True:
                    self.parent.goButton.Enable()
                    return True
        self.parent.goButton.Disable()

    def OnButton(self, event=None):
        """Calls the class TemplateDesignerFrame if user input is valid
        
        if user input is valid, returns True, else returns False
        
        """
        textCtrl = self.GetWindow()
        if textCtrl.GetName() == "goButton":
            for selection in ["fullAccess", "restrictedAccess", "viewAccess"]:
                radio = self.parent.FindWindowByName(selection)
                pw = self.parent.FindWindowByName("password")
                if pw.IsEnabled() == True and radio.GetValue() == True:
                        compare = self.keychain.comparePassword(selection, pw.GetValue())
                        if compare == True:
                            self.parent.OnExitWindow()
                            frame = TemplateDesignerFrame(None, selection)
                            frame.Show(True)
                elif pw.IsEnabled() == False and radio.GetValue() == True:
                    self.parent.OnExitWindow()
                    frame = TemplateDesignerFrame(None, selection)
                    frame.Show(True)
        return False

    def OnRadio(self, event=None):
        """Enables and Disables the password text 
        control dependend on the system settings
        
        returns True
        
        """
        textCtrl = self.GetWindow()
        for selection in ["fullAccess", "restrictedAccess", "viewAccess"]:
            check = self.keychain.isKey(selection)
            if textCtrl.GetName() == selection and check == True:
                self.parent.FindWindowByName("passwordLabel").Enable()
                self.parent.FindWindowByName("password").Enable()
                self.parent.FindWindowByName("password").SetValue("")
                self.parent.goButton.Disable()
                return True
            elif textCtrl.GetName() == selection and check == False:
                self.parent.FindWindowByName("passwordLabel").Disable()
                self.parent.FindWindowByName("password").Disable()
                self.parent.goButton.Enable()
                return True

    def Clone(self):
         return WelcomeValidator(self.parent)

    def Validate(self):
        return True

    def TransferToWindow(self):
        return True

    def TransferFromWindow(self):
        return True

class TemplateDesignerWelcome(wx.Frame):
    """Generally called by class TemplateDesigner
    
    returns nothing but calls  class TemplateDesignerFrame 
    if user decides not to leave the dialog
    
    """
    def __init__(self, 
                 parent, 
                 style = wx.FULL_REPAINT_ON_RESIZE, 
                 flag = wx.ADJUST_MINSIZE):
        wx.Frame.__init__(self, parent, -1, _(u"Template-Designer"))

        self.myConfig = ConfigData()
        self.myConfig.saveConfig()

        """
        Set taskbar icon. If you remove this, do not forget to 
        remove the RemoveIcon() and Destroy() methods 
        in self.OnExitWindow()
        """
        self.taskBarIcon = wx.TaskBarIcon()
        iconPath = self.myConfig.skinGraphics() + "/domtreeviewer.png"
        icon = wx.Icon(iconPath, wx.BITMAP_TYPE_PNG)
        self.taskBarIcon.SetIcon(icon, _(u"Template-Designer"))

        #Set titlebar icon
        self.SetIcon(icon)

        self.logoPanel = wx.Panel(self, -1)
        self.settingsPanel = wx.Panel(self, -1)

        self.fullRadio = wx.RadioButton(self.settingsPanel,
                                        -1, _(u"Full Access"),
                                        name="fullAccess")
        self.fullRadio.SetValidator(WelcomeValidator(self))

        self.restrictedRadio = wx.RadioButton(self.settingsPanel, 
                                              -1, _(u"Restricted Access"), 
                                              name="restrictedAccess")
        self.restrictedRadio.SetValidator(WelcomeValidator(self))

        self.viewRadio = wx.RadioButton(self.settingsPanel, 
                                        -1, _(u"View available templates"), 
                                        name="viewAccess")
        self.viewRadio.SetValidator(WelcomeValidator(self))

        self.placeholderPanel = wx.Panel(self.settingsPanel, -1)

        self.passwordLabel = wx.StaticText(self.settingsPanel, 
                                           -1, _(u"Password"), 
                                           name="passwordLabel")
        self.passwordTextCtrl = wx.TextCtrl(self.settingsPanel, 
                                            -1, "", 
                                            style=wx.TE_PASSWORD, 
                                            name="password")
        self.passwordTextCtrl.SetValidator(WelcomeValidator(self))

        logo = wx.Bitmap("logo.png", wx.BITMAP_TYPE_ANY)
        self.logoBitmap = wx.StaticBitmap(self.logoPanel, 
                                          -1, 
                                          logo)

        self.staticLine = wx.StaticLine(self, -1)

        self.bitplantLabel = wx.StaticText(self, -1, _(u"Bitplant Template-Designer"))
        self.goButton = wx.Button(self, -1, _(u"OK"), name="goButton")
        self.goButton.SetValidator(WelcomeValidator(self))
        self.exitButton = wx.Button(self, -1, _(u"Exit"), name="exitButton")

        self.__doProperties()
        self.__doBindings()
        self.__doLayout()

    def OnExitWindow(self, event=None):
        """close the Welcome dialog
        
        removes the taskbar icon and destroys the dialog 
        if user clicked the exitButton
        
        """
        self.taskBarIcon.RemoveIcon()
        self.taskBarIcon.Destroy()
        self.Destroy()

    def __doBindings(self):
        self.Bind(wx.EVT_CLOSE, self.OnExitWindow)
        self.Bind(wx.EVT_BUTTON, self.OnExitWindow, self.exitButton)

    def __doProperties(self):
        self.SetTitle(_(u"Bitplant Template-Designer"))
        self.SetMinSize((600, 250))
        white = wx.Colour(255, 255, 255)
        self.logoPanel.SetBackgroundColour(white)
        font = wx.Font(9, wx.SWISS, wx.ITALIC, wx.LIGHT, 0, "")
        self.bitplantLabel.SetFont(font)
        self.goButton.Disable()
        self.passwordLabel.Disable()
        self.passwordTextCtrl.Disable()
        self.restrictedRadio.SetValue(True)

    def __doLayout(self):
        sizerStyle = wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL

        radioSizer = wx.BoxSizer(wx.VERTICAL)
        radioSizer.Add(self.fullRadio, 1, wx.EXPAND, 0)
        radioSizer.Add(self.restrictedRadio, 1, wx.EXPAND, 0)
        radioSizer.Add(self.viewRadio, 1, wx.EXPAND, 0)
        radioSizer.Add(self.placeholderPanel, 2, wx.EXPAND, 0)

        passwordSizer = wx.BoxSizer(wx.HORIZONTAL)
        passwordSizer.Add(self.passwordLabel, 0, wx.RIGHT, 4)
        passwordSizer.Add(self.passwordTextCtrl, 1, 0, 0)

        settingsSizer = wx.BoxSizer(wx.VERTICAL)
        settingsSizer.Add(radioSizer, 1, wx.ALL|wx.EXPAND, 0)
        settingsSizer.Add(passwordSizer, 0, sizerStyle, 4)
        self.settingsPanel.SetSizer(settingsSizer)

        logoSizer = wx.BoxSizer(wx.HORIZONTAL)
        logoSizer.Add(self.logoBitmap, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 24)
        self.logoPanel.SetSizer(logoSizer)

        settingsLogoSizer = wx.BoxSizer(wx.HORIZONTAL)
        settingsLogoSizer.Add(self.settingsPanel, 1, wx.ALL|wx.EXPAND, 4)
        settingsLogoSizer.Add(self.logoPanel, 0, sizerStyle, 0)

        buttonBoxSizer = wx.BoxSizer(wx.HORIZONTAL)
        buttonBoxSizer.Add(self.bitplantLabel, 1, wx.ALL|wx.ALIGN_BOTTOM, 4)
        buttonBoxSizer.Add(self.goButton, 0, wx.ALL, 4)
        buttonBoxSizer.Add(self.exitButton, 0, wx.ALL, 4)

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(settingsLogoSizer, 1, wx.ALL|wx.EXPAND, 0)
        mainSizer.Add(self.staticLine, 0, wx.ALL|wx.EXPAND, 4)
        mainSizer.Add(buttonBoxSizer, 0, wx.ALL|wx.EXPAND, 4)
        self.SetSizer(mainSizer)

        mainSizer.Fit(self)
        self.Layout()
