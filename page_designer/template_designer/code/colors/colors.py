#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

from myrgb import myRgb
from mycmyk import myCmyk
from myhex import myHex
from myname import myName

import gettext
trans = gettext.translation(domain="colors", localedir="i18n", fallback=True) 
trans.install("colors")

class colors():

    """
This class defines all available methods.
    """

    def __init__(self, value):
        self.myRgb = myRgb()
        self.myCmyk = myCmyk()
        self.myHex = myHex()
        self.myName = myName()
        self.setColor(value)

    def setColor(self, value):
        self.value = self.setValues(value)

    def getRgb(self):
        return self.value["rgb"]

    def getRgb100(self):
        return self.value["rgb100"]

    def getRgb1(self):
        return self.value["rgb1"]

    def getCmyk(self):
        return self.value["cmyk"]

    def getCmyk100(self):
        return self.value["cmyk100"]

    def getCmyk1(self):
        return self.value["cmyk1"]

    def getHex(self):
        return self.value["hex"]

    def getName(self):
        return self.value["name"]

    def getAll(self):
        return self.value

    def setValues(self, value):
        color = {}
        if re.match(self.myRgb.rgbRe, value) != None:
            color["rgb"]     = self.myRgb.rgb(value)
            color["cmyk"]    = self.myRgb.rgb2cmyk(color["rgb"])
            color["hex"]     = self.myRgb.rgb2hex(color["rgb"])
            color["name"]    = self.myRgb.rgb2name(color["rgb"])
            color["rgb100"]  = self.myRgb.lowerTo100(color["rgb"])
            color["rgb1"]    = self.myRgb.lowerTo1(color["rgb"])
            color["cmyk100"] = self.myRgb.lowerTo100(color["cmyk"])
            color["cmyk1"]   = self.myRgb.lowerTo1(color["cmyk"])
            return color
        elif re.match(self.myCmyk.cmykRe, value) != None:
            color["cmyk"] = self.myCmyk.cmyk(value)
            color["rgb"]  = self.myCmyk.cmyk2rgb(color["cmyk"])
            color["hex"]  = self.myCmyk.cmyk2hex(color["cmyk"])
            color["name"] = self.myCmyk.cmyk2name(color["cmyk"])
            color["rgb100"]  = self.myCmyk.lowerTo100(color["rgb"])
            color["rgb1"]    = self.myCmyk.lowerTo1(color["rgb"])
            color["cmyk100"] = self.myCmyk.lowerTo100(color["cmyk"])
            color["cmyk1"]   = self.myCmyk.lowerTo1(color["cmyk"])
            return color
        elif re.match(self.myHex.hexRe, value) != None:
            color["hex"] = self.myHex.hex(value)
            color["rgb"]  = self.myHex.hex2rgb(color["hex"])
            color["cmyk"]  = self.myHex.hex2cmyk(color["hex"])
            color["name"]  = self.myHex.hex2name(color["hex"])
            color["rgb100"]  = self.myHex.lowerTo100(color["rgb"])
            color["rgb1"]    = self.myHex.lowerTo1(color["rgb"])
            color["cmyk100"] = self.myHex.lowerTo100(color["cmyk"])
            color["cmyk1"]   = self.myHex.lowerTo1(color["cmyk"])
            return color
        elif re.match(self.myName.nameRe, value) != None:
            color["name"] = self.myName.name(value)
            color["rgb"]  = self.myName.name2rgb(color["name"])
            color["cmyk"]  = self.myName.name2cmyk(color["name"])
            color["hex"]  = self.myName.name2hex(color["name"])
            color["rgb100"]  = self.myName.lowerTo100(color["rgb"])
            color["rgb1"]    = self.myName.lowerTo1(color["rgb"])
            color["cmyk100"] = self.myName.lowerTo100(color["cmyk"])
            color["cmyk1"]   = self.myName.lowerTo1(color["cmyk"])
            return color
        color["name"] = self.myName.name("Black")
        color["rgb"]  = self.myName.name2rgb(color["name"])
        color["cmyk"]  = self.myName.name2cmyk(color["name"])
        color["hex"]  = self.myName.name2hex(color["name"])
        color["rgb100"]  = self.myName.lowerTo100(color["rgb"])
        color["rgb1"]    = self.myName.lowerTo1(color["rgb"])
        color["cmyk100"] = self.myName.lowerTo100(color["cmyk"])
        color["cmyk1"]   = self.myName.lowerTo1(color["cmyk"])
        return color

