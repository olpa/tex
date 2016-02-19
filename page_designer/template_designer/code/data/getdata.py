#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import os
import fnmatch

import xml.etree.ElementTree as ET

import tdparser as parser

class GetData:

    def __init__(self, *args, **kwargs):
        self.fillData()

    def fillData(self):
        #Please be cautious with the following i18n strings! 
        #These are used in "OnSelChanged()" of class view for a comparison.
        self.__setTreeNodes(self.document.GetRootItem(), 
                          self.serverTemplates(),
                           _(u"Server-Templates"))
        self.__setTreeNodes(self.document.GetRootItem(), 
                          self.clientTemplates(), 
                          _(u"Client-Templates"))

    def dropData(self):
        self.document.DeleteAllItems()
        self.document.createRootItem()

    def renewData(self):
        self.dropData()
        self.fillData()

#----------------------------------------------------------------------
# Now the ElementTree stuff follows
#-----------------------------------------------------------------------

    def __setTreeNodes(self, root, directory, name):
        """Recursively traverses the data structure, 
        adding tree nodes to match it
            
        """
        #Add Source, checkPath is a method of class getFiles
        if self.checkPath(directory) == False: 
            return
        sourceServer = self.document.AppendItem(root, name)
        self.document.SetItemImage(sourceServer, self.document.imageSource, wx.TreeItemIcon_Normal)
        #getFiles is a method of class fetFiles
        self.__getFiles(sourceServer, directory)

    def __addTreeItem(self, parentItem, element, icon):
        item = self.document.AppendItem(parentItem, element.attrib["name"], data=None)
        self.document.SetItemPyData(item, element)
        self.document.SetItemImage(item, icon, wx.TreeItemIcon_Normal)
        return item

    def __addRoot(self, treeItem, directory, file):
        #Define Namespace prefix
        ET._namespace_map["http://www.bitplant.de/template"] = "bit"
        xml = ET.parse(directory + "/" + file)
        root = xml.getroot()

        if root.tag.rsplit("}")[-1] == "designer":
            item = self.__addTreeItem(treeItem, root, self.document.imageCompilation)
            self.__addTemplate(item, root)
        elif root.tag.rsplit("}")[-1] == "template":
            item = self.__addTreeItem(treeItem, root, self.document.imageDocuments)
            self.__addPage(item, root)

    def __addTemplate(self, treeItem, root):
            for e in root:
                if e.tag.rsplit("}")[-1] == "template":
                    item = self.__addTreeItem(treeItem, e, self.document.imageDocuments)
                    self.__addPage(item, e)

    def __addPage(self, treeItem, root):
            for e in root:
                if e.tag.rsplit("}")[-1] == "page":
                    item = self.__addTreeItem(treeItem, e, self.document.imagePages)
                    self.__addFrame(item, e)

    def __addFrame(self, treeItem, root):
            for e in root:
                if e.tag.rsplit("}")[-1] == "frame":
                    item = self.__addTreeItem(treeItem, e, self.document.imageFrames)

#----------------------------------------------------------------------
# Now the file system stuff follows
#-----------------------------------------------------------------------

    def __getFiles(self, sourceServer, directory):
        files = self.checkFiles(directory)
        for file in files:
            self.__addRoot(sourceServer, directory, file)

    def checkPath(self, directory):
        """Wrapper function to check, if given directory is valid.
        Needs to be extended, if network access is desired
        
        """
        tree = []
        if os.path.isdir(directory) == True:
            return True
        else:
            return False

    def checkFiles(self, directory):
        """Scans given directory for valid files 
        and return a list with their names
        
        """
        tree = []
        files = os.listdir(directory)
        for file in files:
            if os.path.isfile(directory + "/" + file) == True and \
            fnmatch.fnmatch(directory + "/" + file, "*.xml") and \
            self.valiFile(directory + "/" + file) == True:
                tree.append(file)
        return tree

    def valiFile(self, file):
        """Scans a given file, if it validates correctly
        against the bitplanttemplate XML parser
        
        """
        newParser = parser.parse(file, outfile = None, messagefile = None, printnotice = False, printwarning = True, printerror = True)
        if newParser.result() == True:
            return True
        else:
            return False
