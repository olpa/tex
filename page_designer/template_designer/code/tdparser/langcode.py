#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import re

import xml.etree.ElementTree as ET

REGEXP_FORMAL = re.compile(ur"\A([a-zA-Z]{2}|[a-zA-Z]{3}|[iI{1}|[xX]{1})(-[a-zA-Z0-9]{2}|-[a-zA-Z0-9]{3,8})*\Z", re.UNICODE)
"""
This comment explains the preceeding regular expression "formal"
\A            begin of string
(                    language code
[a-zA-Z]{2}          ISO 639 part 1
|                    or
[a-zA-Z]{3}          ISO 639 part 2
|                    or
[iI]{1}              IANA-defined registration
|                    or
[xX]{1}              Private registration
)
(                    country code
-                    RFC3066
[a-zA-Z0-9]{2}       ISO 3166 alpha-2
|                    or
-                    RFC3066
[a-zA-Z0-9]{3,8}     IANA-defined registration
)
*                 Unlimited detailation
\Z    end of string
"""

class langCode():
    """
This class checks, if a given string is compatible to the RFC3066.
This RFC is relevant while validating the xml:lang attribute value
    """
    def __init__(self, lang=None, dir=None):
        self.lang = lang
        if dir == None:
            path = os.path.split(os.path.abspath(os.path.dirname(sys.modules[__name__].__file__)))[0]
            self.defDir = path + "/definitions"
        else:
            self.defDir = dir
        self.defFileIana = "iana.xml"
        self.defFileIso639 = "iso639.xml"
        self.defFileIso3166 = "iso3166.xml"

    def check(self, lang=None):
        """
Do a normal test. This includes a simple syntax check 
and a test, if given language and country code is valid
        """
        if lang == None:
            lang = self.lang
        if self.formalCheck(lang) == True:
            return self.fullCheck(lang)
        else:
            return False

    def updateLangCodes(self, dir="."):
        from update_iana import updateIana
        from update_iso3166 import updateIso3166
        from update_iso639 import updateIso639

        updateIana(dir + self.defFileIana)
        updateIso3166(dir + self.defFileIso3166)
        updateIso639(dir + self.defFileIso639)

    def formalCheck(self, lang=None):
        if lang == None:
            lang = self.lang
        if re.match(REGEXP_FORMAL, lang):
            return True
        else:
            return False

    def fullCheck(self, lang=None):
        if lang == None:
            lang = self.lang
        divide = re.split(ur"-", lang)
        languageCode = self.setLanguageCode(divide[0])

        if languageCode == False:
            return False

        elif languageCode == "private":
            if len(divide) <= 1:
                return False
            else:
                privateSubTag = re.compile(ur"\A([a-zA-Z0-9]{2,8})*\Z", re.UNICODE)
                for i in range(1, len(divide)):
                    if re.match(privateSubTag, divide[i]):
                        return True
                    else:
                        return False

        elif languageCode in ["iso639_1", "iso639_2"]:
            if len(divide) <= 1:
                return True
            else:
                isoSubTag = []
                for i in range(1, len(divide)):
                     isoSubTag.append(self.setIso3166(divide[i], self.defDir))
                if isoSubTag.count(False) == 0:
                    return True
                else:
                    return False

        elif languageCode == "iana":
            if len(divide) <= 1:
                return True
            else:
                iana = unicode("")
                for i in range(1, len(divide)):
                    iana += divide[i] + "-"
                iana = iana.rstrip("-")
                ianaSubTag = self.setIanaCountry(iana, self.defDir)
                if ianaSubTag == True:
                    return True
                else:
                    return False

        else:
            return False

    def setLanguageCode(self, lang=None):
        if lang == None:
            lang = self.lang
        iso639_1    = re.compile(ur"\A[a-zA-Z]{2}\Z", re.UNICODE)
        iso639_2    = re.compile(ur"\A[a-zA-Z]{3}\Z", re.UNICODE)
        ianaLang    = re.compile(ur"\A[iI]{1}\Z", re.UNICODE)
        privateLang = re.compile(ur"\A[xX]{1}\Z", re.UNICODE)

        if re.match(iso639_1, lang):
            return self.setIso639_1(lang, self.defDir)
        elif re.match(iso639_2, lang):
            return self.setIso639_2(lang, self.defDir)
        elif re.match(ianaLang, lang):
            return "iana"
        elif re.match(privateLang, lang):
            return "private"
        else:
            return False

    def setIso639_1(self, lang=None, dir="."):
        if lang == None:
            lang = self.lang
        list = []
        xml = ET.parse(dir + "/" + self.defFileIso639)
        root = xml.getroot()
        find = root.findall(".//ISO_639-1_Alpha-2_Code_element")
        for code in find:
            list.append(code.text.lower())
        if lang.lower() in list:
            return "iso639_1"
        else:
            return False

    def setIso639_2(self, lang=None, dir="."):
        if lang == None:
            lang = self.lang
        list = []
        xml = ET.parse(dir + "/" + self.defFileIso639)
        root = xml.getroot()
        find = root.findall(".//ISO_639-2_Alpha-3_Bibliographic_Code_element")
        for code in find:
            list.append(code.text.lower())
        find = root.findall(".//ISO_639-2_Alpha-3_Terminologic_Code_element")
        for code in find:
            list.append(code.text.lower())
        if lang.lower() in list:
            return "iso639_2"
        else:
            return False

    def setIso3166(self, lang=None, dir="."):
        if lang == None:
            lang = self.lang
        list = []
        xml = ET.parse(dir + "/"+ self.defFileIso3166)
        root = xml.getroot()
        find = root.findall(".//ISO_3166-1_Alpha-2_Code_element")
        for code in find:
            list.append(code.text.lower())
        if lang.lower() in list:
            return True
        else:
            return False

    def setIanaCountry(self, lang=None, dir="."):
        if lang == None:
            lang = self.lang
        list = []
        xml = ET.parse(dir + "/" + self.defFileIana)
        root = xml.getroot()
        find = root.findall(".//Tag")
        for code in find:
            list.append(code.text.lower())
        find = root.findall(".//Subtag")
        for code in find:
            list.append(code.text.lower())
        if lang.lower() in list:
            return True
        else:
            return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        for lang in sys.argv:
            if lang != sys.argv[0]:
                #Some self testing
                lang = langCode(lang)
                #lang.updateLangCodes(".")
                print lang.check()
