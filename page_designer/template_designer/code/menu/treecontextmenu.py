#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
from safety import Safety
from createmenu import CreateMenu

class TreeContextMenu(CreateMenu):

    """
This class contains the context menu definitions for the xml tree,
adds them to a menu and add this menu to the classes parent. 
The menu is called treeContextMenu
    """

    def __init__(self, *args, **kwargs):
        CreateMenu.__init__(self, *args, **kwargs)

    def getTreeMenuData(self):
        if self.safetyMode == "fullAccess":
            return [("&Edit", (
                    (_(u"&New"), _(u"Create new template file"), self.OnNew, "filenew.png", "Ctrl+N"),
                    (_(u"Remove"), _(u"Remove current selection"), self.OnDeleteItem, "edit_delete.png", "Ctrl+Del"))),
                (_(u"&View"), (
                    (_(u"Expand All"), _(u"Expand all items"), self.OnExpandAll, "2downarrow.png", ""),
                    (_(u"Collapse All"), _(u"Collapse all items"), self.OnCollapseAll, "2uparrow.png", "")))]
        elif self.safetyMode == "restrictedAccess":
            return [(_(u"&View"), (
                    (_(u"Expand All"), _(u"Expand all items"), self.OnExpandAll, "2downarrow.png", ""),
                    (_(u"Collapse All"), _(u"Collapse all items"), self.OnCollapseAll, "2uparrow.png", "")))]
        else:
            return [(_(u"&View"), (
                    (_(u"Expand All"), _(u"Expand all items"), self.OnExpandAll, "2downarrow.png", ""),
                    (_(u"Collapse All"), _(u"Collapse all items"), self.OnCollapseAll, "2uparrow.png", "")))]

    def OnTreeContextMenu(self, event=None):
        self.graphics = self.documentTreeGraphics()
        self.treeContextMenu = self.createMenu(self.getTreeMenuData())
        self.PopupMenu(self.treeContextMenu)
