#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

from papersizes import PaperSizes
from langcode import langCode
from checkid import checkId

class parseAttributes:
    def __init__(self):
        #Tuple to store all id of xml
        self.idInStock = []

    def checkPermission(self, elem, enum):
        """
This method checks, if a given element has an element which is not in enumeration
        """
        for attr in elem.keys():
            if not attr in enum:
                self.mb.setMessage("error", _(u"The attribute %s is not permitted at element %s. Permitted attributes are %s") % (attr, elem.tag, ", ".join(enum)))

    def checkRequiredEnum(self, elem, attr, enum):
        """
Handle a required direct child attribute with a enumeration of possible values
elem is a ElementTree element instance
attr is the name of the required attribute, string
enum is a list or tuple of possible values for attr
        """
        if elem.get(attr) == None:
            self.mb.setMessage("error", _(u"Element %s must contain the attribute %s") % (elem.tag, attr))
        else:
            if not elem.get(attr) in enum:
                self.mb.setMessage("error", _(u"The value of attribute %s must be of %s") % (attr, ", ".join(enum)))

    def checkOptionalEnum(self, elem, attr, enum):
        """
Handle a optional direct child attribute with a enumeration of possible values
elem is a ElementTree element instance
attr is the name of the required attribute, string
enum is a list or tuple of possible values for attr
        """
        if elem.get(attr) == None:
            self.mb.setMessage("notice", _(u"Element %s has no optional attribute %s") % (elem.tag, attr))
        else:
            self.mb.setMessage("notice", _(u"Element %s has optional attribute %s with value %s") % (elem.tag, attr, elem.get(attr)))
            if elem.get(attr) not in enum:
                self.mb.setMessage("error", _(u"The value of attribute %s must be of %s") % (attr, ", ".join(enum)))

    def checkRequiredRegExpCdata(self, elem, attr, regexp):
        """
Handle a optional direct child attribute with a enumeration of possible values
elem is a ElementTree element instance
attr is the name of the required attribute, string
regexp is a a regular expression to match the attributes value, string
        """
        if elem.get(attr) == None:
            self.mb.setMessage("error", _(u"Element %s must contain the attribute %s") % (elem.tag, attr))
        else:
            if not re.match(regexp, elem.get(attr), re.UNICODE|re.IGNORECASE):
                self.mb.setMessage("error", _(u"The value of attribute %s in element %s must be a valid decimal") % (attr, elem.tag))

    def checkRequiredCdata(self, elem, attr):
        """
Handle a required direct child attribute of type CData
elem is a ElementTree element instance
attr is the name of the required attribute, string
        """
        if elem.get(attr) == None:
            self.mb.setMessage("error", _(u"Element %s must contain the attribute %s") % (elem.tag, attr))
        else:
            self.mb.setMessage("notice", _(u"Element %s has attribute %s with value %s") % (elem.tag, attr, elem.get(attr)))

    def checkOptionalId(self, elem, attr):
        """
Handle a optional direct child attribute of type ID. Compares the value of 
attr with the rules defined in XML 1.0 (Fourth Edition) Recommendation

elem is a ElementTree element instance
attr is the name of the optional attribute, string
        """
        if elem.get(attr) == None:
            self.mb.setMessage("notice", _(u"Element %s has no optional attribute %s") % (elem.tag, attr))
        else:
            self.mb.setMessage("notice", _(u"Element %s has optional attribute %s with value %s") % (elem.tag, attr, elem.get(attr)))
            id = checkId(elem.get(attr))
            if id.checkId() == True:
                self.mb.setMessage("notice", _(u"Value %s of attribute %s in element %s accords to XML 1.0 (Fourth Edition) Recommendation") % (elem.get(attr), attr, elem.tag))
                if self.idInStock.count(elem.get(attr)) > 1:
                    self.mb.setMessage("error", _(u"Value %s of attribute %s in element %s is already existent. %s values must be unique") % (elem.get(attr), attr, elem.tag, attr))
                else:
                    self.idInStock.append(elem.get(attr))
            else:
                self.mb.setMessage("error", _(u"Value %s of attribute %s in element %s does not accord to XML 1.0 (Fourth Edition) Recommendation") % (elem.get(attr), attr, elem.tag))

    def checkOptionalLang(self, elem, attr):
        """
Handle a optional direct child attribute of type LANG. Compares the value of 
attr with the rules defined in RFC3066, Iana, Iso639 or Iso3166 specifications

elem is a ElementTree element instance
attr is the name of the optional attribute, string
        """
        if elem.get(attr) == None:
            self.mb.setMessage("notice", _(u"Element %s has no optional attribute %s") % (elem.tag, attr))
        else:
            self.mb.setMessage("notice", _(u"Element %s has optional attribute %s with value %s") % (elem.tag, attr, elem.get(attr)))
            lang = langCode(elem.get(attr))
            if lang.formalCheck() == True:
                self.mb.setMessage("notice", _(u"Value %s of attribute %s in element %s accords to RFC3066") % (elem.get(attr), attr, elem.tag))
                if lang.fullCheck() == True:
                    self.mb.setMessage("notice", _(u"Value %s of attribute %s in element %s accords to RFC3066, Iana, Iso639 or Iso3166 specifications") % (elem.get(attr), attr, elem.tag))
                else:
                    self.mb.setMessage("warning", _(u"Value %s of attribute %s in element %s does not accord to RFC3066, Iana, Iso639 or Iso3166 specifications") % (elem.get(attr), attr, elem.tag))
            else:
                self.mb.setMessage("error", _(u"Value %s of attribute %s in element %s does not accord to RFC3066") % (elem.get(attr), attr, elem.tag))

    def checkDependendEnum(self, elem, attrib1_name, attrib1_value, attrib2_name, attrib2_enum):
        """
Handle a to attribute siblings. This function shall check for something 
simiilar to a co-constraint. It get's an attribute with a value and a second
attribute name with an enumeration. Then it checks, if value of attribute one 
is x, so value of attribute y must be in the enumeration.
elem is a ElementTree element instance
attr1_name is a string defining the name of the first attribute
attrib1_value is a string defining the value of the first attribute
attr2_name is a string defining the name of the second attribute
attr2_value is a list or tuple defining all possible values of attribute two, 
depend on attribute value one
        """
        if elem.get(attrib1_name) and elem.get(attrib2_name):
            if elem.get(attrib1_name) == attrib1_value and not elem.get(attrib2_name) in attrib2_enum:
                self.mb.setMessage("warning", _(u"The value of attribute %s does not correspondent to the value of attribute %s in a logical manner. \n\tAttribute %s with value %s recommends a value of %s for attribute %s") % (attrib1_name, attrib2_name, attrib1_name, type, ", ".join(attrib2_enum), attrib2_name))

    def checkDimPosLogic(self, xml):
        """
This method checks, if the given types of the position and dimension elements 
are used in a convenient way. It evaluates the use of attribute values which
describe the vertical and horizontal compass of the parent element and warns
if something is wrong. Problems there can be the over- and/or unde defining
of the vertical or horizontal axis
        """
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
        if len(self.defDimPos) != len(self.union(dimension, position)):
            self.mb.setMessage("warning", _(u"Duplicate value attribution of attribute %s within the children of element %s") % ("type", xml.tag))
        #Trim illegal values
        usefulValues = self.intersection(self.union(allowedVerticalValues, allowedHorizontalValues), self.defDimPos.keys())
        #Divide values in axis
        verticalValues = self.intersection(usefulValues, allowedVerticalValues)
        horizontalValues = self.intersection(usefulValues, allowedHorizontalValues)
        #Add vertical values
        if len(verticalValues) == 0:
            self.mb.setMessage("warning", _(u"The vertical axis of element %s is under defined. An element of type of %s is missing") % (xml.tag, ", ".join(allowedVerticalValues)))
        elif len(verticalValues)  == 1:
            self.mb.setMessage("warning", _(u"The vertical axis of element %s is under defined. An element of type of %s is missing") % (xml.tag, ", ".join(allowedVerticalValues)))
        elif len(verticalValues)  > 2:
            self.mb.setMessage("warning", _(u"The vertical axis of element %s is over defined. An element of type of %s hangs over") % (xml.tag, ", ".join(allowedVerticalValues)))
        #Add vertical values
        if len(horizontalValues) == 0:
            self.mb.setMessage("warning", _(u"The horizontal axis of element %s is under defined. An element of type of %s is missing") % (xml.tag, ", ".join(allowedVerticalValues)))
        elif len(horizontalValues)  == 1:
            self.mb.setMessage("warning", _(u"The horizontal axis of element %s is under defined. An element of type of %s is missing") % (xml.tag, ", ".join(allowedVerticalValues)))
        elif len(horizontalValues)  > 2:
            self.mb.setMessage("warning", _(u"The horizontal axis of element %s is over defined. An element of type of %s hangs over") % (xml.tag, ", ".join(allowedHorizontalValues)))

    def checkPaperLogic(self, xml):
        """
This method checks, if the given types of the paper elements are 
used in a convenient way.
        """
        paper = xml.findall("{http://www.bitplant.de/template}paper")
        #InternalCounter
        self.defPaper = {}
        #Ignore duplicate attributions in element paper
        for pap in paper:
            if pap.get("type"):
                if not self.defPaper.has_key(pap.get("type")):
                    self.defPaper[pap.get("type")] = pap
                else:
                    break
        if len(self.defPaper) != len(paper):
            self.mb.setMessage("warning", _(u"Duplicate value attribution of attribute %s within the children of element %s") % ("type", xml.tag))
        paperSizes = PaperSizes()
        for pap in paper:
            self.checkDependendEnum(pap, "type", "layout", "value", ["oneside", "twoside"])
            self.checkDependendEnum(pap, "type", "format", "value", paperSizes.getAllowedSizes())
            self.checkDependendEnum(pap, "type", "orientation", "value", ["portrait", "landscape"])

    def checkContentLogic(self, xml):
        self.checkRequiredEnum(xml, "type", ["image", "color", "text", "vartext"])
        self.checkOptionalEnum(xml, "angle", ["0", "90", "180", "270"])
