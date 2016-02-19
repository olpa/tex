#!/usr/bin/env python
# -*- coding: utf-8 -*-

import webbrowser
import os
import sys

class Help:
    def __init__(self, *args, **kwargs):
        #Just do set some valid values
        """
        self.protocol = "http://"
        self.server = "www.bitplant.de"
        self.path = "/template/help"
        self.basename= "/index_en.html"
        """
        self.setHelpTarget()

    def getHelpTarget(self):
        return self.HelpTarget

    def setHelpTarget(self, protocol="file://", 
                      server=os.path.dirname(__file__),
                       path="/content", 
                       basename="/index_en.html"):
        self.HelpTarget = str(protocol + server + path + basename)

    def OnHelp(self, event=None):
        if sys.platform == 'darwin':
            self.__execMacHtml()
        elif sys.platform == 'win32':
            self.__execWinHtml()
        elif sys.platform == 'linux2':
            self.__execLinuxHtml()

    def __execMacHtml(self):
        webbrowser.open_new_tab(self.getHelpTarget())

    def __execWinHtml(self):
        webbrowser.open_new_tab(self.getHelpTarget())

    def __execLinuxHtml(self):
        #This will need spmething like the http://pypi.python.org/pypi/desktop
        #This is not implemented for now to avoid unnecessary dependencies
        webbrowser.open_new_tab(self.getHelpTarget())
