#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from myhelper import myHelper
from x11colorvalues import x11colorValues

class myName(myHelper):

    """
This class defines contains all methods, 
that convert from x11 color name to another color space
    """

    def __init__(self):
        myHelper.__init__(self)
        self.nameRe = re.compile(ur"\A( *)" + self.getReX11colors() + "( *)\Z", re.UNICODE|re.IGNORECASE)

    def name(self, value):
        value = value.strip()
        for k, v in self.x11colorValues.iteritems():
            if k.lower() == value.lower():
                return str(k)
        return None

    def name2rgb(self, name):
        return self.rgbByHex(self.name2hex(name))

    def name2cmyk(self, name):
        return self.cmykByRgb(self.name2rgb(name))

    def name2hex(self, name):
        for k, v in self.x11colorValues.iteritems():
            if k == name:
                return str(v)
        return None
