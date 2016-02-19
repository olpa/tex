#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import wx.gizmos
from safety import Safety

class dateTimeTree(wx.gizmos.TreeListCtrl):
    def __init__(self, parent, *args, **kwds):
        wx.gizmos.TreeListCtrl.__init__(self, parent, style = wx.TR_DEFAULT_STYLE|wx.TR_FULL_ROW_HIGHLIGHT|wx.TR_HIDE_ROOT)

        self.parent = parent.parent
        self.frame = self.parent.parent
        self.tree = self.parent.parent.document

        self.AddColumn("Category")
        self.AddColumn("Description")
        self.AddColumn("Example")
        self.SetMainColumn(0)
        self.SetColumnWidth(0, 130)
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
        return [(_(u"Day and Week"), (
                    (u"d", _(u"Day of the month, 2 digits with leading zeros"), _(u"01 through 31")),
                    (u"D", _(u"A textual representation of a day, three letters"), _(u"Mon through Sun")),
                    (u"j", _(u"Day of the month without leading zeros"), _(u"1 through 31")),
                    (u"l", _(u"A full textual representation of the day of the week"), _(u"Sunday through Saturday")),
                    (u"N", _(u"ISO-8601 numeric representation of the day of the week"), _(u"1 (for Monday) through 7 (for Sunday)")),
                    (u"S", _(u"English ordinal suffix for the day of the month"), _(u"2 characters st, nd, rd or th")),
                    (u"w", _(u"Numeric representation of the day of the week"), _(u"0 (for Sunday) through 6 (for Saturday)")),
                    (u"z", _(u"The day of the year (starting from 0)"), _(u"0 through 365")),
                    (u"W", _(u"ISO-8601 week number of year, weeks starting on Monday"), _(u"42"))
                    )),
                (_(u"Month"), (
                    (u"F", _(u"A full textual representation of a month, such as January or March"), _(u"January through December")),
                    (u"m", _(u"Numeric representation of a month, with leading zeros"), _(u"01 through 12")),
                    (u"M", _(u"A short textual representation of a month, three letters"), _(u"Jan through Dec")),
                    (u"n", _(u"Numeric representation of a month, without leading zeros"), _(u"1 through 12")),
                    (u"t", _(u"Number of days in the given month"), _(u"28 through 31")))),
                (_(u"Year"), (
                    (u"L", _(u"Whether It is a leap year"), _(u"1 if it is a leap year, 0 otherwise.")),
                    (u"o", _(u"ISO-8601 year number"), _(u"1999 or 2003")),
                    (u"Y", _(u"A full numeric representation of a year, 4 digits"), _(u"1999 or 2003")),
                    (u"y", _(u"A two digit representation of a year"), _(u"99 or 03")))),
                (_(u"Time"), (
                    (u"a", _(u"Lowercase Ante meridiem and Post meridiem"), _(u"am or pm")),
                    (u"A", _(u"Uppercase Ante meridiem and Post meridiem"), _(u"AM or PM")),
                    (u"B", _(u"Swatch Internet time"), _(u"000 through 999")),
                    (u"g", _(u"12-hour format of an hour without leading zeros"), _(u"1 through 12")),
                    (u"G", _(u"24-hour format of an hour without leading zeros"), _(u"0 through 23")),
                    (u"h", _(u"12-hour format of an hour with leading zeros"), _(u"01 through 12")),
                    (u"H", _(u"24-hour format of an hour with leading zeros"), _(u"00 through 23")),
                    (u"i", _(u"Minutes with leading zeros"), _(u"00 through 59")),
                    (u"s", _(u"Seconds, with leading zeros"), _(u"00 through 59")),
                    (u"u", _(u"Microseconds"), _(u"40392")))),
                (_(u"Timezone"), (
                    (u"e", _(u"Timezone identifier"), _(u"UTC, GMT, Atlantic/Azores")),
                    (u"I", _(u"Whether or not the date is in daylight saving time"), _(u"1 if Daylight Saving Time, 0 otherwise")),
                    (u"O", _(u"Difference to Greenwich time (GMT) in hours"), _(u"+0200")),
                    (u"P", _(u"Difference to Greenwich time (GMT) with colon between hours and minutes"), _(u"+02:00")),
                    (u"T", _(u"Timezone abbreviation"), _(u"EST, MDT")),
                    (u"Z", _(u"Timezone offset in seconds"), _(u"-43200 through 50400")))),
                (_(u"Full Date/Time"), (
                    (u"c", _(u"ISO 8601 date"), _(u"2004-02-12T15:19:21+00:00")),
                    (u"r", _(u"RFC 2822 formatted date"), _(u"Thu, 21 Dec 2000 16:01:07 +0200")),
                    (u"U", _(u"Seconds since the Unix Epoch"), _(u" (14553423)"))))]

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
