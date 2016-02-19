#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import os
import shutil
import fnmatch
import random
from time import time

import xml.etree.ElementTree as ET

class WriteData():
    """This class collects all methods which are relevnt to 
    write modified xml data to the file system
    
    """
    def __init__(self, *args, **kwargs):
        pass

    def OnWrite(self, event=None):
        #Write data back into xml object
        self.OnSave()
        self.remapData()
        self.change = False
        self.toolBar.EnableTool(wx.ID_SAVE, False)
        #Initiate Writing into files
        root = self.document.GetRootItem()
        self.__getLocations(root)
        self.__removeObsolete(self.serverTemplates())
        self.__removeObsolete(self.clientTemplates())

    def __getLocations(self, item):
        """Identifiy items that represent files 
        and initiate the writing process
        
        """
        if self.document.GetChildrenCount(item, False) > 0:
            entries = self.getChildren_(item)
            for entry in entries:
                self.__getFiles(entry)

    def __getFiles(self, item):
        #Identify template and compilation files and 
        #initiate the writing to the storage
        if self.document.GetChildrenCount(item, False) > 0:
            self.__writeFiles(item, _(u"Server-Templates"), "server", "client")
            self.__writeFiles(item, _(u"Client-Templates"), "client", "server")

    def __writeFiles(self, item, axisName, axis, counterAxis):
            if self.document.GetItemText(item) == axisName:
                entries = self.getChildren_(item)
                for entry in entries:
                    filename = str(random.uniform(0, 1)).replace(".", "") + ".temp"
                    #move possible images
                    data = self.document.GetItemPyData(entry)
                    self.__moveImages(data, axis, counterAxis)
                    prettyPrintXML(data)
                    self.document.SetItemPyData(entry, data)
                    #write out
                    ET.ElementTree(data).write(eval("self." + axis + "Templates()") + "/" + filename)

    def __moveImages(self, xml, axis, counterAxis):
        images = xml.findall(".//{http://www.bitplant.de/template}content")
        if images:
            for image in images:
                if image.get("type", "text") == "image":
                    dir = image.text.split(":")[0]
                    file =  image.text.split(":")[1]
                    orifile = image.text.split(":")[2]
                    if dir == counterAxis + "Images":
                        if os.path.isfile(eval("self." + counterAxis + "Images()") + "/" + file):
                            shutil.move(eval("self." + counterAxis + "Images()") + "/" + file, 
                                        eval("self." + axis + "Images()") + "/" + file)
                            image.text = axis + "Images:" + file + ":" + orifile

    def __removeObsolete(self, directory):
        """Scans given directory for xmls files, drops them 
        and renames temporary data
        
        """
        files = os.listdir(directory)
        for file in files:
            remove = directory + "/" + file
            if os.path.isfile(remove) == True and \
            fnmatch.fnmatch(remove, "*.xml"):
                os.remove(remove)

        files = os.listdir(directory)
        for file in files:
            source = directory + "/" + file
            destination = source.rstrip(".temp") + ".xml"
            if os.path.isfile(source) == True and \
            fnmatch.fnmatch(source, "*.temp"):
                shutil.move(source, 
                            destination)

        #Remove images from dropped frames
        for img in self.deleteItem:
          try:
            os.remove(img)
          except OSError:
            pass
        self.deleteItem = []
        return

def prettyPrintXML(xml, level=0):
    """This function is from the 
    effbot (http://effbot.org/zone/element-lib.htm)
    It formats the xml output for pretty printing on 
    ET versions lower 1.3
    
    """
    i = "\n" + level*"  "
    if len(xml):
        if not xml.text or not xml.text.strip():
            xml.text = i + "  "
        if not xml.tail or not xml.tail.strip():
            xml.tail = i
        for xml in xml:
            prettyPrintXML(xml, level+1)
        if not xml.tail or not xml.tail.strip():
            xml.tail = i
    else:
        if level and (not xml.tail or not xml.tail.strip()):
            xml.tail = i
