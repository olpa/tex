#!/usr/bin/env python

import wx
from colors import colors

class colorSetting:
    def __init__(self, parent, color="cmyk(0, 0, 0, 255)"):
        self.parent = parent
        self.frame = self.parent.GetTopLevelParent()
        self.myColor = colors(color)
        self.setColor(color)

    def setColor(self, color="cmyk(0, 0, 0, 255)"):
        self.myColor.setColor(color)

    def setHex(self):
        hex = self.myColor.getHex()
        hexPanel = self.frame.FindWindowByName("colorHexPanel")
        if hexPanel:
            hexPanel.input.SetValue(hex.lstrip("#"))

    def setCmyk(self):
        cmyk = self.myColor.getCmyk()
        cmykPanel = self.frame.FindWindowByName("colorCmykPanel")
        if cmykPanel:
            cmykPanel.cSpin.SetValue(int(cmyk[0]))
            cmykPanel.mSpin.SetValue(int(cmyk[1]))
            cmykPanel.ySpin.SetValue(int(cmyk[2]))
            cmykPanel.kSpin.SetValue(int(cmyk[3]))

    def setSelect(self):
        rgb = self.myColor.getRgb()
        selectPanel = self.frame.FindWindowByName("colorSelectPanel")
        if selectPanel:
            selectPanel.color.SetValue(wx.Colour(rgb[0], rgb[1], rgb[2]))

    def setRgb(self):
        rgb = self.myColor.getRgb()
        rgbPanel = self.frame.FindWindowByName("colorRgbPanel")
        if rgbPanel:
            rgbPanel.rSpin.SetValue(int(rgb[0]))
            rgbPanel.gSpin.SetValue(int(rgb[1]))
            rgbPanel.bSpin.SetValue(int(rgb[2]))
