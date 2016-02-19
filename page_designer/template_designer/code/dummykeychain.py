#!/usr/bin/env python 
# -*- coding: utf-8 -*-

"""Modified from beginning of line 152
This is a dummy implementation for non-darwin systems
"""

class Keychain:

    DEBUG=False

    def __init__(self):
        """ Keychain.py    is a simple class allowing access to keychain data and 
        settings. Keychain.py can also setup new keychains as required. As the 
        keychain is only available on MaxOSX the module will raise ImportError 
        if import is attempted on anything other than Mac OSX """
        return

    def listkeychains(self):
        return

    def checkkeychainname(self, keychain):
        """ Rationalises keychain strings as to whether they have .keychain or not 
        and looks them up in the dictionary of keychains created at 
        instantiation. Returns a string if successful and False if keychain is 
        not available"""
        return [True]

    def getgenericpassword(self, keychain, item):
        """ Returns account + password pair from specified keychain item """
        return [True]

    def setgenericpassword(self, keychain, account, password, servicename=None):
        """ Create and store a generic account and password in the given keychain """
        return

    def lockkeychain(self, keychain):
        return

    def unlockkeychain(self, keychain, password=None):
        return

    def createkeychain(self, keychain, password=None):
        return

#-----------------------------------------------------------------------
# Modified section
#-----------------------------------------------------------------------

    def setkeychain(self, keychain, lock=True, timeout=0):
        """ Allows setting the keychain configuration. 
        If lock is True the keychain will be locked on sleep. 
        If the timeout is set to anything other than 0 the keychain 
        will be set to lock after timeout seconds of inactivity 
        
        """
        return

    def showkeychaininfo(self, keychain):
        """Returns a dictionary containing the keychain settings
        
        """
        return

    def listgenericpasswords(self, keychain):
        """Returns account + password list from specified keychain
        
        """
        return

    def removekeychain(self, keychain):
        """Remove a keychain
        
        """
        return

    def removegenericpassword(self, keychain, keychainpassword, account):
        """Drop a generic password.
        
        Attentation: Servicename information of all passwords in 
        keychain gets lost on this process! 
        This is an ugly thing because the security tool does 
        not allow this by nature, as I know ;)
        
        """
        return

    def changegenericpassword(self, keychain, keychainpassword, 
                              account, newaccountpassword):
        """Change a generic password.
        
        Attentation: Servicename information of all passwords in 
        keychain gets lost on this process! 
        This is an ugly thing because the security tool does 
        not allow this by nature, as I know ;)
        
        """
        return
