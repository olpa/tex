#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

from time import time
from datetime import datetime

import xml.parsers.expat
import xml.etree.ElementTree as ET

from papersizes import PaperSizes
from messagebus import messageBus
from parsedefaults import parseDefaults
from sanitizeattributes import sanitizeAttributes

class myList():
    def union(self, list1, list2):
        return list1 + filter(lambda x:x not in list1, list2)

    def intersection(self, list1, list2):
        return filter(lambda x:x in list1, list2)

    def difference(self, list1, list2):
        return filter(lambda x:x not in list2, list1)

    def distinct(self, list1, list2):
        return filter (lambda x:x not in list2, list1) + filter(lambda x:x not in list1, list2)

class sanitize(myList, parseDefaults, sanitizeAttributes):
    """
This class parses a given bitplant template xml file instance
gives status messages, if desired
repairs, if desired
    """
    def __init__(self, infile=None, outfile=None, messagefile=None, printnotice=False, printwarning=False, printerror=True):
        sanitizeAttributes.__init__(self)
        parseDefaults.__init__(self, dir="../definitions/")
        #File handler
        self.infile = infile
        self.outfile = outfile

        #Initiate message bus
        self.mb = messageBus()
        #Set message file name
        self.mb.messagefile = messagefile

        #Set Message handler
        self.mb.printnotice = printnotice
        self.mb.printwarning = printwarning
        self.mb.printerror = printerror

        #Begin
        self.fileHandler()

    def result(self):
        if self.mb.testBreakExec() == True:
            return True
        else:
            return False

    def fileHandler(self):
        if self.mb.messagefile != None:
            #Write standard file header
            self.mb.log.append(_(u"Bitplant Template parser"))
            self.mb.log.append(_(u"Start time is:\t%s") % (str(datetime.now().isoformat())))
            #Open message file
            self.handle = open(self.mb.messagefile,"a")
            #Start testing for well formedness and validity
            self.__checkWrapper()
            #Close message file
            self.handle.write((" ".join(self.mb.log))+"\n")
            self.handle.close()
        else:
            #Start testing for well formedness and validity
            self.__checkWrapper()

    def __checkWrapper(self):
        #Test for given file
        if os.path.isfile(self.infile):
            self.mb.setMessage("notice", _(u"String %s points to a file") % self.infile)
        else:
            self.mb.setMessage("error", _(u"String %s does not point to a file") % self.infile)
        if self.mb.testBreakExec() == False:
            return False
        #Test with Expat if xml is well-formed
        if self.infile != None and len(self.infile) != 0:
            try:
                parser = xml.parsers.expat.ParserCreate()
                parser.ParseFile(open(self.infile, "r"))
                self.mb.setMessage("notice", _(u"File %s is well-formed.") % self.infile)
            except Exception, description:
                self.mb.setMessage("error", _(u"File %s is not well-formed: %s") % (self.infile, str(description)))
        else:
            self.mb.setMessage("error", _(u"No file specified"))
        if self.mb.testBreakExec() == False:
            return False
        #Test for validity
        self.sanitize()
        self.paramSort(self.newXml)
        self.prettyPrintXML(self.newXml)
        if self.outfile != None:
            tree = ET.ElementTree(self.newXml)
            tree.write(self.outfile, "UTF-8")

    def sanitize(self):
        #Load xml to check syntax with ElementTree
        ET._namespace_map["http://www.bitplant.de/template"] = "bit"
        try:
            self.xml = ET.parse(self.infile)
            self.mb.setMessage("notice", _(u"File %s is ready for sanitation") % self.infile)
        except Exception, description:
            self.mb.setMessage("error", _(u"File %s is not suitable for sanitation: %s") % (self.infile, str(description)))
        self.mb.testBreakExec()
        self.getRoot(self.xml)

    def getRoot(self, xml):
        #Identify the root element of the given xml and decide what to do
        root = xml.getroot()
        #Test for best case
        if root.tag == "{http://www.bitplant.de/template}designer":
            self.mb.setMessage("notice", _(u"Root element is designer"))
            #Start creating a beautified instance of the xml file
            self.newXml = ET.Element("{http://www.bitplant.de/template}designer")
            self.getDesigner(root, self.newXml)
        elif root.tag == "{http://www.bitplant.de/template}template":
            self.mb.setMessage("notice", _(u"Root element is template"))
            self.newXml = ET.Element("{http://www.bitplant.de/template}template")
            self.getDesigner(root, self.newXml)
        else:
            self.mb.setMessage("error", _(u"No valid root element found"))
        if self.mb.testBreakExec() == False:
            return False

