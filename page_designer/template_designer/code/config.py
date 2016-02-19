#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import os.path

import ConfigParser

class ConfigData:
    """ConfigData adds support of a very simple transparent 
    configuration storage.
    
    Please take in mind, that there should be only one instance of 
    ConfigData in the application. In other ways nobody can garantee 
    which values became modified or get perhaps overwritten 
    by another ConfigData instance
    
    Because that, it is useful to derive the main frame of 
    the application from ConfigData
    
    """
    def __init__(self):
        self.parser = ConfigParser.SafeConfigParser()

        #Collect Configuration data
        #Load base configuration file
        configFile = "templatedesigner.conf"
        path = os.path.abspath(os.path.dirname(sys.modules[__name__].__file__))
        baseConfigFile = path + "/" + configFile
        self.setConfigFile(baseConfigFile, "r")
        self.selfCheck()

       #Load system wide configuration file
        systemConfigFile = self.systemDir() + "/" + configFile
        self.setConfigFile(systemConfigFile, "r")

        #Load user configuration file
        userConfigFile = self.userDir() + "/" + configFile
        self.userConfig = os.path.expanduser(userConfigFile)
        self.setConfigFile(self.userConfig, "rw")

        #Prepare Paths
        self.checkDir(self.userDir(), 0744)
        self.checkDir(self.clientTemplates(), 0744)
        self.checkDir(self.serverTemplates(), 0744)

    def setConfigFile(self, file, mode):
        try:
            fileObject = open(file, mode)
        except IOError: pass
        else:
            self.parser.readfp(fileObject)

    def selfCheck(self):
        if self.parser.sections() == []:
            exit(_(u"I was not able to find valid configuration data. Aborting"))

    def getOption(self, section, option):
        """Return the value of a given option from a given section.
        
        Return False, if option or section is not available
        
        """
        if self.parser.has_section(section) == False:
            return False
        else:
            if self.parser.has_option(section, option) == False:
                return False
        return self.parser.get(section, option)

    def setOption(self, section, option, value):
        """Add a given option with a given value to a given section
        
        """
        if self.parser.has_section(section) == False:
            self.parser.add_section(section)
        self.parser.set(section, option, value)

    def removeOption(self, section, option):
        """Remove a given option from a given section
        
        """
        if self.parser.has_section(section) == False:
            return False
        if self.parser.has_option(section, option) == False:
            return False
        self.parser.remove_option(section, option)

    def saveConfig(self):
        """Save the current configuration to 
        the users configuration file
        
        """
        if type(self.userConfig) == "file":
            self.parser.write(self.userConfig)
        else:
            self.parser.write(open(self.userConfig, "w"))

    def checkDir(self, path, mode):
        """checkDir locks, if the user has full read, write, execute
        access to a given directory. 
        
        I don't think this works on non-Unix filesystems
        
        """
        def checkRights(pos):
            if oct(os.stat(path).st_mode)[pos] < 7:
                try:
                    chmodDir = os.chmod(path, mode)
                except OSError:
                    exit(_(u"Insufficient rights to enter the required directory %s. Aborting!") % path)

        def makeDir(path):
            try:
                makeDir = os.mkdir(path, mode)
            except OSError:
                exit(_(u"I was not able to enter the required directory %s. Aborting!") % path)
            #Recheck
            if os.path.isdir(path) == True:
                return True
            return False

        if os.path.isdir(path) == False:
            if makeDir(path) == False:
                exit(_(u"Could not access required directory " + path))
        if oct(os.stat(path).st_uid) == os.getuid():
            checkRights(3)
        elif oct(os.stat(path).st_gid) == os.getgid():
            checkRights(4)
        else:
            checkRights(5)

    def getExamples(self):
        """getExampled copies all files from the example directory
        to the client storage and server storage directory
        
        """
        import shutil
        import fnmatch
        directory = self.exampleDir()
        files = os.listdir(directory)
        for file in files:
            file = file
            if os.path.isfile(directory + "/" + file) == True and \
            fnmatch.fnmatch(directory + "/" + file, "*.xml"):
                try:
                    shutil.copyfile(directory + "/" + file, self.clientTemplates() + "/" + file)
                    shutil.copyfile(directory + "/" + file, self.serverTemplates() + "/" + file)
                finally: pass
        return

    def getValue(self, section, option):
        dir = self.getOption(section, option)
        if dir != False:
            return dir
        else:
            exit(_(u"Invalid configuration: Please check your configuration files: section %s , %option %s") % (section, option))

    def baseDir(self):
        return os.path.normpath(os.path.expanduser(self.getValue("paths", "baseDir")))

    def userDir(self):
        return os.path.normpath(os.path.expanduser(self.getValue("paths", "userDir")))

    def systemDir(self):
        return os.path.normpath(os.path.expanduser(self.getValue("paths", "systemDir")))

    def exampleDir(self):
        return os.path.normpath(os.path.expanduser(self.getValue("paths", "exampleDir")))

    def baseGraphics(self):
        return os.path.normpath(os.path.expanduser(self.getValue("graphics", "baseGraphics")))

    def menuBarGraphics(self):
        return os.path.normpath(os.path.expanduser(self.getValue("graphics", "menuBarGraphics")))

    def toolBarGraphics(self):
        return os.path.normpath(os.path.expanduser(self.getValue("graphics", "toolBarGraphics")))

    def documentTreeGraphics(self):
        return os.path.normpath(os.path.expanduser(self.getValue("graphics", "documentTreeGraphics")))

    def programGraphics(self):
        return os.path.normpath(os.path.expanduser(self.getValue("graphics", "programGraphics")))

    def contextMenuGraphics(self):
        return os.path.normpath(os.path.expanduser(self.getValue("graphics", "contextMenuGraphics")))

    def skinGraphics(self):
        return os.path.normpath(os.path.expanduser(self.getValue("graphics", "skinGraphics")))

    def clientTemplates(self):
        return os.path.normpath(os.path.expanduser(self.getValue("templates", "clientTemplates")))

    def serverTemplates(self):
        return os.path.normpath(os.path.expanduser(self.getValue("templates", "serverTemplates")))

    def clientImages(self):
        return os.path.normpath(os.path.expanduser(self.getValue("templates", "clientImages")))

    def serverImages(self):
        return os.path.normpath(os.path.expanduser(self.getValue("templates", "serverImages")))
