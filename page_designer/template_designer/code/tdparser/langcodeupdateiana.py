#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import openanything

class updateIana():

    def __init__(self, file=None):
        rawData = self.http()
        data = self.translate(rawData)
        self.write(data, file)

    def http(self):

        return openanything.openAnything("http://www.iana.org/assignments/language-subtag-registry").read()

    def translate(self, rawData):
        REGEXP1 = re.compile(ur"%%", re.UNICODE|re.IGNORECASE)
        splitData = re.split(REGEXP1, rawData) 
        new = []
        new.append("""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>""")
        new.append("""<Iana_List xml:lang="en">""")
        splitData.pop(0)
        for line in splitData:
            new.append("\t<Iana_Entry>")
            REGEXP2 = re.compile(ur"(\n[-_a-zA-Z0-9]{1,}: )")
            entry = re.split(REGEXP2, line)
            for i in range(0, len(entry)):
                if i % 2 == 1:
                    new.append("\t\t<" + entry[i].replace("\n", "").replace(": ", "") + ">" + entry[i + 1].replace("\n", "").replace("  ", " ") + "</" + entry[i].replace("\n", "").replace(": ", "") + ">")
            new.append("\t</Iana_Entry>")
        new.append("</Iana_List>")
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
                iana = updateIana(file)
            else:
                iana = updateIana()

