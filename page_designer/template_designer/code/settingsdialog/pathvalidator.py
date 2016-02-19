#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx

class PathValidator(wx.PyValidator):
    """This class acts as validator to the server and client values, 
    the user is able to set in the dialog created by instance of 
    class settingsDialog
    
    """
    def __init__(self, parent, message=_(u"Please enter a valid path!")):
        wx.PyValidator.__init__(self)

        self.parent = parent
        self.frame = self.parent.parent
        self.message = message

        self.Bind(wx.EVT_DIRPICKER_CHANGED, self.OnChar)

    def OnChar(self, evt):
        self.parent.okayButton.Enable()
        evt.Skip()

    def Clone(self):
         return PathValidator(self.parent, self.message)

    def Validate(self, win):
        if len(self.GetWindow().GetPath()) == 0:
            wx.MessageBox(self.message, _(u"Error"))
            self.GetWindow().SetFocus()
            self.GetWindow().Refresh()
            return False

        if self.GetWindow().GetName() == "clientTemplates":
            self.frame.setOption("templates", 
                                  "clientTemplates", 
                                  self.GetWindow().GetPath())
        elif self.GetWindow().GetName() == "clientImages":
            self.frame.setOption("templates", 
                                  "clientImages", 
                                  self.GetWindow().GetPath())
        elif self.GetWindow().GetName() == "serverTemplates":
            self.frame.setOption("templates", 
                                  "serverTemplates", 
                                  self.GetWindow().GetPath())
        elif self.GetWindow().GetName() == "serverImages":
            self.frame.setOption("templates", 
                                  "serverImages", 
                                  self.GetWindow().GetPath())
        else:
            print _(u"Internal error while saving template path of type %s") % self.type
        self.frame.saveConfig()
        return True

    def TransferToWindow(self):
        return True

    def TransferFromWindow(self):
        return True
