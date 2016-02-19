#!/usr/bin/env python
# -*- coding: utf-8 -*-

class messageBus():

    def __init__(self):

        #Dummy file handler
        self.messagefile = None

        #Message handler
        self.printnotice = None
        self.printwarning = None
        self.printerror = None

        #Set message containers
        self.notice = []
        self.warning = []
        self.error = []

        #Set log file container
        self.log = []

    def __setNotice(self, message):
        if self.printnotice == True:
            print "notice:\t" + message
        if self.messagefile != None:
            self.log.append("notice:\t" + message)
        self.notice.append(message)

    def __setWarning(self, message):
        if self.printwarning == True:
            print "warning:\t" + message
        if self.messagefile != None:
            self.log.append("warning:\t" + message)
        self.warning.append(message)

    def __setError(self, message):
        if self.printerror == True:
            print "error:\t" + message
        if self.messagefile != None:
            self.log.append("error:\t" + message)
        self.error.append(message)

    def setMessage(self, type, message):
        if type == "notice":
            self.__setNotice(message)
        elif type == "warning":
            self.__setWarning(message)
        elif type == "error":
            self.__setError(message)

    def testBreakExec(self):
        if len(self.error) > 0:
            return False
        else:
            return True
