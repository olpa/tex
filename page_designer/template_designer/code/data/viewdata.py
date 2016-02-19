#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx

class ViewData():
    """
The viewData class handles all functions which are relevant to to presentation
of the treeCtrl, which is derived from it with class documentData.
    """
    def __init__(self, *args, **kwargs):
        pass

    def OnSelChanged(self, event=None, restoreItem=None):
        if restoreItem:
            item = self.document.GetSelection()
        else:
            item = event.GetItem()
        if not item.IsOk():
            return
        xmlDataObject = self.document.GetItemPyData(item)

        #Delete old panel
        for i in self.propertiesPanel.GetChildren():
                if i.GetName() == "propertyPanel":
                    # (See note (04.06.2010))
                    #This is required because problems with Python2.6
                    #In Python2.5 a simple 
                    i.Destroy() #is enough!
                    #This also leads to a bug i don't know how to
                    #prevent. If wx.CallAfter() is used, the color panel
                    #does not initialize its validator
                    #wx.CallAfter(i.Destroy)
                    # Note 04.06.2010, olpa
                    # Simple i.Destroy() does work for me. If not,
                    # the use of CallAfter should be corrected. In current
                    # implementation, an asynchronious call leads to an
                    # unexpected call of the window validator, the validator
                    # updates tempItemData with now wrong value, which
                    # comes to XML of other frame. AS result, the template
                    # is corrupted.

        #Please be cautious with the following i18n strings! 
        #These are referenced from "__init__()" for comparison.
        if self.document.GetRootItem() == item:
            panel = self.pp.nothing(self.propertiesPanel, name="propertyPanel")
        elif self.document.GetItemText(item) == _(u"Server-Templates"):
            panel = self.pp.nothing(self.propertiesPanel, name="propertyPanel")
        elif self.document.GetItemText(item) == _(u"Client-Templates"):
            panel = self.pp.nothing(self.propertiesPanel, name="propertyPanel")
        else:
            if xmlDataObject.tag.rsplit("}")[-1] == "designer":
                panel = self.pp.designer(self.propertiesPanel, name="propertyPanel")
            elif xmlDataObject.tag.rsplit("}")[-1] == "template":
                panel = self.pp.template(self.propertiesPanel, name="propertyPanel")
            elif xmlDataObject.tag.rsplit("}")[-1] == "page":
                panel = self.pp.page(self.propertiesPanel, name="propertyPanel")
            elif xmlDataObject.tag.rsplit("}")[-1] == "frame":
                panel = self.pp.frame(self.propertiesPanel, name="propertyPanel")
            else:
                return

        #Add new panel to existing sizer
        self.propertiesSizer.Prepend(panel, 1, wx.EXPAND, 0)
        #Renew Layout
        self.Layout()
        self.propertiesPanel.Layout()

    def OnExpandAll(self, event=None):
        self.document.ExpandAll()

    def OnCollapseAll(self, event=None):
        root = self.document.GetRootItem()
        if self.document.ItemHasChildren(root):
            cookie = 0
            (item, cookie) = self.document.GetFirstChild(root)
            while item.IsOk():
                self.document.CollapseAllChildren(item)
                (item, cookie) = self.document.GetNextChild(root, cookie)
