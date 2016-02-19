#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
import re

from papersizes import PaperSizes

class parseDefaults():
    def __init__(self, dir="."):
        self.defaults = {}
        ET._namespace_map["http://www.bitplant.de/template"] = "bit"
        self.defaultXml = ET.parse(dir + "/" + "default.xml")
        self.defaultRoot = self.defaultXml.getroot()
        self.setDefaultDesigner()
        self.setDefaultTemplate()
        self.setDefaultPage()
        self.setDefaultFrame()
        self.setDefaultContent()
        self.paperSizes = PaperSizes()

    def setDefaultDesigner(self):
        designer = self.defaultRoot
        self.defaults["designerName"] = designer.get("name", "Designer")
        self.defaults["designerLang"] = designer.get("lang", "en-EN")

    def setDefaultTemplate(self):
        template = self.defaultRoot.find(".//{http://www.bitplant.de/template}template")
        self.defaults["templateName"] = template.get("name", "Template")
        self.defaults["templateLang"] = template.get("lang", "en-EN")
        templateDescription = template.find(".//{http://www.bitplant.de/template}description")
        if templateDescription.text:
            self.defaults["templateDescription"] = templateDescription.text
        else:
            self.defaults["templateDescription"] = "This is a Description"

        templatePaper = template.findall(".//{http://www.bitplant.de/template}paper")
        #Get paper defaults from default file
        for paper in templatePaper:
            if paper.get("type") == "layout": 
                if paper.get("value") in ["oneside", "twoside"]:
                    self.defaults["templateLayoutValue"] = paper.get("value", "oneside")
            if paper.get("type") == "orientation":
                if paper.get("value") in ["portrait", "landscape"]:
                    self.defaults["templateOrientationValue"] = paper.get("value", "portrait")
            if paper.get("type") == "format":
                if paper.get("value") in self.paperSizes.getAllowedSizes():
                    self.defaults["templateFormatValue"] = paper.get("value", "a4")
        #If default file is not fully populated with paper values
        self.addFallbackDefault("templateLayoutValue", "oneside")
        self.addFallbackDefault("templateOrientationValue", "portrait")
        self.addFallbackDefault("templateFormatValue", "a4")

        templateDimension = template.findall(".//{http://www.bitplant.de/template}dimension")
        for dim in templateDimension:
            self.iterAddDimPos(dim, "template", "height", ["mm", "cm", "pt", "inch"])
            self.iterAddDimPos(dim, "template", "width", ["mm", "cm", "pt", "inch"])
        self.addFallbackDefault("templateHeightUnit", "mm")
        self.addFallbackDefault("templateHeightValue", "240")
        self.addFallbackDefault("templateWidthUnit", "mm")
        self.addFallbackDefault("templateWidthValue", "175")

        templatePosition = template.findall(".//{http://www.bitplant.de/template}position")
        for pos in templatePosition:
            self.iterAddDimPos(pos, "template", "top", ["mm", "cm", "pt", "inch"])
            self.iterAddDimPos(pos, "template", "left", ["mm", "cm", "pt", "inch"])
            self.iterAddDimPos(pos, "template", "right", ["mm", "cm", "pt", "inch"])
            self.iterAddDimPos(pos, "template", "bottom", ["mm", "cm", "pt", "inch"])
        self.addFallbackDefault("templateTopUnit", "mm")
        self.addFallbackDefault("templateTopValue", "35")
        self.addFallbackDefault("templateLeftUnit", "mm")
        self.addFallbackDefault("templateLeftValue", "25")
        self.addFallbackDefault("templateRightUnit", "mm")
        self.addFallbackDefault("templateRightValue", "10")
        self.addFallbackDefault("templateBottomUnit", "mm")
        self.addFallbackDefault("templateBottomValue", "22")

    def iterAddDimPos(self, elem, kind, type, unit_enum):
        if elem.get("type") == type:
            if elem.get("unit") in unit_enum:
                self.defaults[kind + type.capitalize() + "Unit"] = elem.get("unit", "mm")
                if re.match(ur"\A[0-9]{1,}(\.[0-9]{1,})?\Z", elem.get("value"), re.UNICODE):
                    self.defaults[kind + type.capitalize() + "Value"] = elem.get("value")
            else:
                if re.match(ur"\A[0-9]{1,}(\.[0-9]{1,})?\Z", elem.get("value"), re.UNICODE):
                    self.defaults[kind + type.capitalize() + "Value"] = elem.get("value")

    def addFallbackDefault(self, type, value):
        if not self.defaults.has_key(type):
            self.defaults[type] = value

    def setDefaultPage(self):
        page = self.defaultRoot.find(".//{http://www.bitplant.de/template}page")
        self.defaults["pageName"] = page.get("name", "Page")
        self.defaults["pageLang"] = page.get("lang", "en-EN")
        self.defaults["pageInherit"] = page.get("inherit", "enable")
        pageDescription = page.find(".//{http://www.bitplant.de/template}description")
        if pageDescription.text:
            self.defaults["pageDescription"] = pageDescription.text
        else:
            self.defaults["pageDescription"] = "This is a Description"

        pagePaper = page.findall(".//{http://www.bitplant.de/template}paper")
        #Get paper defaults from default file
        for paper in pagePaper:
            if paper.get("type") == "layout":
                if paper.get("value") in ["oneside", "twoside"]:
                    self.defaults["pageLayoutValue"] = paper.get("value", "oneside")
            if paper.get("type") == "orientation":
                if paper.get("value") in ["portrait", "landscape"]:
                    self.defaults["pageOrientationValue"] = paper.get("value", "portrait")
            if paper.get("type") == "format":
                if paper.get("value") in self.paperSizes.getAllowedSizes():
                    self.defaults["pageFormatValue"] = paper.get("value", "a4")
        #If default file is not fully populated with paper values
        self.addFallbackDefault("pageLayoutValue", "oneside")
        self.addFallbackDefault("pageOrientationValue", "portrait")
        self.addFallbackDefault("pageFormatValue", "a4")

        pageDimension = page.findall(".//{http://www.bitplant.de/template}dimension")
        for dim in pageDimension:
            self.iterAddDimPos(dim, "page", "height", ["mm", "cm", "pt", "inch"])
            self.iterAddDimPos(dim, "page", "width", ["mm", "cm", "pt", "inch"])
        self.addFallbackDefault("pageHeightUnit", "mm")
        self.addFallbackDefault("pageHeightValue", "240")
        self.addFallbackDefault("pageWidthUnit", "mm")
        self.addFallbackDefault("pageWidthValue", "175")

        pagePosition = page.findall(".//{http://www.bitplant.de/template}position")
        for pos in pagePosition:
            self.iterAddDimPos(pos, "page", "top", ["mm", "cm", "pt", "inch"])
            self.iterAddDimPos(pos, "page", "left", ["mm", "cm", "pt", "inch"])
            self.iterAddDimPos(pos, "page", "right", ["mm", "cm", "pt", "inch"])
            self.iterAddDimPos(pos, "page", "bottom", ["mm", "cm", "pt", "inch"])
        self.addFallbackDefault("pageTopUnit", "mm")
        self.addFallbackDefault("pageTopValue", "35")
        self.addFallbackDefault("pageLeftUnit", "mm")
        self.addFallbackDefault("pageLeftValue", "25")
        self.addFallbackDefault("pageRightUnit", "mm")
        self.addFallbackDefault("pageRightValue", "10")
        self.addFallbackDefault("pageBottomUnit", "mm")
        self.addFallbackDefault("pageBottomValue", "22")

    def setDefaultFrame(self):
        frame = self.defaultRoot.find(".//{http://www.bitplant.de/template}frame")
        self.defaults["frameName"] = frame.get("name", "Frame")
        self.defaults["frameLang"] = frame.get("lang", "en-EN")
        frameDescription = frame.find(".//{http://www.bitplant.de/template}description")
        if frameDescription.text:
            self.defaults["frameDescription"] = frameDescription.text
        else:
            self.defaults["frameDescription"] = "This is a Description"

    def setDefaultContent(self):
        content = self.defaultRoot.find(".//{http://www.bitplant.de/template}content")
        self.defaults["contentType"] = content.get("type", "color")
        self.defaults["contentAngle"] = content.get("angle", "0")
        if content.text:
            self.defaults["contentText"] = content.text
        else:
            self.defaults["contentText"] = "cmyk(0,0,0,0)"
