#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import os

class StatusBar:
    """This class is designed to be a subclass of wx.Frame.
    
    It adds an instance statusBar to its parent.
    While calling the function setStatusBarContent, the contents of 
    statusBar become updated.
    
    """
    def __init__(self, *args, **kwargs):
        self.statusBar = self.CreateStatusBar()
        self.statusBar.SetFieldsCount(3)
        self.statusBar.SetStatusWidths([-2, -2, -3])

    def setStatusBarContent(self):
        """Set a textual contents of the statusBar
        
        """
        root = self.document.GetRootItem()
        availableObjects = self.document.GetChildrenCount(root, True) - self.document.GetChildrenCount(root, False)
        self.statusBar.SetStatusText(_(u"Currently available objects: %i" % (availableObjects)) , 0)
        self.statusBar.SetStatusText(_("%s mode") % (self.__formatSafetyMode()), 1)

    def __formatSafetyMode(self):
        """Helper function
        
        Formats the name of the applications 
        safetyMode to write it in the statusbar
        Returns the formatted name
        
        """
        new = str()
        for s in self.safetyMode:
            if s.isupper():
                new += " " + s.lower()
            else:
                new += s
        return new
