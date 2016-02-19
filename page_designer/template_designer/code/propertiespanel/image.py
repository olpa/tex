#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import re
import sys
import os.path
from PIL import Image
import subprocess
from StringIO import StringIO
import xml.etree.ElementTree as ET
from safety import Safety

class imageValidator(wx.PyValidator):
    def __init__(self, parent):
        wx.PyValidator.__init__(self)

        self.parent = parent
        self.frame = self.parent.GetTopLevelParent()
        self.tree = self.frame.document
        self.item = self.tree.GetSelection()
        self.xml = self.tree.GetItemPyData(self.item)

        self.Bind(wx.EVT_FILEPICKER_CHANGED, self.OnChange)

    def OnChange(self, event=None):
        textCtrl = self.GetWindow()
        #Enable Preview
        bmp = self.getPreview(textCtrl.GetPath())
        if bmp != None:
            self.parent.inputPreview.SetBitmap(bmp)
            self.parent.status.SetLabel(textCtrl.GetPath())

        self.frame.OnEdit()
        #set temporary data for possible later saving
        self.TransferFromWindow()
        event.Skip()

    def Clone(self):
         return imageValidator(self.parent)

    def Validate(self):
        return True

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
            dialog = wx.MessageDialog(None, _(u"Internal error while converting image file into a suitable format. The image will not be available. Please use an external program like Preview to convert the image into a format like png or eps."), _(u"Run Preview to change image format?"), wx.YES_NO|wx.YES_DEFAULT|wx.ICON_QUESTION)
            decision = dialog.ShowModal()
            dialog.Destroy()
            if decision == wx.ID_YES:
                cmd = ["open", "-a", "/Applications/Preview.app", file] 
                subprocess.Popen(cmd)
            return None
        try:
            pil.thumbnail((600, 128))
        except:
            dialog = wx.MessageDialog(None, _(u"Internal error while converting image file into a suitable format. The image will not be available. Please use an external program like Preview to convert the image into a format like png or eps."), _(u"Run Preview to change image format?"), wx.YES_NO|wx.YES_DEFAULT|wx.ICON_QUESTION)
            decision = dialog.ShowModal()
            dialog.Destroy()
            if decision == wx.ID_YES:
                cmd = ["open", "-a", "/Applications/Preview.app", file] 
                subprocess.Popen(cmd)
            return None
        wxi = wx.EmptyImage(pil.size[0],pil.size[1])
        wxi.SetData(pil.convert("RGB").tostring())
        wxi.SetAlphaData(pil.convert("RGBA").tostring()[3::4])
        bmp = wx.BitmapFromImage(wxi)
        return bmp

    def TransferToWindow(self):
        textCtrl = self.GetWindow()
        if textCtrl.GetName() == "imageSelect":
            xmlText = self.xml.find("{http://www.bitplant.de/template}content")
            dir = self.__getDir(xmlText)
            if not xmlText.text:
                return True
            if xmlText.text.count(":") == 2:
                file = xmlText.text.split(":")[1]
                orifile = xmlText.text.split(":")[2]
                if os.path.isfile(dir + "/" + file):
                    bmp = self.getPreview(dir + "/" + file)
                    if bmp != None:
                        self.parent.inputPreview.SetBitmap(bmp)
                        self.parent.status.SetLabel(orifile)
        self.frame.tempItemData["contentType"] = "image"
        return True

    def TransferFromWindow(self):
        textCtrl = self.GetWindow()
        #Preparation of this is done in prepareData class
        self.frame.tempItemData["text"] = textCtrl.GetPath()
        return True

class image(wx.Panel):
    def __init__(self, parent, *args, **kwds):
        wx.Panel.__init__(self, parent, *args, **kwds)

        self.parent = self.GetTopLevelParent()
        self.tree = self.parent.document
        self.item = self.tree.GetSelection()
        self.xml = self.tree.GetItemPyData(self.item)

        self.staticBox = wx.StaticBox(self, -1, _(u"Image"))

        self.status = wx.StaticText(self, -1, "", name="imageStatus")
        self.status.SetLabel(_(u"No image selected or available."))

        self.inputFile = self.OnSelect()
        self.inputFile.SetValidator(imageValidator(self))

        self.labelPreview = wx.StaticText(self, -1, _(u"Preview"))
        self.inputPreview = wx.StaticBitmap(self, -1, wx.Bitmap(self.parent.skinGraphics() + "/images_display.png", wx.BITMAP_TYPE_ANY), name="imagePreview")

        self.__doProperties()
        self.__doLayout()
        self.InitDialog()
        Safety(self)

    def __doProperties(self):
        self.SetName("imagePanel")

    def OnSelect(self):
        setMessage = _(u"Choose an image file")
        setDefaultDir = self.parent.clientImages()
        setDefaultFile = ""

        setWildcard = "Preferred image formats (*.eps*.pdf*.png*.tiff)|*.eps;*.pdf;*.png;*.tiff;|"\
                      "Allowed image formats |*.bmp;*.cur;*.dcx;*.eps;*.fli;*.flc;*.gbr;*.gif;*.ico;*.im;*.imt;*.iptc;*.naa;*.jpg;*.jpeg;*.mcidas;*.mic;*.msp;*.pcd;*.pcx;*.pdf;*.png;*.ppm;*.spi;*.tga;*.tif;*.tiff;*.wal;*.xbm;*.xpm;*.xv|" \
                      "All files (*.*)|*.*"
        setStyle       = wx.OPEN

        return wx.FilePickerCtrl(self, -1, path=setDefaultDir + setDefaultFile, message=setMessage, wildcard=setWildcard, style=setStyle, name="imageSelect")

    def __doLayout(self):
        staticSizer = wx.StaticBoxSizer(self.staticBox, wx.VERTICAL)
        sizer = wx.BoxSizer(wx.VERTICAL)
        imageSizer = wx.BoxSizer(wx.HORIZONTAL)
        previewSizer = wx.BoxSizer(wx.HORIZONTAL)

        imageSizer.Add(self.status, 1, wx.EXPAND|wx.ALL|wx.ALIGN_CENTER_VERTICAL, 0)
        imageSizer.Add(self.inputFile, 0, wx.EXPAND|wx.ALL|wx.ALIGN_CENTER_VERTICAL, 0)

        previewSizer.Add(self.labelPreview, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 4)
        previewSizer.Add(self.inputPreview, 1, wx.EXPAND|wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 4)

        sizer.Add(imageSizer, 0, wx.EXPAND|wx.ALL, 4)
        sizer.Add(previewSizer, 1, wx.EXPAND|wx.ALL, 0)

        staticSizer.Add(sizer, 1, wx.EXPAND|wx.ALL, 0)
        self.SetSizerAndFit(staticSizer)
