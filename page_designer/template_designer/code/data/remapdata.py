#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET

class RemapData:
    """If xml data was modified through drag&drop or delete, the 
    classes method remapData tries to sort the co-relative xml again
    
    """
    def __init__(self, *args, **kwargs):
        pass

    def remapData(self):
        root = self.document.GetRootItem()
        for axis in self.getChildren_(root):
            for item in self.getChildren_(axis):
                #Start remapping
                self.__setRoot(item)

    def __setRoot(self, item):
        if self.identifyMyItem_(item) == "designer":
            self.document.SetItemPyData(item, self.__setDesigner(item))
        elif self.identifyMyItem_(item) == "template":
            self.document.SetItemPyData(item, self.__setTemplate(item))

    def __setDesigner(self, item):
        data = self.document.GetItemPyData(item)
        designer = ET.Element("{http://www.bitplant.de/template}designer")
        self.__setIdentify(data, designer)
        self.__setFilename(data, designer)
        if self.document.ItemHasChildren(item) == True:
            for child in self.getChildren_(item):
                designer.append(self.__setTemplate(child))
        return designer

    def __setTemplate(self, item):
        data = self.document.GetItemPyData(item)
        template = ET.Element("{http://www.bitplant.de/template}template")
        self.__setIdentify(data, template)
        self.__setFilename(data, template)
        self.__setParameter(data, template)
        if self.document.ItemHasChildren(item) == True:
            for child in self.getChildren_(item):
                template.append(self.__setPage(child))
        return template

    def __setPage(self, item):
        data = self.document.GetItemPyData(item)
        page = ET.Element("{http://www.bitplant.de/template}page")
        self.__setIdentify(data, page)
        self.__setInheritance(data, page)
        self.__setParameter(data, page)
        if self.document.ItemHasChildren(item) == True:
            for child in self.getChildren_(item):
                page.append(self.__setFrame(child))
        return page

    def __setFrame(self, item):
        data = self.document.GetItemPyData(item)
        frame = ET.Element("{http://www.bitplant.de/template}frame")
        self.__setIdentify(data, frame)
        self.__setParameterFrame(data, frame)
        self.__setContent(data, frame)
        return frame

    def __setContent(self, oldData, newData):
        for content in oldData.findall("{http://www.bitplant.de/template}content"):
            newData.append(content)
        return newData

    def __setIdentify(self, oldData, newData):
        if oldData.get("name", None) != None:
            newData.attrib["name"] = oldData.attrib["name"]
        if oldData.get("id", None) != None:
            newData.attrib["id"] = oldData.attrib["id"]
        if oldData.get("lang", None) != None:
            newData.attrib["lang"] = oldData.attrib["lang"]

    def __setFilename(self, oldData, newData):
        if hasattr(oldData, "filename"):
            newData.filename = oldData.filename

    def __setInheritance(self, oldData, newData):
        if oldData.get("inherit", None) != None:
            newData.attrib["inherit"] = oldData.attrib["inherit"]

    def __setParameter(self, oldData, newData):
        parameter = ET.Element("{http://www.bitplant.de/template}parameter")
        for description in oldData.findall("{http://www.bitplant.de/template}parameter/{http://www.bitplant.de/template}description"):
            parameter.append(description)
        for dimension in oldData.findall("{http://www.bitplant.de/template}parameter/{http://www.bitplant.de/template}dimension"):
            parameter.append(dimension)
        for position in oldData.findall("{http://www.bitplant.de/template}parameter/{http://www.bitplant.de/template}position"):
            parameter.append(position)
        for paper in oldData.findall("{http://www.bitplant.de/template}parameter/{http://www.bitplant.de/template}paper"):
            parameter.append(paper)
        newData.append(parameter)
        return newData

    def __setParameterFrame(self, oldData, newData):
        parameter = ET.Element("{http://www.bitplant.de/template}parameter")
        for description in oldData.findall(".//{http://www.bitplant.de/template}description"):
            parameter.append(description)
        for dimension in oldData.findall(".//{http://www.bitplant.de/template}dimension"):
            parameter.append(dimension)
        for position in oldData.findall(".//{http://www.bitplant.de/template}position"):
            parameter.append(position)
        newData.append(parameter)
        return newData
