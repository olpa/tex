#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import xml.etree.ElementTree as ET

from safety import Safety
from tdparser.papersizes import PaperSizes

class paperFormatValidator(wx.PyValidator):
    def __init__(self, parent):
        wx.PyValidator.__init__(self)

        self.parent = parent
        self.frame = self.parent.GetTopLevelParent()
        self.tree = self.frame.document
        self.item = self.tree.GetSelection()
        self.xml = self.tree.GetItemPyData(self.item)

        self.sizes = PaperSizes()

        self.Bind(wx.EVT_CHOICE, self.OnText)
        self.Bind(wx.EVT_SET_FOCUS, self.OnText)

    def OnText(self, event=None):
        self.frame.OnEdit()
        #set temporary data for possible later saving
        self.TransferFromWindow()
        return True

    def Clone(self):
         return paperFormatValidator(self.parent)

    def Validate(self):
        return True

    def TransferToWindow(self):
        textCtrl = self.GetWindow()
        xmlForm = self.xml.findall("{http://www.bitplant.de/template}parameter/{http://www.bitplant.de/template}paper")
        for form in xmlForm:
            if form.attrib["type"] == "format" and form.attrib["value"] in self.sizes.getAllowedSizes():
                textCtrl.SetStringSelection(form.attrib["value"])
        return True

    def TransferFromWindow(self):
        textCtrl = self.GetWindow()
        if textCtrl.GetStringSelection() in self.sizes.getAllowedSizes():
            self.frame.tempItemData["paperFormat"] = str(textCtrl.GetStringSelection())
        return True

class paperFormat(wx.Panel):

    """This class includes the widgets to select the page format of a template.
    
    The corresponding validator is paperFormatValidator and already set.
    Currently only some Din and us page sizes are enabled. 
    If you want more, overwrite variable `usedSizes`.
    
    """

    def __init__(self, parent, *args, **kwargs):
        wx.Panel.__init__(self, parent, *args, **kwargs)

        self.parent = self.GetTopLevelParent()
        self.tree = self.parent.document
        self.item = self.tree.GetSelection()
        self.xml = self.tree.GetItemPyData(self.item)

        self.allSizes = PaperSizes()
        self.usedSizes = ["a2", "a3", "a4", "a5", "executive", "letter", "legal", "cdsingle", "cddouble", "dvdsingle", "dvddouble"]

        self.label = wx.StaticText(self, -1, _(u"Page format"))
        self.choice = wx.Choice(self, -1, choices=self.usedSizes, name="paperFormat")
        self.choice.SetValidator(paperFormatValidator(self))

        self.__doProperties()
        self.__doLayout()
        self.InitDialog()
        Safety(self)

    def __doProperties(self):
        self.SetName("paperFormatPanel")

    def __doLayout(self):
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.label, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 8)
        sizer.Add(self.choice, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        self.SetSizerAndFit(sizer)