#-------------------------------------------------------------------------------
# Methods to check structured elements
#-------------------------------------------------------------------------------
    def getDesigner(self, xml, sxml):
        self.saniRequiredCdata(xml, "name", sxml, self.defaults["designerName"])
        self.saniOptionalLang(xml, "lang", sxml, self.defaults["designerLang"])
        self.saniOptionalId(xml, "id", sxml)
        templates = xml.findall("{http://www.bitplant.de/template}template")
        if templates:
            for template in templates:
                stemplate = ET.SubElement(sxml, "{http://www.bitplant.de/template}template")
                self.getTemplate(template, stemplate)

    def getTemplate(self, xml, sxml):
        self.saniRequiredCdata(xml, "name", sxml, self.defaults["templateName"])
        self.saniOptionalLang(xml, "lang", sxml, self.defaults["templateLang"])
        self.saniOptionalId(xml, "id", sxml)
        parameter = xml.findall("{http://www.bitplant.de/template}parameter")
        if len(parameter) == 0:
            self.createNewTemplateParameter(sxml)
        else:
            sparameter = ET.SubElement(sxml, "{http://www.bitplant.de/template}parameter")
            self.getParameter(parameter[0], sparameter, "template")
        pages = xml.findall("{http://www.bitplant.de/template}page")
        for page in pages:
            spage = ET.SubElement(sxml, "{http://www.bitplant.de/template}page")
            self.getPage(page, spage)

    def getPage(self, xml, sxml):
        self.saniRequiredCdata(xml, "name", sxml, self.defaults["pageName"])
        self.saniOptionalLang(xml, "lang", sxml, self.defaults["pageLang"])
        self.saniOptionalId(xml, "id", sxml)
        self.saniOptionalEnum(xml, "inherit", ["enable", "disable"], sxml, self.defaults["pageInherit"])
        parameter = xml.findall("{http://www.bitplant.de/template}parameter")
        if len(parameter) == 0:
            self.createNewPageParameter(sxml)
        else:
            sparameter = ET.SubElement(sxml, "{http://www.bitplant.de/template}parameter")
            self.getParameter(parameter[0], sparameter, "page")
        frames = xml.findall("{http://www.bitplant.de/template}frame")
        for frame in frames:
            sframe = ET.SubElement(sxml, "{http://www.bitplant.de/template}frame")
            self.getFrame(frame, sframe)

    def getFrame(self, xml, sxml):
        self.saniRequiredCdata(xml, "name", sxml, self.defaults["frameName"])
        self.saniOptionalLang(xml, "lang", sxml, self.defaults["frameLang"])
        self.saniOptionalId(xml, "id", sxml)
        parameter = xml.findall("{http://www.bitplant.de/template}parameter")
        if len(parameter) == 0:
            self.createNewFrameParameter(sxml)
        else:
            sparameter = ET.SubElement(sxml, "{http://www.bitplant.de/template}parameter")
            self.getParameter(parameter[0], sparameter, "frame")
        contents = xml.findall("{http://www.bitplant.de/template}content")
        if len(contents) == 0:
            self.createNewContent(sxml)
        else:
            scontent = ET.SubElement(sxml, "{http://www.bitplant.de/template}content")
            self.getContent(contents[0], scontent)

    def getParameter(self, xml, sxml, position):
        self.getDescription(xml, sxml, position)
        self.saniDimPosLogic(xml, sxml, position)
        if position != "frame":
            self.getPaper(xml, sxml, position)
            self.saniPaperLogic(xml, sxml, position)

