#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import re
import sys
import copy
import os.path
import subprocess
from StringIO import StringIO

from PIL import Image
import xml.etree.ElementTree as ET

from tdparser.papersizes import PaperSizes
from colors import colors

class DrawData:
    def __init__(self, parent):
        self.parent = parent
        self.frame = self.parent
        self.tree = self.frame.document
        self.item = self.tree.GetSelection()
        self.data = self.tree.GetItemPyData(self.item)

        self.paperSizes = PaperSizes()

    def countUp(self, item, count=0, layout="oneside"):
        if self.tree.GetChildrenCount(item, False) > 0:
            if self.tree.GetRootItem() == item \
            or self.tree.GetItemText(item) == _(u"Client-Templates") \
            or self.tree.GetItemText(item) == _(u"Server-Templates"):
                children = self.listChildren(item)
                for child in children:
                    count += self.countUp(child)
                return count
            xml = self.tree.GetItemPyData(item)
            if xml.tag.rsplit("}")[-1] == "designer":
                children = self.listChildren(item)
                for child in children:
                    count += self.countUp(child)
                return count
            if xml.tag.rsplit("}")[-1] == "template":
                children = self.listChildren(item)
                for child in children:
                    paper = xml.findall("{http://www.bitplant.de/template}parameter/{http://www.bitplant.de/template}paper")
                    for layout in paper:
                        default = "oneside"
                        if layout.get("type") == "layout":
                            default = layout.get("value")
                            break
                    count += self.countUp(child, default)
                return count
            if xml.tag.rsplit("}")[-1] == "page":
                if xml.get("inherit", "enable") == "disable" and layout == "oneside":
                    paper = xml.findall("{http://www.bitplant.de/template}parameter/{http://www.bitplant.de/template}paper")
                    for layout in paper:
                        default = "oneside"
                        if layout.get("type") == "layout":
                            if layout.get("value") == "oneside":
                                return 1
                            else:
                                return 2
                            break
                elif xml.get("inherit", "enable") == "enable" and layout == "oneside":
                    return 1
                if xml.get("inherit", "enable") == "disable" and layout == "twoside":
                    paper = xml.findall("{http://www.bitplant.de/template}parameter/{http://www.bitplant.de/template}paper")
                    for layout in paper:
                        default = "oneside"
                        if layout.get("type") == "layout":
                            if layout.get("value") == "oneside":
                                return 1
                            else:
                                return 2
                            break
                elif xml.get("inherit", "enable") == "enable" and layout == "twoside":
                    return 2
            return count
        else:
            try:
                xml = self.tree.GetItemPyData(item)
                xml.tag
            except:
                return count
            if xml.tag.rsplit("}")[-1] == "frame":
                parent = self.tree.GetItemParent(item)
                return self.countUp(parent)
            else:
                return count

    def listChildren(self, parent):
        list = []
        if self.tree.ItemHasChildren(parent):
            cookie = 0
            (item, cookie) = self.tree.GetFirstChild(parent)
            while item.IsOk():
                list.append(item)
                (item, cookie) = self.tree.GetNextChild(parent, cookie)
        return list

    def totalPages(self):
        if not self.item.IsOk():
            return
        return self.countUp(self.item)

    def listPages(self, item, list=[]):
        if self.tree.GetRootItem() == item:
            for child in self.listChildren(item):
                self.listPages(child, list)
        elif self.tree.GetItemText(item) == _(u"Client-Templates") \
        or self.tree.GetItemText(item) == _(u"Server-Templates"):
            for child in self.listChildren(item):
                self.listPages(child, list)
        else:
            xml = self.tree.GetItemPyData(item)
            if xml.tag.rsplit("}")[-1] == "designer":
                for child in self.listChildren(item):
                    self.listPages(child, list)
            if xml.tag.rsplit("}")[-1] == "template":
                for child in self.listChildren(item):
                    list.append(self.listPages(child, list))
            if xml.tag.rsplit("}")[-1] == "page":
                return item
            if xml.tag.rsplit("}")[-1] == "frame":
                parent = self.tree.GetItemParent(item)
                list.append(self.listPages(parent, list))
        return list

    def getPageData(self, pageNum):
        if not self.item.IsOk():
            return
        list = self.listPages(self.item, list=[])
        tmplist = []
        if hasattr(list, "__iter__"):
            for item in list:
                tmplist.append(item)
        else:
            tmplist.append(list)
        del list
        #Check kind of page
        pageList = []
        for item in tmplist:
            xml = self.tree.GetItemPyData(item)
            parent = self.tree.GetItemParent(item)
            parentXml = self.tree.GetItemPyData(parent)
            if xml.tag.rsplit("}")[-1] == "page":
                if self.getPageInherit(xml) == "enable":
                    if self.getPaperLayout(parentXml) == "oneside":
                        xml.flip = "noflip"
                        xml = parentXml
                        pageList.append(xml)
                    else:
                        xml.flip = "noflip"
                        xml = parentXml
                        pageList.append(xml)
                        xml2 = copy.deepcopy(xml)
                        xml2.flip = "flip"
                        xml2 = parentXml
                        pageList.append(xml2)
                else:
                    if self.getPaperLayout(xml) == "oneside":
                        xml.flip = "noflip"
                        pageList.append(xml)
                    else:
                        xml.flip = "noflip"
                        pageList.append(xml)
                        xml2 = copy.deepcopy(xml)
                        xml2.flip = "flip"
                        xml2 = parentXml
                        pageList.append(xml2)
        return pageList[pageNum - 1]

    def getPaperLayout(self, xml):
        paper = xml.findall("{http://www.bitplant.de/template}parameter/{http://www.bitplant.de/template}paper")
        for layout in paper:
            if layout.get("type") == "layout":
                return layout.get("value")
        return "oneside"

    def getPageInherit(self, xml):
        if xml.get("inherit", "enable") == "enable":
            return "enable"
        return "disable"

    def preparePageData(self, xml):
        parameter = xml.find("{http://www.bitplant.de/template}parameter")
        if hasattr(xml, "parent"):
            #Inheritance was enabled, so overwrite parameters with template paramters
            position = parameter.findall("{http://www.bitplant.de/template}position")
            for pos in position:
                parameter.remove(pos)
            position = xml.findall("{http://www.bitplant.de/template}parameter/{http://www.bitplant.de/template}position")
            for pos in position:
                parameter.append(pos)
            dimension = parameter.findall("{http://www.bitplant.de/template}dimension")
            for dim in dimension:
                parameter.remove(dim)
            dimension = xml.findall("{http://www.bitplant.de/template}parameter/{http://www.bitplant.de/template}dimension")
            for dim in dimension:
                parameter.append(dim)

    def drawPageData(self, xml, dc, logUnits):
        self.preparePageData(xml)

        #set font
        dc.SetFont(wx.Font(9, wx.FONTFAMILY_SWISS, wx.NORMAL, wx.NORMAL))
        dc.SetTextForeground(wx.Colour(0,0,0,0))

        #main frame
        rectangle = self.convertFrameData(xml, dc)
        penclr   = wx.Colour(228, 228, 228, 228)
        brushclr = wx.Colour(228, 228, 228, 228)
        dc.SetPen(wx.Pen(penclr))
        dc.SetBrush(wx.Brush(brushclr))
        dc.DrawRectangleRect(rectangle)

        #other frames
        frames = xml.findall("{http://www.bitplant.de/template}frame")
        for frame in frames:
            x, y, w, h = self.convertFrameData(frame, dc)
            rectangle = wx.Rect(x, y, w, h)
            content = frame.find("{http://www.bitplant.de/template}content")
            if content.get("type") == "color":
                myColor=colors(content.text)
                r, g, b = myColor.getRgb()
                brushclr = wx.Colour(r, g, b, 255)
                penclr   = wx.Colour(r, g, b, 255)
                dc.SetBrush(wx.Brush(brushclr))
                dc.SetPen(wx.Pen(penclr))
                dc.DrawRectangleRect(rectangle)

            if content.get("type") == "text" or content.get("type") == "vartext":
                text = content.text
                text = text.replace("\\t", "\t")

                penclr   = wx.Colour(128, 128, 128)
                dc.SetBrush(wx.TRANSPARENT_BRUSH)
                dc.SetPen(wx.Pen(penclr))
                dc.DrawRectangleRect(rectangle)

                brushclr = wx.Colour(0, 0, 0, 255)
                penclr   = wx.Colour(0, 0, 0, 255)
                dc.SetBrush(wx.Brush(brushclr))
                dc.SetPen(wx.Pen(penclr))
                dc.SetLayoutDirection(2)
                angle = int(content.get("angle", 0))
                if angle == 270:
                    angle = 90
                    y = y + h
                elif angle == 90:
                    angle = 270
                elif angle == 180:
                    x = x + w
                    y = y + h
                dc.DrawRotatedText(content.text, x, y, angle)
                dc.SetLayoutDirection(0)

            if content.get("type") == "image":
                penclr   = wx.Colour(128, 128, 128)
                dc.SetBrush(wx.TRANSPARENT_BRUSH)
                dc.SetPen(wx.Pen(penclr))
                dc.DrawRectangleRect(rectangle)

                dir = self.__getDir(content)
                if not content.text:
                    return True
                if content.text.count(":") == 2:
                    file = content.text.split(":")[1]
                    orifile = content.text.split(":")[2]
                    if os.path.isfile(dir + "/" + file):
                        bmp = self.getPreview(dir + "/" + file)
                        if bmp != None:
                            dc.DrawBitmap(bmp, x, y)

    def __getDir(self, xmlText):
        if xmlText.text:
            dir = xmlText.text.split(":")[0]
            if dir == "clientImages":
                return self.frame.clientImages()
            elif dir == "serverImages":
                return self.frame.serverImages()
            else:
                return ""
        else:
            return ""

    def __convertPdfEps2Png(self, file):
        sys.path.append("/Library/Frameworks/Python.framework/Versions/Current/bin")
        sys.path.append("/opt/local/bin")
        sys.path.append("/opt/local/sbin")
        sys.path.append("/usr/bin")
        sys.path.append("/bin")
        sys.path.append("/usr/sbin")
        sys.path.append("/sbin")
        sys.path.append("/usr/local/bin")
        sys.path.append("/usr/texbin")
        sys.path.append("/usr/X11/bin")

        cmd = ["gs-noX11", "-q", "-dQUIET", "-dBATCH", "-dNOPAUSE", "-sDEVICE=png16m", "-sOutputFile=%stdout", file]
        process = subprocess.Popen(cmd, env={"PATH": ":".join(sys.path)}, stdout=subprocess.PIPE)
        file = StringIO(process.stdout.read()) 
        if process.wait() != 0: 
            raise Exception(_(u"Internal Ghostscript error while preparing preview image"))
        return file

    def getPreview(self, file):
        REGEXP = re.compile(ur"\A.(pdf|eps)\Z", re.UNICODE|re.IGNORECASE)
        if re.match(REGEXP, os.path.splitext(file)[1]):
            file = self.__convertPdfEps2Png(file)
        try:
            pil = Image.open(file)
        except:
            return None
        try:
            pil.thumbnail((600, 128))
        except:
            return None
        wxi = wx.EmptyImage(pil.size[0],pil.size[1])
        wxi.SetData(pil.convert("RGB").tostring())
        wxi.SetAlphaData(pil.convert("RGBA").tostring()[3::4])
        bmp = wx.BitmapFromImage(wxi)
        return bmp

    def convertToPoint(self, value, unit):
        if unit == "mm":
            return int( float(value) * (float(360) / float(127)) )
        if unit == "cm":
            return int( float(value) * (float(3600) / float(127)) )
        if unit == "point":
            return int(float(value))
        if unit == "inch":
            return int(float(value) * float(72))

    def convertFrameData(self, xml, dc):
        #Gets an ElementTree instance and a 2-tuple of mm values as size of dc
        #Returns an wx.Rect instance
        totalWidth, totalHeight = dc.GetSize()
        calc = {}
        parameter = xml.find("{http://www.bitplant.de/template}parameter")
        dimension = parameter.findall("{http://www.bitplant.de/template}dimension")
        for dim in dimension:
            if dim.get("type") == "height":
                calc["height"] = self.convertToPoint(dim.get("value", 10), dim.get("unit", "mm"))
            elif dim.get("type") == "width":
                calc["width"] = self.convertToPoint(dim.get("value", 10), dim.get("unit", "mm"))

        position = parameter.findall("{http://www.bitplant.de/template}position")
        for pos in position:
            if pos.get("type") == "top":
                calc["top"] = self.convertToPoint(pos.get("value", 10), pos.get("unit", "mm"))
            elif pos.get("type") == "left":
                calc["left"] = self.convertToPoint(pos.get("value", 10), pos.get("unit", "mm"))
            elif pos.get("type") == "right":
                calc["right"] = self.convertToPoint(pos.get("value", 10), pos.get("unit", "mm"))
            elif pos.get("type") == "bottom":
                calc["bottom"] = self.convertToPoint(pos.get("value", 10), pos.get("unit", "mm"))

        #Define missing values positions
        if calc.has_key("top") and calc.has_key("bottom"):
            calc["height"] = totalHeight - calc["bottom"] - calc["top"]
        elif calc.has_key("top") and calc.has_key("height"):
            calc["bottom"] = calc["top"] + calc["height"]
        elif calc.has_key("bottom") and calc.has_key("height"):
            calc["top"] = totalHeight - calc["bottom"] - calc["height"]

        if calc.has_key("left") and calc.has_key("right"):
            calc["width"] = totalWidth - calc["right"] - calc["left"]
        elif calc.has_key("left") and calc.has_key("width"):
            calc["right"] = calc["left"] + calc["width"]
        elif calc.has_key("right") and calc.has_key("width"):
            calc["left"] = totalWidth - calc["bottom"] - calc["width"]

        dimpos = []
        dimpos.append(calc["left"])
        dimpos.append(calc["top"])
        dimpos.append(calc["width"])
        dimpos.append(calc["height"])
        return dimpos

    def getOrientation(self, xml):
        #set default
        ori = "portrait"
        if hasattr(xml, "parent"):
            #Inheritance was enabled, so overwrite paramters with template paramters
            parameter = xml.find("{http://www.bitplant.de/template}parameter")
            paper = parameter.findall("{http://www.bitplant.de/template}paper")
            for pap in paper:
                if pap.get("type") == "orientation":
                    ori = pap.get("value")
        else:
            parameter = xml.find("{http://www.bitplant.de/template}parameter")
            paper = parameter.findall("{http://www.bitplant.de/template}paper")
            for pap in paper:
                if pap.get("type") == "orientation":
                    ori = pap.get("value")
        if ori == "portrait":
            return(wx.PORTRAIT)
        else:
            return(wx.LANDSCAPE)

    def getPaperSize(self, xml):
        paperSpecs = self.paperSizes.getAll()
        #set default
        format = "a4"
        if hasattr(xml, "parent"):
            #Inheritance was enabled, so overwrite paramters with template paramters
            parameter = xml.find("{http://www.bitplant.de/template}parameter")
            paper = parameter.findall("{http://www.bitplant.de/template}paper")
            for pap in paper:
                if pap.get("type") == "format":
                    format = pap.get("value")
        else:
            parameter = xml.find("{http://www.bitplant.de/template}parameter")
            paper = parameter.findall("{http://www.bitplant.de/template}paper")
            for pap in paper:
                if pap.get("type") == "orientation":
                    format = pap.get("value")
        if format in paperSpecs:
            return paperSpecs[format]
