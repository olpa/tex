#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from myhelper import myHelper
from x11colorvalues import x11colorValues

class myRgb(myHelper):
    """
This class defines contains all methods, 
that convert from rgb to another color space
    """
    def __init__(self):
        myHelper.__init__(self)
        self.rgbRe = re.compile( ur"\A(\s*)rgb(\s*)(\(?)(\s*)([\d]{,3}\s*%?)(\s*,?\s*)([\d]{,3}\s*%?)(\s*,?\s*)([\d]{,3}\s*%?)(\s*)(\)?)(\s*)\Z", re.UNICODE|re.IGNORECASE)

    def rgb(self, value):
        list = []
        for entry in re.findall(self.decValueRe, value):
            if entry != "" and re.match(ur"\A\s\Z", entry, re.UNICODE|re.IGNORECASE) == None:
                entry = self.stripWhitespace(entry)
                entry = self.convertPercent(entry)
                list.append(entry)
        list = self.validDecValue(list, 255)
        list = self.validList(list, 3)
        return tuple(list)

    def rgb100(self, value):
        return self.lowerTo100(value)

    def rgb1(self, value):
        return self.lowerTo1(value)

    def rgb2cmyk(self, rgb):
        return self.cmykByRgb(rgb)

    def rgb2hex(self, rgb):
        return self.hexByRgb(rgb)

    def rgb2name(self, rgb):
        for k, v in self.x11colorValues.iteritems():
            if v == self.rgb2hex(rgb):
                return str(k)
        return None