#-------------------------------------------------------------------------------
# Methods to check descriptive elements
#-------------------------------------------------------------------------------
    def getDescription(self, xml, sxml, position):
        descriptions = xml.findall("{http://www.bitplant.de/template}description")
        description = ET.SubElement(sxml, "{http://www.bitplant.de/template}description")
        #Check elements itself
        if len(description) == 0:
            description.text = self.defaults[position + "Description"]
        else:
            if descriptions[0].text:
                description.text = descriptions[0].text
            else:
                description.text = self.defaults[position + "Description"]

    def getPaper(self, xml, sxml, position):
        #Parse one paper element
        papers = xml.findall("{http://www.bitplant.de/template}paper")
        if len(papers) == 0:
            self.createNewPaper(sxml, position)
        else:
            defPaper = {}
            for paper in papers:
                if paper.get("type"):
                    if not defPaper.has_key(paper.get("type")):
                        defPaper[paper.get("type")] = paper
            for pap, val in defPaper.iteritems():
                spap = ET.SubElement(sxml, "{http://www.bitplant.de/template}paper")
                self.saniSetPaper(val, spap, "layout", ["oneside", "twoside"], position)
                paperSizes = PaperSizes()
                self.saniSetPaper(val, spap, "format", paperSizes.getAllowedSizes(), position)
                self.saniSetPaper(val, spap, "orientation", ["portrait", "landscape"], position)

    def getContent(self, xml, sxml):
        self.saniContentLogic(xml, sxml)
        if xml.text:
            sxml.text = xml.text
        else:
            sxml.text = self.defaults["contentText"]

#-------------------------------------------------------------------------------
# Methods to create xml structures from scratch
#-------------------------------------------------------------------------------
    def createNewPaper(self, sxml, position):
        defParam = self.defaultRoot.find(".//{http://www.bitplant.de/template}" + position + "/{http://www.bitplant.de/template}parameter")
        papers = defParam.findall("{http://www.bitplant.de/template}paper")
        for paper in papers:
            sxml.append(paper)

    def createNewTemplateParameter(self, sxml):
        templateParameter = self.defaultRoot.find(".//{http://www.bitplant.de/template}template/{http://www.bitplant.de/template}parameter")
        sxml.append(templateParameter)

    def createNewPageParameter(self, sxml):
        sxml.set("inherit", self.defaults["pageInherit"])
        pageParameter = self.defaultRoot.find(".//{http://www.bitplant.de/template}page/{http://www.bitplant.de/template}parameter")
        sxml.append(pageParameter)

    def createNewFrameParameter(self, sxml):
        frameParameter = self.defaultRoot.find(".//{http://www.bitplant.de/template}frame/{http://www.bitplant.de/template}parameter")
        sxml.append(frameParameter)

    def createNewContent(self, sxml):
        frameContent = self.defaultRoot.find(".//{http://www.bitplant.de/template}frame/{http://www.bitplant.de/template}content")
        sxml.append(frameContent)

    def paramSort(self, xml):
        #Sort the childs of the parameter element
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

    def prettyPrintXML(self, xml, level=0):
        #This function is from the effbot (http://effbot.org/zone/element-lib.htm)
        #It formats the xml output for pretty printing on ET versions lower 1.3
        i = "\n" + level*"\t"
        if len(xml):
            if not xml.text or not xml.text.strip():
                xml.text = i + "\t"
            if not xml.tail or not xml.tail.strip():
                xml.tail = i
            for xml in xml:
                self.prettyPrintXML(xml, level+1)
            if not xml.tail or not xml.tail.strip():
                xml.tail = i
        else:
            if level and (not xml.tail or not xml.tail.strip()):
                xml.tail = i

if __name__ == "__main__":
    if len(sys.argv) > 1:
        for file in sys.argv:
            if file != sys.argv[0]:
                newSanitizer = sanitize(file)
