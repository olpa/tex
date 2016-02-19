#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
from safety import Safety
from createmenu import CreateMenu

class MenuBar(CreateMenu):

    """
Core functionalities to the menubar. This class contains the menu definitions,
adds them to a menubar and adds the menubar to the classes parent.
The menu is called menuBar
    """

    def __init__(self, *args, **kwargs):
        CreateMenu.__init__(self, *args, **kwargs)
        self.menuBar = wx.MenuBar(wx.MB_DOCKABLE)

    def getMenuBarData(self):
        if self.safetyMode == "fullAccess":
            return [("&File", (
                    (_(u"&New"), _(u"Create new template file"), self.OnNew, "filenew.png", "Ctrl+N"),
                    (_(u"&Save"), _(u"Save current progress to template file"), self.OnWrite, "document_save.png", "Ctrl+S"),
                    ("", "", ""),
                    (_(u"Print Setup..."), _(u"Set up the printer options, etc."), self.OnPrintSetup, "preferences_desktop_printer.png", "F5"),
                    (_(u"Page Setup..."), _(u"Set up the page options, etc."), self.OnPageSetup, "preferences_desktop_printer.png", "F6"),
                    (_(u"Print Preview..."), _(u"View the printout on-screen"), self.OnPrintPreview, "document_print_preview.png", "F7"),
                    (_(u"Print..."), _(u"Print the Template"), self.OnDoPrint, "document_print.png", "F8"),
                    ("", "", ""),
                    (_(u"&Quit"), _(u"Leave the program"), self.OnExitWindow, "application_exit.png", "Ctrl+Q"))),
                (_(u"&Edit"), (
                    (_(u"Remove"), _(u"Remove current selection"), self.OnDeleteItem, "edit_delete.png", "Ctrl+Del"),
                    ("", "", ""),
                    (_(u"&Settings"), _(u"Set up Template-Designer"), self.OnSettings, "configure.png", "F9"))),
                (_(u"&Help"), (
                    (_(u"H&elp"), _(u"Show Help"), self.OnHelp, "help_contents.png", "Ctrl+?"),
                    (_(u"&About"), _(u"Show informations on Template-Designer"), self.OnAbout, "help_about.png", "")))]
        elif self.safetyMode == "restrictedAccess":
            return [("&File", (
                    (_(u"&Save"), _(u"Save current progress to template file"), self.OnWrite, "document_save.png", "Ctrl+S"),
                    ("", "", ""),
                    (_(u"Print Setup..."), _(u"Set up the printer options, etc."), self.OnPrintSetup, "preferences_desktop_printer.png", "F5"),
                    (_(u"Page Setup..."), _(u"Set up the page options, etc."), self.OnPageSetup, "preferences_desktop_printer.png", "F6"),
                    (_(u"Print Preview..."), _(u"View the printout on-screen"), self.OnPrintPreview, "document_print_preview.png", "F7"),
                    (_(u"Print..."), _(u"Print the Template"), self.OnDoPrint, "document_print.png", "F8"),
                    ("", "", ""),
                    (_(u"&Quit"), _(u"Leave the program"), self.OnExitWindow, "application_exit.png", "Ctrl+Q"))),
                (_(u"&Edit"), (
                    ("", "", ""),
                    (_(u"&Settings"), _(u"Set up Template-Designer"), self.OnSettings, "configure.png", "F9"))),
                (_(u"&Help"), (
                    (_(u"H&elp"), _(u"Show Help"), self.OnHelp, "help_contents.png", "Ctrl+?"),
                    (_(u"&About"), _(u"Show informations on Template-Designer"), self.OnAbout, "help_about.png", "")))]
        else:
            return [("&File", (
                    ("", "", ""),
                    (_(u"Print Setup..."), _(u"Set up the printer options, etc."), self.OnPrintSetup, "preferences_desktop_printer.png", "F5"),
                    (_(u"Page Setup..."), _(u"Set up the page options, etc."), self.OnPageSetup, "preferences_desktop_printer.png", "F6"),
                    (_(u"Print Preview..."), _(u"View the printout on-screen"), self.OnPrintPreview, "document_print_preview.png", "F7"),
                    (_(u"Print..."), _(u"Print the Template"), self.OnDoPrint, "document_print.png", "F8"),
                    ("", "", ""),
                    (_(u"&Quit"), _(u"Leave the program"), self.OnExitWindow, "application_exit.png", "Ctrl+Q"))),
                (_(u"&Help"), (
                    (_(u"H&elp"), _(u"Show Help"), self.OnHelp, "help_contents.png", "Ctrl+?"),
                    (_(u"&About"), _(u"Show informations on Template-Designer"), self.OnAbout, "help_about.png", "")))]

    def setMenuBarData(self):
        self.graphics = self.menuBarGraphics()
        for eachMenuData in self.getMenuBarData():
            menuLabel = eachMenuData[0]
            menuItems = eachMenuData[1]
            self.menuBar.Append(self.createMenu(menuItems), menuLabel)
        self.SetMenuBar(self.menuBar)
