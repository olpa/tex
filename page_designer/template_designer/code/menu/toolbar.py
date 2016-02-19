#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
from safety import Safety
from createmenu import CreateMenu

class ToolBar(CreateMenu):

    def __init__(self, *args, **kwargs):
        CreateMenu.__init__(self, *args, **kwargs)
        self.toolBar = self.CreateToolBar(wx.TB_DOCKABLE)

    def getToolBarData(self):
        if self.safetyMode == "fullAccess":
            return [(wx.ID_NEW, _(u"New"), "filenew.png", _(u"Create new object"), self.OnNew),
                (wx.ID_DELETE, _(u"Delete"), "edit_delete.png", _(u"Delete object"), self.OnDeleteItem),
                (wx.ID_SAVE, _(u"Save"), "document_save.png", _(u"Save current progress to template file"), self.OnWrite),
                ("", "", "", "", ""),
                (wx.ID_SETUP, _(u"Settings"), "configure.png", _(u"Set up Template-Designer"), self.OnSettings),
                ("", "", "", "", ""),
                (wx.ID_PREVIEW, _(u"Print Preview"), "document_print_preview.png", _(u"Show a preview"), self.OnPrintPreview),
                ("", "", "", "", ""),
                (wx.ID_HELP, _(u"Help"), "help_contents.png", _(u"Show Help"), self.OnHelp),
                (wx.ID_ABOUT, _(u"About"), "help_about.png", _(u"Show informations on Template-Designer"), self.OnAbout),
                ("", "", "", "", ""),
                (wx.ID_EXIT, _(u"Quit"), "application_exit.png", _(u"Leave the program"), self.OnExitWindow)]

        elif self.safetyMode == "restrictedAccess":
            return [(wx.ID_SAVE, _(u"Save"), "document_save.png", _(u"Save current progress to template file"), self.OnWrite),
                ("", "", "", "", ""),
                (wx.ID_SETUP, _(u"Settings"), "configure.png", _(u"Set up Template-Designer"), self.OnSettings),
                ("", "", "", "", ""),
                (wx.ID_PREVIEW, _(u"Print Preview"), "document_print_preview.png", _(u"Show a preview"), self.OnPrintPreview),
                ("", "", "", "", ""),
                (wx.ID_HELP, _(u"Help"), "help_contents.png", _(u"Show Help"), self.OnHelp),
                (wx.ID_ABOUT, _(u"About"), "help_about.png", _(u"Show informations on Template-Designer"), self.OnAbout),
                ("", "", "", "", ""),
                (wx.ID_EXIT, _(u"Quit"), "application_exit.png", _(u"Leave the program"), self.OnExitWindow)]

        else:
            return [(wx.ID_PREVIEW, _(u"Print Preview"), "document_print_preview.png", _(u"Show a preview"), self.OnPrintPreview),
                ("", "", "", "", ""),
                (wx.ID_HELP, _(u"Help"), "help_contents.png", _(u"Show Help"), self.OnHelp),
                (wx.ID_ABOUT, _(u"About"), "help_about.png", _(u"Show informations on Template-Designer"), self.OnAbout),
                ("", "", "", "", ""),
                (wx.ID_EXIT, _(u"Quit"), "application_exit.png", _(u"Leave the program"), self.OnExitWindow)]

    def setToolBarData(self):
        for each in self.getToolBarData():
            self.__createSimpleTool(*each)
        self.toolBar.AddSeparator()
        self.toolBar.Realize()
        self.toolBar.EnableTool(wx.ID_SAVE, False)

    def __createSimpleTool(self, id, label, filename, help, handler):
        if not label:
            self.toolBar.AddSeparator()
            return True
        self.graphics = self.toolBarGraphics()
        bmp = wx.Image(self.toolBarGraphics() + "/" + filename, wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        tool = self.toolBar.AddSimpleTool(id, bmp, label, help)
        self.Bind(wx.EVT_MENU, handler, tool)
