#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import wx.gizmos
from safety import Safety

class documentTree(wx.gizmos.TreeListCtrl):
    def __init__(self, parent, *args, **kwds):
        wx.gizmos.TreeListCtrl.__init__(self, parent, style = wx.TR_DEFAULT_STYLE|wx.TR_FULL_ROW_HIGHLIGHT|wx.TR_HIDE_ROOT)

        self.parent = parent.parent
        self.frame = self.parent.parent
        self.tree = self.parent.parent.document

        self.AddColumn("Category")
        self.AddColumn("Description")
        self.AddColumn("Example")
        self.SetMainColumn(0)
        self.SetColumnWidth(0, 150)
        self.SetColumnWidth(1, 400)
        self.SetColumnWidth(2, 300)

        self.SetMinSize((600, 250))

        root = self.AddRoot("Date/Time Placeholders")
        data = self.isoData()

        self.imageList = wx.ImageList(16,16)
        self.catImg = self.imageList.Add(wx.Image(self.frame.programGraphics() + "/alarmclock.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap())
        self.valImg = self.imageList.Add(wx.Image(self.frame.programGraphics() + "/clock.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap())
        self.AssignImageList(self.imageList)

        self.addItems(root, data)
        self.Expand(root)

        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OnActivated, self)
        Safety(self)

    def OnActivated(self, event=None):
        if self.GetItemParent(self.GetCurrentItem()) == self.GetRootItem() or self.GetCurrentItem() == self.GetRootItem():
            return True
        start = self.parent.text.GetRange(0, self.parent.text.GetInsertionPoint())
        middle = "%" + self.GetItemText(self.GetCurrentItem())
        end = self.parent.text.GetRange(self.parent.text.GetInsertionPoint(), len(self.parent.text.GetValue()))
        value = start + middle + end
        self.parent.text.SetValue(value)
        self.frame.OnEdit()

    def addItems(self, parentItem, items):
        for eachItem in items:
            if len(eachItem) == 2:
                item = self.AppendItem(parentItem, eachItem[0])
                self.SetItemImage(item, self.catImg, wx.TreeItemIcon_Normal)
                self.addItems(item, eachItem[1])
                self.SetItemBold(item)
            else:
                item = self.AppendItem(parentItem, eachItem[0])
                self.SetItemImage(item, self.valImg, wx.TreeItemIcon_Normal)
                self.SetItemText(item, eachItem[0], 0)
                self.SetItemText(item, eachItem[1], 1)
                self.SetItemText(item, eachItem[2], 2)

    def isoData(self):
        return [(_(u"Document"), (
                    (u"1", _(u"Current page, arabic numbers"), _(u"1")),
                    (u"2", _(u"Current page, arabic numbers with leading zerro"), _(u"01")),
                    (u"3", _(u"Current page, roman numbers"), _(u"V")),
                    (u"4", _(u"Current chapter, arabic numbers"), _(u"1")),
                    (u"5", _(u"Current chapter, arabic numbers with leading zero"), _(u"01")),
                    (u"6", _(u"Current chapter, roman numbers"), _(u"V")),
                    (u"7", _(u"Document title"), _(u"This is a Bitplant document")),
                    (u"8", _(u"Section title"), _(u"Howto handle the Template-Designer"))))]

    def OnExpandAll(self, event=None):
        self.ExpandAll(self.GetRootItem())

    def OnCollapseAll(self, event=None):
        root = self.GetRootItem()
        def walkTree(item):
            def getChildren(parent):
                result = []
                item, cookie = self.GetFirstChild(parent)
                while item:
                    result.append(item)
                    item, cookie = self.GetNextChild(parent, cookie)
                return result
            children = getChildren(item)
            for child in children:
                getChildren(child)
                self.Collapse(child)
        walkTree(root)

    def OnCollapseAllButCurrent(self, event=None):
        if self.GetCurrentItem() == self.GetRootItem():
            return True
        mypos = self.GetItemParent(self.GetCurrentItem())
        root = self.GetRootItem()
        self.OnCollapseAll(root)

        def walkTree(item):
            parent = self.GetItemParent(mypos)
            if parent != self.GetRootItem() and self.IsOk() == True:
                walkTree(parent)

        self.Expand(mypos)

    def OnItemExpanded(self, event=None):
        pass

    def OnItemCollapsed(self, event=None):
        pass
