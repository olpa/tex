#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from myhelper import myHelper
from x11colorvalues import x11colorValues

class myCmyk(myHelper):

    """
This class defines contains all methods, 
that convert from cmyk to another color space
    """

    def __init__(self):
        myHelper.__init__(self)
        self.cmykRe = re.compile( ur"\A(\s*)cmyk(\s*)(\(?)(\s*)([\d]{,3}\s*%?)(\s*,?\s*)([\d]{,3}\s*%?)(\s*,?\s*)([\d]{,3}\s*%?)(\s*,?\s*)([\d]{,3}\s*%?)(\s*)(\)?)(\s*)\Z", re.UNICODE|re.IGNORECASE)

    def cmyk(self, value):
        list = []
        for entry in re.findall(self.decValueRe, value):
            if entry != "" and re.match(ur"\A\s\Z", entry, re.UNICODE|re.IGNORECASE) == None:
                entry = self.stripWhitespace(entry)
                entry = self.convertPercent(entry)
                list.append(entry)
        list = self.validDecValue(list, 255)
        list = self.validList(list, 4)
        return tuple(list)

    def cmyk100(self, value):
        return self.lowerTo100(value)

    def cmyk1(self, value):
        return self.lowerTo1(value)

    def cmyk2rgb(self, cmyk):
        #PostScript® Language Reference, Third Edition, chapter 7.2.4, page 477, [http://www.adobe.com/products/postscript/pdfs/PLRM.pdf]
        c, m, y, k = cmyk
        def convert(color, key):
            return 255 - min(255, color + key)
        return tuple((convert(c, k), convert(m, k), convert(y, k)))

    def cmyk2hex(self, cmyk):
        return self.hexByRgb(self.cmyk2rgb(cmyk))

    def cmyk2name(self, cmyk):
        for k, v in self.x11colorValues.iteritems():
            if v == self.cmyk2hex(cmyk):
                return str(k)
        return None
