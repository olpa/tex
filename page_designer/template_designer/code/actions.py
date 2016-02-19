#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx

class Actions:
    """The Actions class handles some methods which are
    not yet implemented only links to other methods
    
    """
    def __init__(self, *args, **kwargs):
        pass
 
    def OnNew(self, event=None):
        """This is a wrapper to add a new item. This method 
        is intended to be called when the user clicks
        on New from inside the menubar or toolbar

        """
        self.OnAddItem(event=None)

    def OnImport(self, event=None):
        """Not yet implemented
        
        """
        pass

    def OnExport(self, event=None):
        """Not yet implemented
        
        """
        pass

    def __confirmExitDialog(self):
        """Helper Method to show a confirmation dialog 
        on exit if changes appeard to the data
        
        """
        if self.change == True:
            dialog = wx.MessageDialog(None, 
                                      _(u"You modified the data. Do you want to save the modifications before leaving? If you decide no, modifications get lost."),
                                       _(u"Save Modifications?"), 
                                      wx.YES_NO|wx.CANCEL|wx.YES_DEFAULT|wx.ICON_QUESTION)
            decision = dialog.ShowModal()
            if decision == wx.ID_YES:
                self.OnWrite()
                dialog.Destroy()
                return True
            elif decision == wx.ID_NO:
                dialog.Destroy()
                return True
            else:
                dialog.Destroy()
                return False

    def OnExitWindow(self, event=None):
        """OnExitWindow is intendet to close the application properly
        
        """
        if self.__confirmExitDialog() == False:
            return False
        else:
            self.taskBarIcon.RemoveIcon()
            self.taskBarIcon.Destroy()
            self.Destroy()

    def OnCut(self, event=None):
        """Not yet implemented
        
        """
        pass

    def OnCopy(self, event=None):
        """Not yet implemented
        
        """
        pass

    def OnPaste(self, event=None):
        """Not yet implemented
        
        """
        pass

    def OnDateTimeVarTextMenu(self, event=None):
        """Wraps the call of the miniframes which can become required
        after the user wants to use xml contents of type vartext
        
        """
        self.dateTimeMenu(self)
