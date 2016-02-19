#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx

class TemplateDesignerMainSplitter(wx.SplitterWindow):
    """This class is intended to be used inside the main frame
    to split the xml tree and the properties panel
    
    It's original goal was to setup the size of the main frame 
    automatically while changes in the property panel appear
    
    I tried very hard finally I hadn't the time to find a usefull 
    way to to this. At least three wxWindow derived objects are in the 
    game and it seems hard to do this. 
    
    The function OnResize was intended to do this and can be used 
    or overwritten if you found a nice way.
    
    """

    def __init__(self, parent):
        wx.SplitterWindow.__init__(self, parent, style = wx.SP_LIVE_UPDATE)
        self.parent = parent
        self.SetMinimumPaneSize(220)
        self.SetSashPosition(220)
        self.SetSashGravity(0)
        self.__doBindings()

    def __doBindings(self):
        #self.Bind(wx.EVT_SIZE, self.OnReSize)
        self.Bind(wx.EVT_SPLITTER_SASH_POS_CHANGED, self.OnSashChanged)
        self.Bind(wx.EVT_SPLITTER_DCLICK, self.OnDoubleClicked)

    def OnDoubleClicked(self, event=None):
        """OnDoubleClocked is called after the user clicked double
        on the sash of the splitter window
        
        Returns True
        
        """
        if event:
            event.Skip()
        return True

    def OnSashChanged(self, event=None):
        """OnSashChanged is called after the user dragged the sash
        of the splitter Window
        
        Returns True
        
        """
        self.OnResizeFrame(event)
        if event:
            event.Skip()
        return True

    def OnResizeFrame(self, event=None):
        """Originally designed method the resize the main frame 
        automatically if contents a bigger than the current size of 
        the frame, but I had no luck doing this. 
        
        This function does currently nothing expect of returning True
        
        """
        if event:
            event.Skip()
        return True

class MainSplitter:
    """This class is designed to be a subclass of a wxWindow instance
    It adds an instance, called mainSplitter, of type wx.Splitter 
    to the wxWindow instance
    
    """
    def __init__(self, *args, **kwargs):
        self.mainSplitter = TemplateDesignerMainSplitter(self)
