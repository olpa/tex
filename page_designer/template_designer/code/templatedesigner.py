#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx

from mainframe import TemplateDesignerFrame
from welcome import TemplateDesignerWelcome
from config import ConfigData

import gettext
trans = gettext.translation(domain="templatedesigner", localedir="i18n", fallback=True) 
trans.install("templatedesigner")

class TemplateDesigner(wx.App, ConfigData):

    def OnInit(self):
        """Called after instantiation
        
        Calls the Splash screen and returns true
        
        """
        ConfigData.__init__(self)
        #self.doSplash()
        self.doMainFrame()
        return True

    def doSplash(self):
        """Show the Splash screen and 
        call the method which handles the welcome dialog

        returns true

        """
        bmp = wx.Image(self.skinGraphics() + "/splash.png").ConvertToBitmap()
        bmpStyle = wx.SPLASH_CENTRE_ON_SCREEN|wx.SPLASH_TIMEOUT
        wx.SplashScreen(bmp, bmpStyle, 1000, None, -1)
        wx.Yield()
        self.doWelcome()
        return True

    def doWelcome(self):
        """Instantiate the welcome dialog and show it
        
        returns True
        
        """
        welcome = TemplateDesignerWelcome(None)
        welcome.CenterOnScreen()
        welcome.SetSizeWH(600, 250)
        welcome.Show(True)
        self.SetTopWindow(welcome)
        return True

    def doMainFrame(self):
        """Call an instance of TemplateDesignerFrame
        
        This method is currently not in use but 
        usefull to tunnel the welcome dialog
        returns True
        
        """
        frame = TemplateDesignerFrame(None, "fullAccess")
        frame.Show(True)
        self.SetTopWindow(frame)
        return True

if __name__ == "__main__":
    app = TemplateDesigner(False)
    app.MainLoop()
