#!/usr/bin/env python
# -*- coding: utf-8 -*-
import wx
import gettext
trans = gettext.translation(domain="testapplication", localedir="i18n", fallback=True) 
trans.install("testapplication")

class rotateText(wx.StaticBitmap):

    """
This class rotates a given string.
Example call: rotateText(self, "Call me rotated text", 90)
This returns a derived object of class wx.StaticBitmap with 
text "Call me rotated text" and rotated count-clockwise 90 degree.
Possible degrees are 0 (default), 90, 180, 270
    """

    def __init__(self, parent, text=_(u"Please define a text"), angle=0, *args, **kwargs):
        wx.StaticBitmap.__init__(self, parent, *args, **kwargs)
        self.text = text
        self.text = self.text.splitlines()[0]
        self.angle = angle
        if [0, 90, 180, 270].count(self.angle) != 1:
            exit(_(u"Error in class rotateText(). Please give me a valid angle to rotate the given text"))
        self.__calculateSizes()
        self.__getText()

    def __calculateSizes(self):
        bmp = wx.EmptyBitmap(1000, 1000)
        dc = wx.MemoryDC(bmp)
        dc.SetFont(wx.SystemSettings.GetFont(1))

        size = dc.GetTextExtent(self.text)
        self.w, self.h = size
        self.x = 0
        self.y = 0

        if self.angle == 90:
            self.h, self.w = size
            self.y = self.h
        if self.angle == 180:
            self.w, self.h = size
            self.x = self.w
            self.y = self.h
        if self.angle == 270:
            self.h, self.w = size
            self.x = self.w

    def __getText(self):
        bmp = wx.EmptyBitmap(self.w, self.h)
        dc = wx.MemoryDC(bmp)
        dc.SetBackground(wx.NullBrush)
        dc.Clear()
        dc.SetFont(wx.SystemSettings.GetFont(1))
        dc.DrawRotatedText(self.text, self.x, self.y, self.angle)
        self.SetBitmap(bmp)
