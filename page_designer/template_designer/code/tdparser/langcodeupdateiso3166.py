#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import urllib
import zipfile

class updateIso3166:

    def __init__(self, file=None):
        data = self.http()
        self.write(data, file)

    def http(self):
        file = urllib.urlretrieve("http://www.iso.org/iso/iso_3166-1_list_en.zip")[0]
        zf = zipfile.ZipFile(file)
        zippedFile = zf.namelist()[0]
        return str(zf.read(zippedFile))
    
    def write(self, data, file=None, getString=True):
        if file != None:
            handle = open(file,"w")
            handle.write(data)
            handle.close()
        else:
            print data
        if getString == True:
            return data

if __name__ == "__main__":
    if len(sys.argv) > 1:
        for file in sys.argv:
            if file != sys.argv[0]:
                iso = updateIso3166(file)
            else:
                iso = updateIso3166()
