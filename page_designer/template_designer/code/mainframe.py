#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx

from menu.menubar import MenuBar
from menu.toolbar import ToolBar
from menu.treecontextmenu import TreeContextMenu
from statusbar import StatusBar

from actions import Actions
from printing.printing import Printing
from config import ConfigData
from help.help import Help

from mainsplitter import MainSplitter
from settingsdialog.settings import Settings
from aboutdialog import About

from data.document import Document
from data.getdata import GetData
from data.viewdata import ViewData
from data.editdata import EditData

import propertiespanel as pp
from safety import Safety

class TemplateDesignerFrame(wx.Frame, ConfigData, StatusBar, MenuBar, 
                            ToolBar, TreeContextMenu, Actions, Printing,
                            Help, About, Settings, MainSplitter, 
                            Document, GetData, ViewData, EditData):
    """wx.Frame instance which includes all 
    widgets for productive use of the application
    
    """

    def __init__(self, parent, safetyMode="viewAccess", *args, **kwargs):
        wx.Frame.__init__(self, parent, *args, **kwargs)
        self.safetyMode = safetyMode
        ConfigData.__init__(self, *args, **kwargs)
        StatusBar.__init__(self, parent, *args, **kwargs)
        MenuBar.__init__(self, parent, *args, **kwargs)
        ToolBar.__init__(self, parent, *args, **kwargs)
        TreeContextMenu.__init__(self, parent, *args, **kwargs)

        # Some actions which are not relevant for any specific area
        Actions.__init__(self, *args, **kwargs)
        # The functions to enable printing
        Printing.__init__(self, parent, *args, **kwargs)
        # The functions to enable the help system
        Help.__init__(self, *args, **kwargs)
        # The functions to enable the about dialog
        About.__init__(self, *args, **kwargs)
        # The functions to enable the about dialog
        Settings.__init__(self, *args, **kwargs)
        #Set main splitter
        MainSplitter.__init__(self, *args, **kwargs)
        #Add the xml tree
        Document.__init__(self, *args, **kwargs)
        #Fill xml tree
        GetData.__init__(self, *args, **kwargs)
        #Add functions to modify the view of the xml tree
        ViewData.__init__(self, *args, **kwargs)
        #Add functions to edit the xml tree
        EditData.__init__(self, *args, **kwargs)

        #Copy example files: Comment this out if Template-Designer is in productive use.
        #self.getExamples()
        #Some kind of self check
        self.saveConfig()

        #Set panels
        #self.propertiesPanel = wx.Panel(self.mainSplitter)
        self.propertiesPanel = wx.ScrolledWindow(self.mainSplitter)
        self.templatePanel   = wx.Panel(self.mainSplitter)

        #Buttons on main frame
        self.applyButton       = wx.Button(self.propertiesPanel, 
                                           wx.ID_APPLY, 
                                           _(u"Apply changes"), 
                                           name="applyButton")
        self.defaultsButton    = wx.Button(self.propertiesPanel, 
                                           wx.ID_RESET, 
                                           _(u"Restore settings"), 
                                           name="defaultsButtons")

        expandAllButtonPath = self.documentTreeGraphics() + "/2downarrow.png"
        expandAllButtonBmp = wx.Image(expandAllButtonPath, wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        self.expandAllButton   = wx.BitmapButton(self.templatePanel, 
                                                 -1, 
                                                 expandAllButtonBmp, 
                                                 name="expandButton")

        collapseAllButtonPath = self.documentTreeGraphics() + "/2uparrow.png"
        collapseAllButtonBmp = wx.Image(collapseAllButtonPath, wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        self.collapseAllButton   = wx.BitmapButton(self.templatePanel, 
                                                 -1, 
                                                 collapseAllButtonBmp, 
                                                 name="collapseButton")

        addButtonPath = self.documentTreeGraphics() + "/filenew.png"
        addButtonBmp = wx.Image(addButtonPath, wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        self.addButton   = wx.BitmapButton(self.templatePanel, 
                                                 -1, 
                                                 addButtonBmp, 
                                                 name="addButton")

        deleteButtonPath = self.documentTreeGraphics() + "/edit_delete.png"
        deleteButtonBmp = wx.Image(deleteButtonPath, wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        self.deleteButton   = wx.BitmapButton(self.templatePanel, 
                                                 -1, 
                                                 deleteButtonBmp, 
                                                 name="deleteButton")

        """
        Set taskbar icon. If you remove this, do not forget to remove 
        the RemoveIcon() and Destroy() methods 
        in self.onCloseWindow()
        
        """
        self.taskBarIcon = wx.TaskBarIcon()
        iconPath = self.skinGraphics() + "/domtreeviewer.png"
        icon = wx.Icon(iconPath, wx.BITMAP_TYPE_PNG)
        self.taskBarIcon.SetIcon(icon, _(u"Template-Designer"))

        #Set titlebar icon
        self.SetIcon(icon)

        #Initiate the contents of the property panel
        self.pp = pp

        self.__doProperties()
        self.__doBindings()
        self.__doLayout()
        Safety(self)

    def __doProperties(self):
        """Sets default properties of the frame
        
        Don't touch the name of the frame! Never!
        
        """
        self.SetName("templateDesignerFrame")
        self.SetExtraStyle(wx.FULL_REPAINT_ON_RESIZE)
        self.SetWindowStyleFlag(wx.ADJUST_MINSIZE)
        self.SetTitle(_(u"Template-Designer"))
        self.SetMinSize((800, 600))
        self.SetSizeWH(800, 600)
        # Set menubar contents
        self.setMenuBarData()
        # Set toolbar contents
        self.setToolBarData()
        # Set statusBar contents
        self.setStatusBarContent()
        # Set button defaults
        self.applyButton.Disable()
        self.defaultsButton.Disable()

    def __doBindings(self):
        self.Bind(wx.EVT_BUTTON, self.OnApply, self.applyButton)
        self.Bind(wx.EVT_BUTTON, self.OnRestore, self.defaultsButton)
        self.Bind(wx.EVT_BUTTON, self.OnExpandAll, self.expandAllButton)
        self.Bind(wx.EVT_BUTTON, self.OnCollapseAll, self.collapseAllButton)
        self.Bind(wx.EVT_BUTTON, self.OnAddItem, self.addButton)
        self.Bind(wx.EVT_BUTTON, self.OnDeleteItem, self.deleteButton)
        self.Bind(wx.EVT_CLOSE, self.OnExitWindow)

        self.Bind(wx.EVT_TREE_ITEM_MENU, self.OnTreeContextMenu)
        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelChanged, self.document)
        self.Bind(wx.EVT_TREE_SEL_CHANGING, self.OnSelChanging, self.document)
        self.Bind(wx.EVT_TREE_BEGIN_LABEL_EDIT, self.OnLabelBeginEdit)
        self.Bind(wx.EVT_TREE_END_LABEL_EDIT, self.OnLabelEndEdit)
        if self.safetyMode == "fullAccess":
            self.Bind(wx.EVT_TREE_BEGIN_DRAG, self.OnDragBegin)
            self.Bind(wx.EVT_TREE_END_DRAG, self.OnDragEnd)

    def __doLayout(self):
        mainSizer = wx.BoxSizer(wx.HORIZONTAL)

        templateSizer = wx.BoxSizer(wx.VERTICAL)
        templateButtonSizer = wx.BoxSizer(wx.HORIZONTAL)
        templateButtonSizer.Add(self.expandAllButton, 0, wx.ALL, 4)
        templateButtonSizer.Add(self.collapseAllButton, 0, wx.ALL, 4)
        templateButtonSizer.Add(self.addButton, 0, wx.ALL, 4)
        templateButtonSizer.Add(self.deleteButton, 0, wx.ALL, 4)
        templateSizer.Add(self.document, 1, wx.EXPAND, 0)
        templateSizer.Add(templateButtonSizer, 0, 0, 0)
        self.templatePanel.SetSizer(templateSizer)

        self.propertiesSizer = wx.BoxSizer(wx.VERTICAL)
        propertyButtonSizer = wx.BoxSizer(wx.HORIZONTAL)
        propertyButtonSizer.Add(self.applyButton, 0, wx.ALL, 8)
        propertyButtonSizer.Add(self.defaultsButton, 0, wx.ALL, 8)
        #Never touch the name of the next panel!
        self.propertiesSizer.Add(wx.Panel(self.propertiesPanel, name="propertyPanel"), 1, wx.EXPAND, 0)
        self.propertiesSizer.Add(propertyButtonSizer, 0, wx.ALIGN_RIGHT|wx.ALIGN_BOTTOM, 0)
        self.propertiesPanel.SetSizer(self.propertiesSizer)

        self.mainSplitter.SplitVertically(self.templatePanel, self.propertiesPanel)

        mainSizer.Add(self.mainSplitter, 1, wx.EXPAND, 0)
        self.SetSizer(mainSizer)
        mainSizer.Fit(self)
        self.Layout()
