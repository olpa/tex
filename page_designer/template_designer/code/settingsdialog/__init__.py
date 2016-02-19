#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This module includes subclasses of wxWindow and its enhanced 
functionality to create a settings dialog for the application.

To create the dialog:

from menu.settings import Settings
class myMainFrame(wx.Frame, Settings)
    def __init__(self, parent, safetyMode="viewAccess", *args, **kwargs)
        wx.Frame.__init__(self, parent, *args, **kwargs)
        Settings.__init__(self, *args, **kwargs)

    self.OnSettings()

"""
