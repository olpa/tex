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
from parseattributes import parseAttributes
from sanitize import sanitize

class myList():
    def union(self, list1, list2):
        return list1 + filter(lambda x:x not in list1, list2)

    def intersection(self, list1, list2):
        return filter(lambda x:x in list1, list2)

    def difference(self, list1, list2):
        return filter(lambda x:x not in list2, list1)

    def distinct(self, list1, list2):
        return filter (lambda x:x not in list2, list1) + filter(lambda x:x not in list1, list2)

class parse(myList, parseAttributes):
    """
This class parses a given bitplant template xml file instance
gives status messages, if desired
repairs, if desired
    """
    def __init__(self, infile = None, outfile = None, messagefile = None, printnotice = False, printwarning = False, printerror = True):
        parseAttributes.__init__(self)
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

        self.messageOpen()
        #Start testing for well formedness and validity
        self.__checkWrapper()
        #Test for validity
        self.validity()
        self.messageClose()
        #Write outfile
        if self.outfile != None:
            sanitizer(self.infile, self.outfile)

    def result(self):
        if self.mb.testBreakExec() == True:
            return True
        else:
            return False

    def messageOpen(self):
        if self.mb.messagefile != None:
            #Write standard file header
            self.mb.log.append(_(u"Bitplant Template parser"))
            self.mb.log.append(_(u"Start time is:\t%s") % (str(datetime.now().isoformat())))
            #Open message file
            self.handle = open(self.mb.messagefile,"a")

    def messageClose(self):
        if self.mb.messagefile != None:
            self.handle.write((" ".join(self.mb.log))+"\n")
            self.handle.close()

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
                self.mb.setMessage("notice", _(u"File %s is well-formed") % self.infile)
            except Exception, description:
                self.mb.setMessage("error", _(u"File %s is not well-formed: %s") % (self.infile, str(description)))
        else:
            self.mb.setMessage("error", _(u"No file specified"))
        if self.mb.testBreakExec() == False:
            return False
        else:
            return True

    def validity(self):
        #Load xml to check syntax with ElementTree
        ET._namespace_map["http://www.bitplant.de/template"] = "bit"
        try:
            self.xml = ET.parse(self.infile)
            self.mb.setMessage("notice", _(u"File %s is ready for validation") % self.infile)
        except Exception, description:
            self.mb.setMessage("error", _(u"File %s is not suitable for validation: %s") % (self.infile, str(description)))
        self.mb.testBreakExec()
        self.getRoot(self.xml)

    def getRoot(self, xml):
        """Identify the root element of the given xml and decide what to do
        This method breaks the parsing process, if namespace is missing or wrong
        
        If root element seems to be valid, the method is called, which is
        responsible for the found child element
        
        """
        root = xml.getroot()
        #Test for best case
        if root.tag == "{http://www.bitplant.de/template}designer":
            self.mb.setMessage("notice", _(u"Root element is designer"))
            self.getDesigner(root)
        elif root.tag == "{http://www.bitplant.de/template}template":
            self.mb.setMessage("notice", _(u"Root element is template"))
            self.getTemplate(root)
        #Test for lost namespace
        elif root.tag == "designer":
            self.mb.setMessage("error", _(u"There is no namespace given for root element designer"))
        elif root.tag == "template":
            self.mb.setMessage("error", _(u"There is no namespace given for root element template"))
        #Test for invalid namespace
        elif root.tag.rsplit("}")[-1] == "designer":
            self.mb.setMessage("error", _(u"Root element designer is not part of a valid namespace"))
        elif root.tag.rsplit("}")[-1] == "template":
            self.mb.setMessage("error", _(u"Root element template is not part of a valid namespace"))
        #Something other is seriously wrong
        else:
            self.mb.setMessage("error", _(u"No valid root element found"))
        if self.mb.testBreakExec() == False:
            return False

