#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from myhelper import myHelper
from x11colorvalues import x11colorValues

class myHex(myHelper):
    """
This class defines contains all methods, 
that convert from hex to another color space
    """
    def __init__(self):
        myHelper.__init__(self)
        self.hexRe = re.compile( ur"\A(\s*)#(\s*)(\(?)(\s*)([\da-f]{2}\s*)(\s*,?\s*)([\da-f]{2}\s*)(\s*,?\s*)([\da-f]{2}\s*)(\s*)(\)?)(\s*)\Z", re.UNICODE|re.IGNORECASE)

    def hex(self, value):
        list = []
        for entry in re.findall(self.hexValueRe, value):
            if entry != "" and re.match(ur"\A\s\Z", entry, re.UNICODE|re.IGNORECASE) == None:
                entry = self.stripWhitespace(entry)
                list.append(entry)
        h = str()
        for entry in list:
            h += entry.upper()
        return str("#" + h)

    def hex2rgb(self, hex):
        return self.rgbByHex(hex)

    def hex2cmyk(self, hex):
        return self.cmykByRgb(self.hex2rgb(hex))

    def hex2name(self, hex):
        for k, v in self.x11colorValues.iteritems():
            if v == hex:
                return str(k)
        return None
