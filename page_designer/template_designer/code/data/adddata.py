#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx

from time import time
import copy

import xml.etree.ElementTree as ET

class AddData:
    """This class adds a new compilation/template/page/frame 
    relative to the selected item inside the xml tree
    
    """
    def __init__(self, *args, **kwargs):
        pass

    def OnAddItem(self, event=None):
        item = self.document.GetSelection()
        if self.identifyMyItem_(item) == "root":
            for axis in self.getChildren_(item):
                if self.document.GetItemText(axis) == _(u"Client-Templates"):
                    designer = self.defaultXml.getroot()
                    item = self.document.AppendItem(axis, designer.attrib["name"], data=None)
                    self.document.SetItemPyData(item, copy.deepcopy(designer))
                    self.document.SetItemImage(item, self.document.imageCompilation, wx.TreeItemIcon_Normal)
        elif self.identifyMyItem_(item) == "axis":
            designer = self.defaultXml.getroot()
            item = self.document.AppendItem(item, designer.attrib["name"], data=None)
            self.document.SetItemPyData(item, copy.deepcopy(designer))
            self.document.SetItemImage(item, self.document.imageCompilation, wx.TreeItemIcon_Normal)
        elif self.identifyMyItem_(item) == "designer":
            template = self.defaultXml.getroot().find(".//{http://www.bitplant.de/template}template")
            item = self.document.AppendItem(item, template.attrib["name"], data=None)
            self.document.SetItemPyData(item, copy.deepcopy(template))
            self.document.SetItemImage(item, self.document.imageDocuments, wx.TreeItemIcon_Normal)
        elif self.identifyMyItem_(item) == "template":
            page = self.defaultXml.getroot().find(".//{http://www.bitplant.de/template}page")
            item = self.document.AppendItem(item, page.attrib["name"], data=None)
            self.document.SetItemPyData(item, copy.deepcopy(page))
            self.document.SetItemImage(item, self.document.imagePages, wx.TreeItemIcon_Normal)
        elif self.identifyMyItem_(item) == "page":
            frame = self.defaultXml.getroot().find(".//{http://www.bitplant.de/template}frame")
            item = self.document.AppendItem(item, frame.attrib["name"], data=None)
            self.document.SetItemPyData(item, copy.deepcopy(frame))
            self.document.SetItemImage(item, self.document.imageFrames, wx.TreeItemIcon_Normal)
        elif self.identifyMyItem_(item) == "frame":
            frame = self.defaultXml.getroot().find(".//{http://www.bitplant.de/template}frame")
            item = self.document.AppendItem(self.document.GetItemParent(item), frame.attrib["name"], data=None)
            self.document.SetItemPyData(item, copy.deepcopy(frame))
            self.document.SetItemImage(item, self.document.imageFrames, wx.TreeItemIcon_Normal)
        if item:
            wx.CallAfter(self.document.SelectItem, item)
        self.document.ExpandAllChildren(self.document.GetItemParent(item))
        self.remapData()
        self.OnEdit()
        self.setStatusBarContent()
        return

    def __designerXml(self):
        designer = self.defaultXml.find(".//{http://www.bitplant.de/template}designer")
        return designer

    def __templateXml(self):
        template = self.defaultXml.find(".//{http://www.bitplant.de/template}template")
        return template

    def __pageXml(self):
        page = self.defaultXml.find(".//{http://www.bitplant.de/template}page")
        return page

    def __frameXml(self):
        frame = self.defaultXml.find(".//{http://www.bitplant.de/template}frame")
        return frame
