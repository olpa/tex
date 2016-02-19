#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import os
import random
from time import time

import xml.etree.ElementTree as ET

from adddata import AddData
from remapdata import RemapData
from preparedata import PrepareData
from writedata import WriteData

# For debug reason, I need to trace changes in tempItemData
class TracedDict(dict):
  def __setitem__(self, k ,v):
    #print "TracedDict: [%s]=%s" % (repr(k), repr(v))
    dict.__setitem__(self, k, v)

class EditData(AddData, RemapData, WriteData):
    """
The editData class includes all functions that are relevant while 
modifiying the assigned xml information of the derived class documentData.
This includes the en/disabling of gui elements while changing information and
the functions to initiate more complex actions with the data like saving.
    """
    def __init__(self, *args, **kwargs):
        ET._namespace_map["http://www.bitplant.de/template"] = "bit"
        self.defaultXml = ET.parse("definitions/default.xml")
        AddData.__init__(self, *args, **kwargs)
        RemapData.__init__(self, *args, **kwargs)
        WriteData.__init__(self, *args, **kwargs)

        #This Boolean indicates, if it is possible or required to save.
        self.change = False
        #Define global dictionary with temporary item data
        self.tempItemData = TracedDict()
        #Define global tuple, to save items which are moved between axis
        self.axisDrag = []
        #Define global tuple, to save items which are moved between axis and contain images
        self.imageDrag = []
        #Define global tuple, to save items whose files need to be deleted
        self.deleteItem = []

    def OnEdit(self, event=None):
        """This function enables all requied widgets, 
        if an edit of the xml data happend by the user

        """
        self.change = True
        self.toolBar.EnableTool(wx.ID_SAVE, True)
        self.applyButton.Enable()
        self.defaultsButton.Enable()

    def OnApply(self, event=None):
        """This function is called after the user 
        clicked the apply button
        
        """
        self.OnSave(event)
        self.OnSelChanged(restoreItem = True)

    def OnRestore(self, event=None):
        """This function throws all temporary data away and recalls 
        the item as if the user had selected the item. This leads 
        to a recall of the saved data
        
        """
        # Reset element name in tree if required
        if self.tempItemData.has_key("informationName"):
            item = self.document.GetSelection()
            if self.document.GetRootItem() == self.document.GetItemParent(item):
                # This should for now not happen, 
                # because the axis don't wear data
                pass
            else:
                xml = self.document.GetItemPyData(item)
                self.document.SetItemText(item, xml.attrib["name"])
        # Reset state
        # self.change = False
        self.applyButton.Disable()
        self.defaultsButton.Disable()
        # Reset temporary data. This should be in xml object now
        self.tempItemData.clear()
        # Recall the item to show saved values
        self.OnSelChanged(restoreItem = True)

    def OnSave(self, event=None):
        """This function appends user modified data to the xml data
        
        This function does not write any data to the hard disk
        
        """
        #Check for modified data
        PrepareData(self)
        #Reset state
        #self.change = False
        self.applyButton.Disable()
        self.defaultsButton.Disable()
        #Reset temporary data. This should be in xml object now
        self.tempItemData.clear()

    def OnSelChanging(self, event=None):
        """This function is called while an item in the tree was clicked
        and is executed before the selection changes to the new item.
        
        This is a good place to stop changing the item selection if
        something goes wrong.
        
        There is a point you should know about: This method is 
        automatically called, after an item was dropped because the 
        selection changes automatically to the parent item. 
        
        """
        self.OnSave()

    def OnDeleteItem(self, event=None):
        """This function deletes a selected item and its children
        from inside the xml tree
        
        """
        item = self.document.GetSelection()
        if not item.IsOk():
            return
        if self.document.GetItemParent(item) == self.document.GetRootItem():
            return
        if item == self.document.GetRootItem():
            return
        category = self.identifyMyItem_(item)
        dialog = wx.MessageDialog(None, 
                                  _(u"Are you sure you want to delete the selected %s") % (category.capitalize()), 
                                  _(u"Delete %s") % (category.capitalize()), 
                                  wx.YES_NO|wx.NO_DEFAULT|wx.ICON_QUESTION)
        decision = dialog.ShowModal()
        if decision == wx.ID_NO:
            dialog.Destroy()
            return
        dialog.Destroy()

        #Mark xml file as removable if possible and required
        data = self.document.GetItemPyData(item)
        if hasattr(data, "filename"):
            if self.getAxis_(item) == _(u"Client-Templates"):
                directory = self.clientTemplates()
            elif self.getAxis_(item) == _(u"Server-Templates"):
                directory = self.serverTemplates()
            self.deleteItem.append(directory + "/" + data.filename)

        #Mark image file as removable if possible and required
        content = data.findall(".//{http://www.bitplant.de/template}content")
        if content:
            for image in content:
                if image.get("type") == "image":
                    file = image.text.split(":")[1]
                    directory =  image.text.split(":")[0]
                    if directory == _(u"clientImages"):
                        directory = self.clientImages()
                    else:
                        directory = self.serverImages()
                    self.deleteItem.append(directory + "/" + file)

        self.deleteMyItemRecursivly_(item)
        self.OnEdit()
        # Remap the tree data, so xml data in 
        # tree correspondents to the items in the tree
        self.remapData()
        # Comment the next line if not using the statusbar class
        self.setStatusBarContent()
        return

    def deleteMyItemRecursivly_(self, item):
        """This function moves an old item and 
        its children to a new given position
        
        """
        if self.document.ItemHasChildren(item) == True:
            for child in self.getChildren_(item):
                self.deleteMyItemRecursivly_(child)
        self.document.Delete(item)
        return

    def OnDragBegin(self, event=None):
        """This function is called when a drag&drop action is initiated
        
        """
        event.Allow()
        self.dragItem = event.GetItem()
        return

    def OnDragEnd(self, event=None):
        """This function is called when a drag-source 
        is hover an drop-target and mouse drops source
        
        """
        if event.GetItem().IsOk():
            target = event.GetItem()
        else:
            return
        try:
            source = self.dragItem
        except:
            return
        targetParent = self.document.GetItemParent(target)
        sourceParent = self.document.GetItemParent(source)
        #Be choosy and return. The next steps compare source, target and 
        #targetparent and decide what to do
        #Identify involved items
        idSource       = self.identifyMyItem_(source)
        idTarget       = self.identifyMyItem_(target)
        idTargetParent = self.identifyMyItem_(targetParent)
        idSourceParent = self.identifyMyItem_(sourceParent)
        if not targetParent.IsOk():
            return
        #Stop configurations
        if idSource == "root":
            return
        if idTarget == "root":
            return
        if idSource == "axis" and idTarget != "axis":
            return
        if idTarget == "axis" and not (idSource == "designer" or idSource == "template"):
            return
        if idTarget == "designer" and not (idSource == "designer" or idSource == "template"):
            return
        if idTarget == "template" and not (idSource == "template" or idSource == "page"):
            return
        if idTarget == "page" and not (idSource == "page" or idSource == "frame"):
            return

        #Do it
        if idTarget == idSource:
            #To allow positioning of objects inside a parent
            newItem = self.insertMyItemRecursivly_(target, source)
        else:
            newItem = self.appendMyItemRecursivly_(target, source)

        self.OnEdit()
        self.remapData()
        return

    def appendMyItemRecursivly_(self, parentItem, oldItem):
        """This function moves an old item and its children 
        to a new given position under a parental item
        
        Returns the new item
        
        """
        if self.document.ItemHasChildren(oldItem) == True:
            #Move recursively
            children = self.getChildren_(oldItem)
            newItem = self.appendMyItem_(parentItem, oldItem)
            for child in children:
                self.appendMyItemRecursivly_(newItem, child)
        else:
            #AppendItem
            newItem = self.appendMyItem_(parentItem, oldItem)
        #Drop old item
        self.document.Delete(oldItem)
        return newItem

    def insertMyItemRecursivly_(self, previousItem, oldItem):
        """This function moves an old item and its children 
        to a new given position near a previous item
        
        Returns the new tree item
        
        """
        if self.document.ItemHasChildren(oldItem) == True:
            #Move recursively
            children = self.getChildren_(oldItem)
            newItem = self.insertMyItem_(previousItem, oldItem)
            for child in children:
                self.appendMyItemRecursivly_(newItem, child)
        else:
            #AppendItem
            newItem = self.insertMyItem_(previousItem, oldItem)
        #Drop old item
        self.document.Delete(oldItem)
        return newItem

    def identifyMyItem_(self, item):
        """This is a helper function, which returns a characterizing 
        string of the given item. 
        Possible values are: root, axis, template, page, frame 
        or the Type None if item is unknown
        
        """
        if not item.IsOk():
            return
        if item == self.document.GetRootItem():
            return "root"
        if self.document.GetItemParent(item) == self.document.GetRootItem():
            return "axis"
        data = self.document.GetItemPyData(item)
        if data.tag.rsplit("}")[-1] == "designer":
            return "designer"
        if data.tag.rsplit("}")[-1] == "template":
            return "template"
        if data.tag.rsplit("}")[-1] == "page":
            return "page"
        if data.tag.rsplit("}")[-1] == "frame":
            return "frame"
        return

    def appendMyItem_(self, parentItem, oldItem):
        """This is a helper function to append a copy of 
        an old treectrl item to another place inside the tree
        
        Does not delete the old item
        
        Returns the new tree item
        
        """
        #Rescue item data
        text                 = self.document.GetItemText(oldItem)
        iconNormal           = self.document.GetItemImage(oldItem, wx.TreeItemIcon_Normal)
        iconSelected         = self.document.GetItemImage(oldItem, wx.TreeItemIcon_Selected)
        iconExpanded         = self.document.GetItemImage(oldItem, wx.TreeItemIcon_Expanded)
        iconSelectedExpanded = self.document.GetItemImage(oldItem, wx.TreeItemIcon_SelectedExpanded)
        data                 = self.document.GetItemPyData(oldItem)
        #Create new item
        newItem = self.document.AppendItem(parentItem, text)
        #Apply old item data to new one
        self.document.SetItemPyData(newItem, data)
        self.document.SetItemImage(newItem, iconNormal, wx.TreeItemIcon_Normal)
        self.document.SetItemImage(newItem, iconSelected, wx.TreeItemIcon_Selected)
        self.document.SetItemImage(newItem, iconExpanded, wx.TreeItemIcon_Expanded)
        self.document.SetItemImage(newItem, iconSelectedExpanded, wx.TreeItemIcon_SelectedExpanded)
        return newItem

    def insertMyItem_(self, previousItem, oldItem):
        """This is a helper function to insert a copy of 
        an old treectrl item to another place inside the tree
        
        Does not delete the old item
        
        Returns the new tree item
        
        """
        #Rescue item data
        text                 = self.document.GetItemText(oldItem)
        iconNormal           = self.document.GetItemImage(oldItem, wx.TreeItemIcon_Normal)
        iconSelected         = self.document.GetItemImage(oldItem, wx.TreeItemIcon_Selected)
        iconExpanded         = self.document.GetItemImage(oldItem, wx.TreeItemIcon_Expanded)
        iconSelectedExpanded = self.document.GetItemImage(oldItem, wx.TreeItemIcon_SelectedExpanded)
        data                 = self.document.GetItemPyData(oldItem)
        #Create new item
        newItem = self.document.InsertItem(self.document.GetItemParent(previousItem), previousItem, text)
        #Apply old item data to new one
        self.document.SetItemPyData(newItem, data)
        self.document.SetItemImage(newItem, iconNormal, wx.TreeItemIcon_Normal)
        self.document.SetItemImage(newItem, iconSelected, wx.TreeItemIcon_Selected)
        self.document.SetItemImage(newItem, iconExpanded, wx.TreeItemIcon_Expanded)
        self.document.SetItemImage(newItem, iconSelectedExpanded, wx.TreeItemIcon_SelectedExpanded)
        return newItem

    def OnLabelBeginEdit(self, event=None):
        """This method is to prevent modifying the axis of 
        the tree or the root element
        
        Returns False, if Edit was prevented, else returns True
        
        """
        item = event.GetItem()
        if item == self.document.GetRootItem():
            event.Veto()
            return False
        if self.document.GetItemParent(item) == self.document.GetRootItem():
            event.Veto()
            return False
        return True

    def OnLabelEndEdit(self, event=None):
        """This method is called, when the 
        user edited a label inside the tree
        
        """
        item = event.GetItem()
        newlabel = event.GetLabel() 
        xml = self.document.GetItemPyData(item)
        #Update xml
        if self.document.GetItemParent(item) == self.document.GetRootItem():
            return
        if item == self.document.GetRootItem():
            return
        xml.attrib["name"] = newlabel
        #Update view in right panel
        if self.identifyMyItem_(item) != "designer":
            nameWindow = self.FindWindowByName("informationName")
            nameWindow.SetValue(newlabel)
        #Update gui widgets
        self.OnEdit()
        #Append xml
        self.document.SetItemPyData(item, xml)

    def getChildren_(self, parent):
        """Gets a treeitem and returns a tuple of the treeItems children
        
        """
        result = []
        child, cookie = self.document.GetFirstChild(parent)
        while child:
            result.append(child)
            child, cookie = self.document.GetNextChild(parent, cookie)
        return result

    def getAxis_(self, item):
        """This function returns the item text of the item which 
        is ancestor of the given item and directly under the root item.
        This should be the "Server-Templates" or "Client-Templates" item
        
        """
        if self.document.GetItemParent(item) != self.document.GetRootItem():
            return self.getAxis_(self.document.GetItemParent(item))
        else:
            return unicode(self.document.GetItemText(item))
