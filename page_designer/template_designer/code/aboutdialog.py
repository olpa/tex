#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx

class AboutDialog(wx.Dialog):

    def __init__(self, parent, *args, **kwargs):
        icon = wx.Icon(parent.skinGraphics() + "/bitplant.png", wx.BITMAP_TYPE_PNG)

        self.info = wx.AboutDialogInfo()
        self.info.SetIcon(icon)
        self.info.SetName(_(u"Template-Designer"))
        self.info.SetVersion(_(u"0,1"))
        self.info.SetDescription(open("DESCRIPTION").read())
        self.info.SetCopyright(_(u"(C) 2008 Bitplant.de"))
        self.info.SetWebSite(_(u"http://www.bitplant.de"))
        self.info.SetLicence(open("COPYING").read())

        self.info.AddDeveloper(_(u"Alexander Fischer"))
        self.info.AddDeveloper(_(u"Oleg Paraschenko"))
        self.info.AddDocWriter(_(u"Alexander Fischer"))
        self.info.AddArtist("http://www.oxygen-icons.org/")
        #info.AddTranslator("")

class About:

    def __init__(self, *args, **kwargs):
        self.aboutDialog = AboutDialog(self)

    def OnAbout(self, event=None):
            wx.AboutBox(self.aboutDialog.info)