#-------------------------------------------------------------------------------
# Methods to check structured elements
#-------------------------------------------------------------------------------
    def getDesigner(self, xml):
        """This method checks for contents of a given designer element
        and calls getTemplate() if it includes template elements
        
        """
        self.checkRequiredCdata(xml, "name")
        self.checkOptionalLang(xml, "lang")
        self.checkOptionalId(xml, "id")
        self.checkPermission(xml, ["name", "lang", "id"])
        templates = xml.findall("{http://www.bitplant.de/template}template")
        if not templates:
            self.mb.setMessage("notice", _(u"Root element designer seems empty. No more relevant information"))
        else:
            for template in templates:
                self.getTemplate(template)

    def getTemplate(self, xml):
        #Parse the template element
        self.checkRequiredCdata(xml, "name")
        self.checkOptionalLang(xml, "lang")
        self.checkOptionalId(xml, "id")
        self.checkPermission(xml, ["name", "lang", "id"])
        parameter = xml.findall("{http://www.bitplant.de/template}parameter")
        if len(parameter) == 0:
            self.mb.setMessage("error", _(u"The element %s must contain exactly one element %s") % (xml.tag, "parameter"))
        elif len(parameter) > 1:
            self.mb.setMessage("error", _(u"The element %s must contain exactly one element %s") % (xml.tag, "parameter"))
        else:
            self.getTemplatePageParameter(parameter[0])
        pages = xml.findall("{http://www.bitplant.de/template}page")
        for page in pages:
            self.getPage(page)

    def getPage(self, xml):
        #Parse the template element
        self.checkRequiredCdata(xml, "name")
        self.checkOptionalLang(xml, "lang")
        self.checkOptionalId(xml, "id")
        self.checkOptionalEnum(xml, "inherit", ["enable", "disable"])
        self.checkPermission(xml, ["name", "lang", "id", "inherit"])
        parameter = xml.findall("{http://www.bitplant.de/template}parameter")
        if len(parameter) == 0:
            self.mb.setMessage("error", _(u"The element %s must contain exactly one element %s") % (xml.tag, "parameter"))
        elif len(parameter) > 1:
            self.mb.setMessage("error", _(u"The element %s must contain exactly one element %s") % (xml.tag, "parameter"))
        else:
            self.getTemplatePageParameter(parameter[0])
        frames = xml.findall("{http://www.bitplant.de/template}frame")
        for frame in frames:
            self.getFrame(frame)

    def getFrame(self, xml):
        #Parse the template element
        self.checkRequiredCdata(xml, "name")
        self.checkOptionalLang(xml, "lang")
        self.checkOptionalId(xml, "id")
        self.checkPermission(xml, ["name", "lang", "id"])
        parameter = xml.findall("{http://www.bitplant.de/template}parameter")
        if len(parameter) == 0:
            self.mb.setMessage("error", _(u"The element %s must contain exactly one element %s") % (xml.tag, "parameter"))
        elif len(parameter) > 1:
            self.mb.setMessage("error", _(u"The element %s must contain exactly one element %s") % (xml.tag, "parameter"))
        else:
            self.getFrameParameter(parameter[0])
        content = xml.findall("{http://www.bitplant.de/template}content")
        if len(content) == 0:
            self.mb.setMessage("error", _(u"The element %s must contain exactly one element %s") % (xml.tag, "content"))
        elif len(parameter) > 1:
            self.mb.setMessage("error", _(u"The element %s must contain exactly one element %s") % (xml.tag, "content"))
        else:
            self.getContent(xml)

    def getTemplatePageParameter(self, xml):
        self.getDescription(xml)
        self.getDimension(xml)
        self.getPosition(xml)
        self.checkDimPosLogic(xml)
        self.getPaper(xml)
        self.checkPaperLogic(xml)

    def getFrameParameter(self, xml):
        self.getDescription(xml)
        self.getDimension(xml)
        self.getPosition(xml)
        self.checkDimPosLogic(xml)

#-------------------------------------------------------------------------------
# Methods to check descriptive elements
#-------------------------------------------------------------------------------
    def getDescription(self, xml):
        description = xml.findall("{http://www.bitplant.de/template}description")
        if len(description) == 0:
            self.mb.setMessage("notice", _(u"The element %s includes no element %s") % (xml.tag, "description"))
        elif len(description) == 1:
            self.checkPermission(description[0], [])
        elif len(description) > 1:
            self.mb.setMessage("error", _(u"The element %s must contain only one element %s") % (xml.tag, "description"))

    def getDimension(self, xml):
        #Parse one dimension element
        dimension = xml.findall("{http://www.bitplant.de/template}dimension")
        if len(dimension) == 0:
            self.mb.setMessage("notice", _(u"The element %s includes no element %s") % (xml.tag, "dimension"))
            return
        elif len(dimension) > 2:
            self.mb.setMessage("error", _(u"The element %s must contain at least one and at most two elements %s") % (xml.tag, "dimension"))
        for dim in dimension:
            self.checkPermission(dim, ["unit", "type", "value"])
            self.checkRequiredEnum(dim, "type", ["width", "height"])
            self.checkRequiredRegExpCdata(dim, "value", ur"\A[0-9]{1,}(\.[0-9]{1,})?\Z")
            self.checkRequiredEnum(dim, "unit", ["mm", "cm", "inch", "pt"])

    def getPosition(self, xml):
        #General check for position elements
        position = xml.findall("{http://www.bitplant.de/template}position")
        if len(position) < 2:
            self.mb.setMessage("error", _(u"The element %s must contain at least two elements %s") % (xml.tag, "position"))
        elif len(position) > 4:
            self.mb.setMessage("error", _(u"The element %s must contain at least two and at most four elements %s") % (xml.tag, "position"))
        for pos in position:
            self.checkPermission(pos, ["unit", "type", "value"])
            self.checkRequiredEnum(pos, "type", ["top", "left", "right", "bottom"])
            self.checkRequiredRegExpCdata(pos, "value", ur"\A[0-9]{1,}(\.[0-9]{1,})?\Z")
            self.checkRequiredEnum(pos, "unit", ["mm", "cm", "inch", "pt"])

    def getPaper(self, xml):
        #Parse one paper element
        paper = xml.findall("{http://www.bitplant.de/template}paper")
        if len(paper) == 0:
            self.mb.setMessage("notice", _(u"The element %s includes no element %s") % (xml.tag, "paper"))
            return
        elif len(paper) > 3:
            self.mb.setMessage("error", _(u"The element %s must contain at least zero and at most three elements %s") % (xml.tag, "paper"))
        for pap in paper:
            self.checkPermission(pap, ["type", "value"])
            self.checkRequiredEnum(pap, "type", ["layout", "orientation", "format"])
            paperSizes = PaperSizes()
            self.checkRequiredEnum(pap, "value", ["portrait", "landscape", "oneside", "twoside"] + paperSizes.getAllowedSizes())

    def getContent(self, xml):
        content = xml.findall("{http://www.bitplant.de/template}content")
        #Check elements itself
        if len(content) == 0:
            self.mb.setMessage("error", _(u"The element %s includes no element %s") % (xml.tag, "content"))
        elif len(content) > 1:
            self.mb.setMessage("error", _(u"The element %s must contain only one element %s") % (xml.tag, "content"))
        for con in content:
            if not con.text:
                self.mb.setMessage("error", _(u"Element %s must not be empty") % (con.tag))
            self.checkContentLogic(con)
            self.checkPermission(con, ["angle", "type"])

if __name__ == "__main__":
    if len(sys.argv) > 1:
        for file in sys.argv:
            if file != sys.argv[0]:
                newParser = parse(file)
