#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx

from setpassword import SetPassword
from unsetpassword import UnsetPassword
from mykeychain import MyKeyChain
from safety import Safety

class PasswordValidator(wx.PyValidator):
    """This class acts as validator to the values, the user 
    is able to set in the dialog created by class settingsDialog
    """
    def __init__(self, parent):
        wx.PyValidator.__init__(self)

        self.parent = parent
        self.frame = parent.frame
        self.keychain = MyKeyChain()

        self.Bind(wx.EVT_BUTTON, self.OnButton)

    def OnButton(self, event=None):
        textCtrl = self.GetWindow()
        setOptions = {
        "setFullAccess": "Set the full access password",
        "setRestrictedAccess": "Set the restricted access password",
        "setViewAccess": "Set the view access password",
        "unsetFullAccess": "Unset the full access password",
        "unsetRestrictedAccess": "Unset the restricted access password",
        "unsetViewAccess": "Unset the view access password"
        }
        for type, title in setOptions.iteritems():
            if textCtrl.GetName() == type:
                if type[:2] == "un":
                    dialog = UnsetPassword(self.parent, title, textCtrl.GetName())
                else:
                    dialog = SetPassword(self.parent, title, textCtrl.GetName())
                result = dialog.ShowModal()
                if result == wx.ID_OK:
                    self.parent.parent.FindWindowByName("settingsCancelButton").Disable()
                    self.parent.parent.FindWindowByName("settingsOkButton").Enable()
                dialog.Destroy()
        return True

    def Clone(self):
         return PasswordValidator(self.parent)

    def Validate(self, win):
        return True

    def TransferToWindow(self):
        textCtrl = self.GetWindow()
        if self.getType(textCtrl.GetName()) != None:
            if self.keychain.isKey(self.getType(textCtrl.GetName())) == False:
                textCtrl.Disable()
        return True

    def camelize(self, type):
        return str(type[0].lower() + type[1:])

    def getType(self, type):
        if type[:5] == "unset":
            return self.camelize(type[5:])
        else:
            return None

    def TransferFromWindow(self):
        return True

class PasswordPanel(wx.Panel):
    """PasswordPanel builds the panel to configure the access to 
    the application and the corresponding keychain
    
    """
    def __init__(self, parent, noteBook):
        wx.Panel.__init__(self, noteBook)

        self.parent = parent
        self.frame = self.parent.parent

        self.fullAccessLabel = wx.StaticText(self, -1, 
                                             _(u"Full access password"))
        self.fullAccessSet = wx.Button(self, -1, 
                                       _(u"Set"), 
                                       name="setFullAccess")
        self.fullAccessSet.SetValidator(PasswordValidator(self))
        self.fullAccessUnset = wx.Button(self, -1, 
                                         _(u"Unset"), 
                                         name="unsetFullAccess")
        self.fullAccessUnset.SetValidator(PasswordValidator(self))

        self.restrictedAccessLabel = wx.StaticText(self, -1, 
                                                   _(u"Restricted access password"))
        self.restrictedAccessSet = wx.Button(self, -1, 
                                             _(u"Set"), 
                                             name="setRestrictedAccess")
        self.restrictedAccessSet.SetValidator(PasswordValidator(self))
        self.restrictedAccessUnset = wx.Button(self, -1, 
                                               _(u"Unset"), 
                                               name="unsetRestrictedAccess")
        self.restrictedAccessUnset.SetValidator(PasswordValidator(self))

        self.viewAccessLabel = wx.StaticText(self, -1, 
                                             _(u"View access password"))
        self.viewAccessSet = wx.Button(self, -1, 
                                       _(u"Set"), 
                                       name="setViewAccess")
        self.viewAccessSet.SetValidator(PasswordValidator(self))
        self.viewAccessUnset = wx.Button(self, -1, 
                                         _(u"Unset"), 
                                         name="unsetViewAccess")
        self.viewAccessUnset.SetValidator(PasswordValidator(self))

        self.__doProperties()
        self.__doLayout()
        Safety(self)

    def __doProperties(self):
        self.SetName("passwordPanel")

    def __doLayout(self):
        accessSizer = wx.FlexGridSizer(rows=3, cols=3, hgap=4, vgap=4)

        accessSizer.Add(self.fullAccessLabel, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        accessSizer.Add(self.fullAccessSet, 0, wx.ALL, 0)
        accessSizer.Add(self.fullAccessUnset, 0, wx.ALL, 0)

        accessSizer.Add(self.restrictedAccessLabel, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        accessSizer.Add(self.restrictedAccessSet, 0, wx.ALL, 0)
        accessSizer.Add(self.restrictedAccessUnset, 0, wx.ALL, 0)

        accessSizer.Add(self.viewAccessLabel, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        accessSizer.Add(self.viewAccessSet, 0, wx.ALL, 0)
        accessSizer.Add(self.viewAccessUnset, 0, wx.ALL, 0)

        accessSizer.AddGrowableCol(2)
        self.SetSizer(accessSizer)
        self.Layout()
