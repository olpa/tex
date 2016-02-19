#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from x11colorvalues import x11colorValues

class myHelper:

    """
This class provides helper functions to convert between different color spaces. 
The classes myCmyk, myHex, myName and myRgb are derived from this class
    """

    def __init__(self):
        self.x11colorValues = x11colorValues.get
        self.decValueRe = re.compile( ur"[\d]{,3}\s*%?", re.UNICODE|re.IGNORECASE)
        self.hexValueRe = re.compile( ur"[\da-f]{2}", re.UNICODE|re.IGNORECASE)
        self.nameValueRe = re.compile(ur"\A( *)" + self.getReX11colors() + "( *)\Z", re.UNICODE|re.IGNORECASE)

    def getReX11colors(self):
        s = str("(")
        for k, v in self.x11colorValues.iteritems():
                s += str(k) + "|"
        s = s.rstrip("|") + ")"
        return str(s)

    def stripWhitespace(self, value):
        if re.match(ur"\s", value, re.UNICODE|re.IGNORECASE) == None:
            return str(value)
        value = value.replace(" ","")
        value = value.replace("\t","")
        value = value.replace("\n","")
        value = value.replace("\r","")
        value = value.replace("\f","")
        value = value.replace("\v","")
        return str(value)

    def convertPercent(self, value):
        if re.match(ur"%", value, re.UNICODE|re.IGNORECASE) == None:
            return int(value)
        value = int(value.replace("%",""))
        value = (255 * value) / 100
        return value

    def validDecValue(self, list, max):
        validlist = []
        for entry in list:
            if entry >= 0 and entry <= max:
                validlist.append(entry)
        return validlist

    def validList(self, list, count):
        if len(list) == count:
            return list
        elif len(list) > count:
            return list[:count]
        list.append(0)
        self.validList(list, count)
        return list

    def cmykByRgb(self, rgb):
        r, g , b = rgb
        c, m, y = (1 - r / 255.0,1 - g / 255.0,1 - b / 255.0)
        C, M, Y, K = (c - min(c, m, y), m - min(c, m, y), y - min(c, m, y), min(c, m, y))
        return tuple(map (lambda proportion: int(proportion * 255), [C, M, Y, K]))

    def rgbByHex(self, hex):
        value = eval("0x" + hex.replace("#", ""))
        r = (value & 0xFF0000) / 0x10000
        g = (value & 0x00FF00) / 0x100
        b = (value & 0x0000FF)
        return tuple((r, g, b))

    def hexByRgb(self, rgb):
        h = str()
        for c in rgb:
            i = hex(c).replace("0x", "")
            if len(i) == 1:
                h += "0" + i
            else:
                h += i
        return str("#" + h.upper())

    def lowerTo100(self, value):
        list = []
        for entry in value:
            list.append((100 * int(entry)) / 255)
        return tuple(list)

    def lowerTo1(self, value):
        list = []
        for entry in value:
            list.append(float(entry) / 255)
        return tuple(list)
