#!/usr/bin/env python

import wx

class posDimStatus:
    def __init__(self, parent):
        self.parent = parent
        self.statusText = ""
        self.horizontal()
        self.vertical()
        self.dimension()
        self.setStatus()

    def horizontal(self):
        window = ["positionLeft", "positionRight", "dimensionWidth"]
        value = []
        for obj in window:
            value.append(self.parent.frame.FindWindowByName(obj).GetValue())
        i = value.count(u"auto")
        if i > 1:
            self.statusText = _(u"The horizontal direction is underdefined. ")
        elif i < 1:
            self.statusText = _(u"The horizontal direction is overdefined. ")
        return

    def vertical(self):
        window = ["positionTop", "positionBottom", "dimensionHeight"]
        value = []
        for obj in window:
            value.append(self.parent.frame.FindWindowByName(obj).GetValue())
        i = value.count(u"auto")
        if i > 1:
            self.statusText += _(u"The vertical direction is underdefined. ")
        elif i < 1:
            self.statusText += _(u"The vertical direction is overdefined. ")
        return

    def dimension(self):
        window = ["dimensionHeight", "dimensionWidth"]
        value = []
        for obj in window:
            value.append(self.parent.frame.FindWindowByName(obj).GetValue())
        i = value.count(u"0")
        i += value.count(u"0.0")
        if not i == 0:
            self.statusText += _(u"Dimension is zero: This is senseless. ")

    def setStatus(self):
        self.parent.frame.FindWindowByName("dimPosStatus").SetLabel(self.statusText)
