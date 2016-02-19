#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
from getdata import GetData

class Tree(wx.TreeCtrl):

    def __init__(self, parent, *args, **kwargs):
        wx.TreeCtrl.__init__(self, parent, 
                             style=wx.TR_HIDE_ROOT|wx.TR_DEFAULT_STYLE|wx.TR_FULL_ROW_HIGHLIGHT, 
                             *args, **kwargs)
        self.parent = parent

        self.createRootItem()

        self.imageList = wx.ImageList(16,16)
        self.imageSource = self.imageList.Add(wx.Image(self.parent.documentTreeGraphics() + "/folder_grey.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap())
        self.imageCompilation = self.imageList.Add(wx.Image(self.parent.documentTreeGraphics() + "/domtreeviewer.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap())
        self.imageDocuments = self.imageList.Add(wx.Image(self.parent.documentTreeGraphics() + "/txt.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap())
        self.imagePages = self.imageList.Add(wx.Image(self.parent.documentTreeGraphics() + "/wordprocessing.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap())
        self.imageFrames = self.imageList.Add(wx.Image(self.parent.documentTreeGraphics() + "/favorites.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap())
        self.AssignImageList(self.imageList)
        self.SetItemImage(self.rootItem, self.imageSource, wx.TreeItemIcon_Normal)

        self.__doProperties()
        self.__doLayout()

    def createRootItem(self):
        self.rootItem = self.AddRoot(_(u"Available Templates"))

    def __doProperties(self):
        self.SetName("dataTree")

    def __doLayout(self):
        pass

class Document:

    def __init__(self, *args, **kwargs):
        #Create xml tree object
        self.document = Tree(self)
