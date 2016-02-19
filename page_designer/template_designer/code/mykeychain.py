#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

if sys.platform == 'darwin':
    from keychain import Keychain
else:
    from dummykeychain import Keychain

class MyKeyChain(Keychain):
    """MyKeyChain adds wrapper functions to the Keychain class
    
    The Keychain class was designed to access the 
    Apple Keychain (Stores and protects passwords)
    
    MyKeyChain adds functions to abstract the access of 
    Keychain to be nearly fully transparent to the calling functions
    
    You maybe also need to look at Keychain. I modified it 
    and send it back to the author but he did not commit the 
    changes and additions for now
    
    """
    def __init__(self, *args, **kwargs):
        Keychain.__init__(self, *args, **kwargs)

        self.kcName = "TemplateDesigner"
        self.kcPassword = "BitplantTemplateDesigner"
        self.kcLock = True
        self.kcTimeout = 300
        self.recursionTest = False
        self.testKeyChain()

    def checkFull(self):
        """Returns true if user gave a password to protect 
        the full access to the calling application
        
        """
        return self.isKey("fullAccess")

    def checkRestricted(self):
        """Returns true if user gave a password to protect 
        the restricted access to the calling application
        
        """
        return self.isKey("restrictedAccess")

    def checkView(self):
        """Returns true if user gave a password to protect 
        the view access to the calling application
        
        """
        return self.isKey("viewAccess")

    def comparePassword(self, key, password):
        """Returns true if a given password matches to a given key
        
        """
        self.unLock()
        keyChainPw = self.getgenericpassword(self.kcName, key)
        if type(keyChainPw) == dict:
            if keyChainPw["password"] == password:
                self.lock()
                return True
        self.lock()
        return False

    def isKey(self, key):
        """Returns true if a given key is 
        available in the default keychain
        
        """
        self.unLock()
        keyChainPw = self.getgenericpassword(self.kcName, key)
        if type(keyChainPw) == dict:
            self.lock()
            return True
        self.lock()
        return False

    def unLock(self):
        """unLock is intended to be a helper function but may usefull
        elselike. It unlocks the default keychain with 
        the default keychain password
        
        Normally this would be required only once at application start,
        but the keychain locks automatically after a settable amount 
        of time. So this method is called by some other wrapper scripts 
        here to avoid the login dialog of the keychain
        
        Returns True on success
        
        """
        test = self.checkkeychainname(self.kcName)
        if test[0] == False:
            self.createKeyChain()
            if self.recursionTest == False:
                self.recursionTest = True
                self.unLock()
            else:
                self.recursionTest = False
        else:
            self.unlockkeychain(self.kcName, self.kcPassword)

    def lock(self):
        """Lock locks the default keychain. 
        
        See self.unLock for deeper explanations.
        Returns True on success
        
        """
        test = self.checkkeychainname(self.kcName)
        if test[0] == False:
            self.createKeyChain()
            if self.recursionTest == False:
                self.recursionTest = True
                self.lock()
            else:
                self.recursionTest = False
        else:
            self.lockkeychain(self.kcName)

    def testKeyChain(self):
        """This method returns True, if the 
        default keychain exists in the system
        
        """
        test = self.checkkeychainname(self.kcName)
        if test[0] == False:
            self.createKeyChain()
            if self.recursionTest == False:
                self.recursionTest = True
                self.testKeyChain()
            else:
                self.recursionTest = False
        else:
            return True

    def createKeyChain(self):
        """This method creates a keychain with the defaulted values
        self.kcName, self.kcPassword, self.kcLock, self.kcTimeout
        
        """
        self.createkeychain(self.kcName, self.kcPassword)
        self.setkeychain(self.kcName, self.kcLock, self.kcTimeout)

    def setFullAccess(self, password):
        """Add a key to protect the full access with a given password
        
        """
        self.setPassword("fullAccess", password)

    def setRestrictedAccess(self, password):
        """Add a key to protect the restricted access with a given password
        
        """
        self.setPassword("restrictedAccess", password)

    def setViewAccess(self, password):
        """Add a key to protect the view access with a given password
        
        """
        self.setPassword("viewAccess", password)

    def setPassword(self, key, password):
        """Apply a given password to a given key
        
        """
        self.unLock()
        self.setgenericpassword(self.kcName, key, password)
        self.lock()

    def changePassword(self, key, password):
        """Change the password from a given key to the given value
        
        No old password is required
        
        """
        self.unLock()
        self.changegenericpassword(self.kcName, self.kcPassword, key, password)
        self.lock()

    def removePassword(self, key):
        """Remove a given key from default keychain
        """
        self.unLock()
        self.removegenericpassword(self.kcName, self.kcPassword, key)
        self.lock()
