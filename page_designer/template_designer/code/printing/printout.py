#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx

from drawdata import DrawData

import xml.etree.ElementTree as ET
class Printout(wx.Printout):
    def __init__(self, parent, *args, **kwargs):
        wx.Printout.__init__(self, *args, **kwargs)
        self.drawData = DrawData(parent)

    def OnPreparePrinting(self):
        dc = self.GetDC()
        self.numPages = self.drawData.totalPages()
        return True

    def OnBeginPrinting(self):
        return True

    def OnBeginDocument(self, startPage, endPage):
        """
        startPage and endPage are integer values, 
        describing the start and end page of the document to print
        """
        return super(Printout, self).OnBeginDocument(startPage, endPage)

    def OnPrintPage(self, pageNum):
        """
        pageNum is an integer value, describing the number of the page to print
        """
        #Enter Drawing commands here, dc is instance of wx.PostScriptDC or wx.MemoryDC (in preview mode)
        dc = self.GetDC()
        self.calculateScale(dc)
        pageData = self.drawData.getPageData(pageNum)
        self.drawData.drawPageData(pageData, dc, self.logUnits)
        return True

    def OnEndDocument(self):
        return super(Printout, self).OnEndDocument()

    def OnEndPrinting(self):
        return True

    def HasPage(self, pageNum):
        return pageNum <= self.numPages

    def calculateScale(self, dc):
        ppiPrinterX, ppiPrinterY = self.GetPPIPrinter()
        ppiScreenX, ppiScreenY = self.GetPPIScreen()
        logScale = float(ppiPrinterX) / float(ppiScreenX)
        pw, ph = self.GetPageSizePixels()
        dw, dh = dc.GetSize()
        scale = logScale * float(dw)/float(pw)
        dc.SetUserScale(scale, scale)
        self.logUnits = {}
        self.logUnits["mm"] = float(ppiPrinterX) / (logScale * 25.4)
        self.logUnits["cm"] = float(ppiPrinterX) / (logScale * 2.54)
        self.logUnits["inch"] = float(ppiPrinterX) / (logScale)
        self.logUnits["point"] = float(ppiPrinterX)
