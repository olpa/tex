#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx

from printout import Printout
from drawdata import DrawData

class Printing:

    def __init__(self, *args, **kwargs):
        #Define object which includes all print data
        self.printData = wx.PrintData()

    def __customPageSetup(self):
        self.drawData = DrawData(self)
        #Is all the time duplex, because duplex is handled internally while drawing to the dc
        self.printData.SetDuplex(wx.DUPLEX_SIMPLEX)
        #Get from template system
        pageData = self.drawData.getPageData(1)
        orientation = self.drawData.getOrientation(pageData)
        self.printData.SetOrientation(orientation)
        size = self.drawData.getPaperSize(pageData)
        self.printData.SetPaperSize((100, 100))

    def OnPrintSetup(self, event=None):
        self.__customPageSetup()
        #Define print dialog settings, for e.g. from the template system
        printDialogData = wx.PrintDialogData()
        printDialogData.SetMaxPage(self.drawData.totalPages()) 
        printDialog = wx.PrintDialog(self, data=printDialogData)
        if printDialog.ShowModal() == wx.ID_OK:
            printDialogData = printDialog.GetPrintDialogData()
        self.printData = wx.PrintData(printDialogData.GetPrintData())
        printDialog.Destroy()
        return True

    def OnPageSetup(self, event=None):
        self.__customPageSetup()
        #Define page dialog settings, for e.g. from the template system
        pageSetupDialogData = wx.PageSetupDialogData()

        pageData = self.drawData.getPageData(1)
        size = self.drawData.getPaperSize(pageData)
        pageSetupDialogData.SetPaperSize((100, 100))
        pageSetupDialogData.SetMarginTopLeft((0, 0))
        pageSetupDialogData.SetMinMarginBottomRight((0, 0))
        pageSetupDialogData.SetDefaultMinMargins(False)

        #Show the page setup dialog
        pageSetupDialog = wx.PageSetupDialog(self, data=pageSetupDialogData)
        if pageSetupDialog.ShowModal() == wx.ID_OK:
            pageSetupDialogData = pageSetupDialog.GetPageSetupDialogData()

        self.printData = wx.PrintData(pageSetupDialogData.GetPrintData())
        pageSetupDialog.Destroy()
        return True

    def OnPrintPreview(self, event=None):
        self.OnSave()
        self.__customPageSetup()
        #Set data to print
        printout = Printout(self)
        printoutForPrinting = Printout(self)
        preview = wx.PrintPreview(printout, printoutForPrinting, self.printData)
        if not preview.Ok():
            wx.MessageBox(_(u"Unable to create Print Preview!"), _(u"Preview Error"))
        else:
            previewFrame = wx.PreviewFrame(preview, self, _(u"Print Preview"), pos=self.GetPosition(), size=self.GetSize())
            previewFrame.Initialize()
            previewFrame.Show()
        return True

    def OnDoPrint(self, event=None):
        self.OnSave()
        self.customPageSetup()
        #Set data to print
        printout = Printout(self)
        #Instance of printer class
        printer = wx.Printer(data=None)
        #Print
        #This processes the methods of printout
        if not printer.Print(self, printout, prompt=True) \
           and printer.GetLastError() == wx.PRINTER_ERROR:
            wx.MessageBox(_(u"There was a problem printing.\nPerhaps your current printer is not set correctly?"), _(u"Printing Error"), wx.OK)
        else:
            data = printer.GetPrintDialogData()
            self.pdata = wx.PrintData(data.GetPrintData())
        printout.Destroy()
        return True
