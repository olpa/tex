#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx

class CreateMenu():

    def __init__(self, *args, **kwargs):
        pass

    def createMenu(self, menuData):
        menu = wx.Menu()
        for eachItem in menuData:
            if len(eachItem) == 2:
                label = eachItem[0]
                subMenu = self.createMenu(eachItem[1])
                menu.AppendMenu(wx.NewId(), label, subMenu)
            else:
                self.createMenuItem(menu, *eachItem)
        return menu

    def createMenuItem(self, menu, label, status, handler, image="", 
                       accel="", val="", kind=wx.ITEM_NORMAL):
        if not label:
            menu.AppendSeparator()
            return True
        menuItem = wx.MenuItem(menu, -1, label, status, kind)
        if image:
            image = wx.Image(self.graphics + "/" + image, wx.BITMAP_TYPE_PNG).ConvertToBitmap()
            menuItem.SetBitmap(image)
        if accel:
            menuItem.SetText(label + "\t" + accel)
        menuItem.SetHelp(status)
        menu.AppendItem(menuItem)
        self.Bind(wx.EVT_MENU, handler, menuItem)
