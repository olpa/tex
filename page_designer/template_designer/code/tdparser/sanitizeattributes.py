#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from langcode import langCode
from checkid import checkId
from time import time
import xml.etree.ElementTree as ET

class sanitizeAttributes:
    def __init__(self):
        #Tuple to store all id of xml
        self.idInStock = []

    def saniRequiredCdata(self, elem, attr, selem, default="some Value"):
        if elem.get(attr) == None:
            selem.set(attr, default)
        else:
            selem.set(attr, elem.get(attr))

    def saniRequiredEnum(self, elem, attr, enum, selem, default="some Value"):
        self.saniOptionalEnum(elem, attr, enum, selem, default)

    def saniOptionalEnum(self, elem, attr, enum, selem, default="some Value"):
        if elem.get(attr) == None:
            selem.set(attr, default)
        else:
            if elem.get(attr) in enum:
                selem.set(attr, elem.get(attr))
            else:
                selem.set(attr, default)

    def saniOptionalId(self, elem, attr, selem, default="id"+str(time()).replace(".", "")):
        if elem.get(attr) != None:
            id = checkId(elem.get(attr))
            if id.checkId() == True:
                if self.idInStock.count(elem.get(attr)) > 1:
                    selem.set(attr, default)
                else:
                    selem.set(attr, elem.get(attr))
            else:
                    selem.set(attr, default)
            self.idInStock.append(selem.get(attr))

    def saniOptionalLang(self, elem, attr, selem, default="en-EN"):
        if elem.get(attr) != None:
            lang = langCode(elem.get(attr))
            if lang.fullCheck() == True:
                selem.set(attr, elem.get(attr))
            else:
                selem.set(attr, default)

    def saniDimPosLogic(self, xml, sxml, position):
        dimension = xml.findall("{http://www.bitplant.de/template}dimension")
        position = xml.findall("{http://www.bitplant.de/template}position")
        #InternalCounter
        self.defDimPos = {}
        #Some mappings for comparison reasons
        allowedDimValues = ["width", "height"]
        allowedPosValues = ["top", "left", "right", "bottom"]
        allowedVerticalValues = ["height", "top", "bottom"]
        allowedHorizontalValues = ["width", "left", "right"]
        #Ignore duplicate dimensions and positions
        for posdim in self.union(dimension, position):
            if posdim.get("type"):
                if not self.defDimPos.has_key(posdim.get("type")):
                    self.defDimPos[posdim.get("type")] = posdim
                else:
                    break
        #Trim illegal values
        usefulValues = self.intersection(self.union(allowedVerticalValues, allowedHorizontalValues), self.defDimPos.keys())
        #Divide values in axis
        verticalValues = self.intersection(usefulValues, allowedVerticalValues)
        horizontalValues = self.intersection(usefulValues, allowedHorizontalValues)
        #Add vertical values
        if len(verticalValues) == 0:
            newHeight = ET.SubElement(sxml, "{http://www.bitplant.de/template}dimension")
            newHeight.set("type", "height")
            newHeight.set("value", self.defaults[position + "HeightValue"])
            newHeight.set("unit", self.defaults[position + "HeightUnit"])
            newTop = ET.SubElement(sxml, "{http://www.bitplant.de/template}position")
            newTop.set("type", "top")
            newTop.set("value", self.defaults[position + "TopValue"])
            newTop.set("unit", self.defaults[position + "TopUnit"])
        elif len(verticalValues)  == 1:
            if verticalValues[0] == "height":
                newHeight = ET.SubElement(sxml, "{http://www.bitplant.de/template}dimension")
                self.saniPosDim(self.defDimPos["height"], position, "width", ["mm", "cm", "pt", "inch"], newHeight)
                newTop = ET.SubElement(sxml, "{http://www.bitplant.de/template}position")
                newTop.set("type", "top")
                newTop.set("value", self.defaults[position + "TopValue"])
                newTop.set("unit", self.defaults[position + "TopUnit"])
            else:
                newHeight = ET.SubElement(sxml, "{http://www.bitplant.de/template}dimension")
                newHeight.set("type", "height")
                newHeight.set("value", self.defaults[position + "HeightValue"])
                newHeight.set("unit", self.defaults[position + "HeightUnit"])
        elif len(verticalValues)  > 1:
            newHeight = ET.SubElement(sxml, "{http://www.bitplant.de/template}dimension")
            self.saniPosDim(self.defDimPos["height"], position, "width", ["mm", "cm", "pt", "inch"], newHeight)
            newTop = ET.SubElement(sxml, "{http://www.bitplant.de/template}position")
            self.saniPosDim(self.defDimPos["top"], position, "width", ["mm", "cm", "pt", "inch"], newTop)

        #Add vertical values
        if len(horizontalValues) == 0:
            newWidth = ET.SubElement(sxml, "{http://www.bitplant.de/template}dimension")
            newWidth.set("type", "width")
            newWidth.set("value", self.defaults[position + "WidthValue"])
            newWidth.set("unit", self.defaults[position + "WidthUnit"])
            newLeft = ET.SubElement(sxml, "{http://www.bitplant.de/template}position")
            newLeft.set("type", "left")
            newLeft.set("value", self.defaults[position + "LeftValue"])
            newLeft.set("unit", self.defaults[position + "LeftUnit"])
        elif len(horizontalValues)  == 1:
            if horizontalValues[0] == "width":
                newWidth = ET.SubElement(sxml, "{http://www.bitplant.de/template}dimension")
                self.saniPosDim(self.defDimPos["width"], position, "width", ["mm", "cm", "pt", "inch"], newWidth)
                newLeft = ET.SubElement(sxml, "{http://www.bitplant.de/template}position")
                newLeft.set("type", "left")
                newLeft.set("value", self.defaults[position + "LeftValue"])
                newLeft.set("unit", self.defaults[position + "LeftUnit"])
            else:
                newWidth = ET.SubElement(sxml, "{http://www.bitplant.de/template}dimension")
                newWidth.set("type", "width")
                newWidth.set("value", self.defaults[position + "WidthValue"])
                newWidth.set("unit", self.defaults[position + "WidthUnit"])
        elif len(horizontalValues)  > 1:
            newWidth = ET.SubElement(sxml, "{http://www.bitplant.de/template}dimension")
            self.saniPosDim(self.defDimPos["width"], position, "width", ["mm", "cm", "pt", "inch"], newWidth)
            newLeft = ET.SubElement(sxml, "{http://www.bitplant.de/template}position")
            self.saniPosDim(self.defDimPos["left"], position, "width", ["mm", "cm", "pt", "inch"], newLeft)

    def saniPosDim(self, elem, kind, type, unit_enum, selem):
        selem.set("type", elem.get("type"))
        if elem.get("unit") in unit_enum:
            selem.set("unit", elem.get("unit", "mm"))
            if re.match(ur"\A[0-9]{1,}(\.[0-9]{1,})?\Z", elem.get("value"), re.UNICODE):
                selem.set("value", elem.get("value"))
            else:
                selem.set("value", self.defaults[kind + type.capitalize() + "Value"])
        else:
            selem.set("unit", self.defaults[kind + type.capitalize() + "Unit"])
            if re.match(ur"\A[0-9]{1,}(\.[0-9]{1,})?\Z", elem.get("value"), re.UNICODE):
                selem.set("value", elem.get("value"))
            else:
                selem.set("value", self.defaults[kind + type.capitalize() + "Value"])

    def saniPaperLogic(self, xml, sxml, position):
        spapers = sxml.findall("{http://www.bitplant.de/template}paper")
        if len(spapers) != 3:
            defsPaper = []
            for paper in spapers:
                defsPaper.append(paper.get("type"))
            inter = self.difference(["layout", "format", "orientation"], defsPaper)
            for type in inter:
                spap = ET.SubElement(sxml, "{http://www.bitplant.de/template}paper")
                spap.set("type", type)
                spap.set("value", self.defaults[position + type.capitalize() + "Value"])

    def saniSetPaper(self, elem, selem, type, enum, position):
        if elem.get("type") == type:
            selem.set("type", elem.get("type"))
            if elem.get("value") in enum:
                selem.set("value", elem.get("value"))
            else:
                selem.set("value", self.defaults[position + type.capitalize() + "Value"])

    def saniContentLogic(self, elem, selem):
        self.saniRequiredEnum(elem, "type", ["image", "color", "text", "vartext"], selem, self.defaults["contentType"])
        self.saniOptionalEnum(elem, "angle", ["0", "90", "180", "270"], selem, self.defaults["contentType"])
