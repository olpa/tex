#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import openanything

class updateIso639:

    def __init__(self, file=None):
        rawData = self.http()
        data = self.translate(rawData)
        self.write(data, file)

    def http(self):
        return openanything.openAnything("http://www.loc.gov/standards/iso639-2/ISO-639-2_utf-8.txt").read()

    def translate(self, rawData):
        REGEXP1 = re.compile(ur"\n", re.UNICODE|re.IGNORECASE)
        splitData = re.split(REGEXP1, rawData) 
        new = []
        new.append("""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>""")
        new.append("""<ISO_639_List xml:lang="en">""")
        for line in splitData:
            new.append("\t<ISO_639_Entry>")
            REGEXP2 = re.compile("\|")
            entry = re.split(REGEXP2, line)
            if len(entry[0]) != 0:
                new.append("\t\t<ISO_639-2_Alpha-3_Bibliographic_Code_element>" + entry[0] + "</ISO_639-2_Alpha-3_Bibliographic_Code_element>")
            if len(entry[1]) != 0:
                new.append("\t\t<ISO_639-2_Alpha-3_Terminologic_Code_element>" + entry[1] + "</ISO_639-2_Alpha-3_Terminologic_Code_element>")
            if len(entry[2]) != 0:
                new.append("\t\t<ISO_639-1_Alpha-2_Code_element>" + entry[2] + "</ISO_639-1_Alpha-2_Code_element>")
            if len(entry[3]) != 0:
                new.append("\t\t<ISO_639-2_Language_name_en>" + entry[3] + "</ISO_639-2_Language_name_en>")
            if len(entry[4]) != 0:
                new.append("\t\t<ISO_639-2_Language_name_fr>" + entry[4] + "</ISO_639-2_Language_name_fr>")
            new.append("\t</ISO_639_Entry>")
        new.append("</ISO_639_List>")
        return new
    
    def write(self, data, file=None, getString=True):
        if file != None:
            handle = open(file,"w")
            for i in data:
                handle.write(i + "\n")
            handle.close()
        else:
            for i in data:
                print i
        if getString == True:
            dataString = unicode("")
            for i in data:
                dataString += (i + "\n")
            return dataString

if __name__ == "__main__":
    if len(sys.argv) > 1:
        for file in sys.argv:
            if file != sys.argv[0]:
                iso = updateIso639(file)
            else:
                iso = updateIso639()
