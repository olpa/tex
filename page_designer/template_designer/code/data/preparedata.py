#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import re
import os
import sys
import shutil
import subprocess
from time import time
from StringIO import StringIO

from PIL import Image
import xml.etree.ElementTree as ET

class PrepareData():
    """This class writes the given temporary data into the xml object
    
    The prepareData class includes the functions to change the 
    assigned xml information of the derived class documentData.
    This class is intended to be used from class EditData.
    The functions are out sourced to get a better overview 
    on this important process
    
    """
    def __init__(self, parent, *args, **kwargs):
        self.parent = parent
        self.item = parent.document.GetSelection()
        if not self.item.IsOk():
            return
        self.xml = parent.document.GetItemPyData(self.item)
        if not self.xml:
            return

        self.tempItemData = parent.tempItemData

        #Start preparation of general information like name and value
        self.name(self.xml)
        self.description(self.xml)

        #Start preparation of content
        self.contentType(self.xml)
        self.contentRotation(self.xml)
        self.contentText(self.xml)
        self.contentRotationUndo(self.xml)
        self.contentColorTest(self.xml)
        self.contentImage(self.xml)

        #Start preparation of position and dimension values
        self.posDim(self.xml, "top", "position")
        self.posDim(self.xml, "left", "position")
        self.posDim(self.xml, "right", "position")
        self.posDim(self.xml, "bottom", "position")
        self.posDim(self.xml, "width", "dimension")
        self.posDim(self.xml, "height", "dimension")

        #Do the paper stuff
        self.paper(self.xml, "orientation")
        self.paper(self.xml, "layout")
        self.paper(self.xml, "format")

        #Do the page related stuff
        self.pageInheritance(self.xml)

        #Do some final layout stuff and write back to xml object
        self.beautifyValue(self.xml)
        self.paramSort(self.xml)

        parent.document.SetItemPyData(self.item, self.xml)

    def name(self, xml):
        if self.tempItemData.has_key("informationName"):
            xml.set("name", self.tempItemData["informationName"])

    def description(self, xml):
        if self.tempItemData.has_key("informationDescription"):
            xmlDesc = xml.find("{http://www.bitplant.de/template}parameter/{http://www.bitplant.de/template}description")
            if ET.iselement(xmlDesc):
                xmlDesc.text = self.tempItemData["informationDescription"]
            else:
                xmlDesc = ET.SubElement(xml.find("{http://www.bitplant.de/template}parameter"), "{http://www.bitplant.de/template}description")
                xmlDesc.text = self.tempItemData["informationDescription"]

    def contentType(self, xml):
        #Save content type
        if self.tempItemData.has_key("contentType"):
            xmlCont = xml.find("{http://www.bitplant.de/template}content")
            xmlCont.set("type", self.tempItemData["contentType"])

    def contentRotation(self, xml):
        #Save content rotation
        if self.tempItemData.has_key("contentAngle"):
            xmlCont = xml.find("{http://www.bitplant.de/template}content")
            xmlCont.set("angle", self.tempItemData["contentAngle"])

    def contentText(self, xml):
        #Save content
        if self.tempItemData.has_key("text"):
            xmlCont = xml.find("{http://www.bitplant.de/template}content")
            xmlCont.text = self.tempItemData["text"]

    def contentRotationUndo(self, xml):
        #It is currently not intended to rotate color and image contents.
        #Because that, angle is reseted for now, while these contents are active
        xmlCont = xml.find("{http://www.bitplant.de/template}content")
        if xmlCont:
            if xmlCont.get("type", "text") == "color" or xmlCont.get("type", "text") == "image":
                xmlCont.attrib["angle"] = "0"

    def contentColorTest(self, xml):
        #This is a test, if a color value is valid.
        xmlCont = xml.find("{http://www.bitplant.de/template}content")
        if xmlCont:
            if xmlCont.get("type", "text") == "color":
                cmykRe = re.compile( ur"\A(\s*)cmyk(\s*)(\(?)(\s*)([\d]{,3}\s*%?)(\s*,?\s*)([\d]{,3}\s*%?)(\s*,?\s*)([\d]{,3}\s*%?)(\s*,?\s*)([\d]{,3}\s*%?)(\s*)(\)?)(\s*)\Z", re.UNICODE|re.IGNORECASE)
                hexRe = re.compile( ur"\A(\s*)#(\s*)(\(?)(\s*)([\da-f]{2}\s*)(\s*,?\s*)([\da-f]{2}\s*)(\s*,?\s*)([\da-f]{2}\s*)(\s*)(\)?)(\s*)\Z", re.UNICODE|re.IGNORECASE)
                rgbRe = re.compile( ur"\A(\s*)rgb(\s*)(\(?)(\s*)([\d]{,3}\s*%?)(\s*,?\s*)([\d]{,3}\s*%?)(\s*,?\s*)([\d]{,3}\s*%?)(\s*)(\)?)(\s*)\Z", re.UNICODE|re.IGNORECASE)
                if re.match(rgbRe, xmlCont.text) == None and re.match(cmykRe, xmlCont.text) == None and re.match(hexRe, xmlCont.text) == None:
                    xmlCont.text = "cmyk(0, 0, 0, 255)"

    def contentImage(self, xml):
        #If content type is image, prepare the image and the xml
        xmlCont = xml.find("{http://www.bitplant.de/template}content")
        if ET.iselement(xmlCont):
            # The next comparision runs only really successfully 
            # if the contentType method ran before this method
            if xmlCont.get("type", "text") == "image" \
            and self.tempItemData.has_key("text"):
                if os.path.isfile(self.tempItemData["text"]):
                    axis = self.parent.getAxis_(self.item)
                    if axis == _(u"Client-Templates"):
                        dir = "clientImages"
                    elif axis == _(u"Server-Templates"):
                        dir = "serverImages"
                    else:
                        exit(_(u"Internal error while checking the current items position in tree"))

                    oriFilename = self.tempItemData["text"]
                    oriExtension = os.path.splitext(oriFilename)[1]
                    newFilename = str(int(time()))
                    REGEXP = re.compile(ur"\A.(pdf|eps|png|tiff)\Z", re.UNICODE|re.IGNORECASE)

                    if re.match(REGEXP, oriExtension):
                        xmlCont.text = dir + ":" + newFilename + oriExtension + ":" + os.path.basename(oriFilename)
                        try:
                            shutil.copyfile(oriFilename, self.__getImagePath() + "/" + newFilename + oriExtension)
                        except IOError:
                            exit(_(u"Internal error copying the current image"))
                    else:
                        try:
                            pil = Image.open(oriFilename).save(self.__getImagePath() + "/" + newFilename + ".png")
                            xmlCont.text = dir + ":" + newFilename + ".png:" + os.path.basename(oriFilename)
                        except:
                            print _(u"Internal error while converting image file into a suitable format. The image will not be available. Please use an external program like Preview to convert the image into a format like png or eps.")
                            dialog = wx.MessageDialog(None, _(u"Internal error while converting image file into a suitable format. The image will not be available. Please use an external program like Preview to convert the image into a format like png or eps."), _(u"Run Preview to change image format?"), wx.YES_NO|wx.YES_DEFAULT|wx.ICON_QUESTION)
                            decision = dialog.ShowModal()
                            dialog.Destroy()
                            if decision == wx.ID_YES:
                                cmd = ["open", "-a", "/Applications/Preview.app", oldFilename] 
                                subprocess.Popen(cmd)
                else:
                    print "sdfsdf"
                    #To be standard conform: Content must not be empty
                    xmlCont.text = _(u"no image selected")

    def __getImagePath(self):
        #This function moves the given image to the required directory, given by axis
        axis = self.parent.getAxis_(self.item)
        if axis == _(u"Client-Templates"):
            dir = self.parent.clientImages()
            return dir
        elif axis == _(u"Server-Templates"):
            dir = self.parent.serverImages()
            return dir
        else:
            exit(_(u"Internal error getting target path"))

    def pageInheritance(self, xml):
        # Disable or enable the pages inheritance
        if self.tempItemData.has_key("inheritance"):
            if self.tempItemData["inheritance"] == True:
                xml.set("inherit", "disable")
            else:
                xml.set("inherit", "enable")

    def paper(self, xml, kind):
        if self.tempItemData.has_key("paper" + kind.capitalize()):
            xmlElem = xml.findall("{http://www.bitplant.de/template}parameter/{http://www.bitplant.de/template}paper")
            count = False
            for elem in xmlElem:
                if elem.get("type") == kind:
                    count = True
                    elem.set("value", self.tempItemData["paper" + kind.capitalize()])
            if count == False:
                element = ET.SubElement(xml.find("{http://www.bitplant.de/template}parameter"), "{http://www.bitplant.de/template}paper")
                element.set("type", kind)
                element.set("value", self.tempItemData["paper" + kind.capitalize()])

    def __setPosDimElement(self, xml, type, kind):
        #Combine redundant actions
        xml.set("value", str(self.tempItemData[kind + type.capitalize()]))
        self.__measureUnit(xml, kind + type.capitalize() + "Unit")

    def __measureUnit(self, xml, topic):
        if self.tempItemData.has_key(topic):
            xml.set("unit", str(self.tempItemData[topic]))
        #This else here is ugly, because ElementTree does not recognize implied attribute values
        #Try to gather base unit selection instead
        else:
            control = self.parent.GetTopLevelParent().FindWindowByName("measureUnit")
            xml.set("unit", str(control.GetStringSelection()))

    def posDim(self, xml, type, kind):
        if self.tempItemData.has_key(str(kind + type.capitalize())):
            #Drop auto values
            if str(self.tempItemData[kind + type.capitalize()]) == "auto" \
            or str(self.tempItemData[kind + type.capitalize()]) == "":
                xmlPosDim = xml.find("{http://www.bitplant.de/template}parameter")
                if xmlPosDim:
                    for child in xmlPosDim.getiterator("{http://www.bitplant.de/template}" + kind):
                        if child.attrib["type"] == type:
                            xmlPosDim.remove(child)

            #Set modified value
            REGEXP = re.compile(ur"\d|\.", re.UNICODE|re.IGNORECASE)
            if re.match(REGEXP, str(self.tempItemData[kind + type.capitalize()])):
                xmlPosDim = xml.findall("{http://www.bitplant.de/template}parameter/{http://www.bitplant.de/template}" + kind)
                if not xmlPosDim:
                    element = ET.SubElement(xml.find("{http://www.bitplant.de/template}parameter"), "{http://www.bitplant.de/template}" + kind)
                    element.set("type", type)
                    self.__setPosDimElement(element, type, kind)
                else:
                    available = False
                    for child in xmlPosDim:
                        if child.get("type", None) == type:
                            available = True
                            self.__setPosDimElement(child, type, kind)
                    if available == False:
                        element = ET.SubElement(xml.find("{http://www.bitplant.de/template}parameter"), "{http://www.bitplant.de/template}" + kind)
                        element.set("type", type)
                        self.__setPosDimElement(element, type, kind)

        #If value not changed, but unit
        if self.tempItemData.has_key(str(kind + type.capitalize() + "Unit")):
            xmlPosDim = xml.findall("{http://www.bitplant.de/template}parameter/{http://www.bitplant.de/template}" + kind)
            for pd in xmlPosDim:
                if pd.get("type", None) == type:
                    self.__measureUnit(pd, kind + type.capitalize() + "Unit")

    def beautifyValue(self, xml):
        """Beautify "value" value
        
        This strips unnecessary zeros and points of right to left
        
        """
        xmlVal = xml.find("{http://www.bitplant.de/template}parameter")
        if xmlVal:
            for val in xmlVal:
                if "value" in val.keys():
                    if val.attrib["value"].count(".") > 0:
                        val.attrib["value"] = val.attrib["value"].rstrip("0").rstrip(".")

    def paramSort(self, xml):
        """Sort the children of the parameter element
        
        """
        xmlParam = xml.find("{http://www.bitplant.de/template}parameter")
        if xmlParam:
            order = ("description", "dimension", "position", "paper")
            sort = []
            for tag in order:
                elemC = xmlParam.findall("{http://www.bitplant.de/template}" + tag)
                if elemC:
                    for elem in elemC:
                        sort.append((tag, elem))
            xmlParam[:] = [item[-1] for item in sort]
