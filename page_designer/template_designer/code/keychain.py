#!/usr/bin/env python 
# -*- coding: utf-8 -*-

# Created by Stuart Colville on 2008-02-02
# Muffin Research Labs. http://muffinresearch.co.uk/

# Copyright (c) 2008, Stuart J Colville
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the Muffin Research Labs nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY Stuart J Colville ``AS IS'' AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL Stuart J Colville BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""Modified from beginning of line 152

"""

import os, sys, commands, re

class Keychain:

    DEBUG=False

    def __init__(self):
        """ Keychain.py    is a simple class allowing access to keychain data and 
        settings. Keychain.py can also setup new keychains as required. As the 
        keychain is only available on MaxOSX the module will raise ImportError 
        if import is attempted on anything other than Mac OSX """
        if sys.platform == 'darwin':
            self.listkeychains()
        else:
            raise ImportError('Keychain is only available on Mac OSX')

    def listkeychains(self):
        """ Returns a dictionary of all of the keychains found on the system """
        k = commands.getoutput("security list-keychains") 
        rx = re.compile(r'".*?/([\w]*)\.keychain"', re.I|re.M) 
        self.keychains = {}
        for match in rx.finditer(k):
            self.keychains[match.group(1)]=match.group().strip('"')
        return self.keychains 

    def checkkeychainname(self, keychain):
        """ Rationalises keychain strings as to whether they have .keychain or not 
        and looks them up in the dictionary of keychains created at 
        instantiation. Returns a string if successful and False if keychain is 
        not available"""

        start = keychain.find('.keychain')
        keychain = start > -1 and keychain[:start] or keychain
        return keychain in self.keychains and '%s.keychain' % keychain or (False, "%s.keychain  doesn't exist" % keychain)

    def getgenericpassword(self, keychain, item):
        """ Returns account + password pair from specified keychain item """
        keychain = self.checkkeychainname(keychain) 
        if keychain[0] == False:
            return keychain

        k = commands.getstatusoutput("security find-generic-password -g -a %s  %s" % (item, keychain))
        if self.DEBUG:
            print k
        if k[0]:
            return False, 'The specified item could not be found'
        else:
            rx1 = re.compile(r'"acct"<blob>="(.*?)"', re.S)
            rx2 = re.compile(r'password: "(.*?)"', re.S)
            account = rx1.search(k[1])
            password = rx2.search(k[1])
            if account and password:
                return {"account":account.group(1),"password":password.group(1)}
            else:
                return False

    def setgenericpassword(self, keychain, account, password, servicename=None):

        """ Create and store a generic account and password in the given keychain """
        keychain = self.checkkeychainname(keychain)
        if keychain[0] == False:
            return keychain

        account = account and '-a %s' % (account,) or '' 
        password = password and '-p %s' % (password,) or ''
        servicename = servicename and '-s %s' % (servicename,) or ''
        k = commands.getstatusoutput("security add-generic-password %s %s %s %s" % (account, password, servicename, keychain))
        if self.DEBUG:
            print k
        if k[0]:
            return False, 'The specified password could not be added to %s' % keychain
        if k[0] == False:
            return True, 'Password added to %s successfully' % keychain

    def lockkeychain(self, keychain):
        keychain = self.checkkeychainname(keychain)
        if keychain[0] == False:
            return keychain

        k = commands.getstatusoutput("security lock-keychain %s" % (keychain))
        if self.DEBUG:
            print k
        if k[0]:
            return False, 'Keychain: %s could not be locked' % keychain
        if k[0] == False:
            return True, 'Keychain: %s locked successfully' % keychain

    def unlockkeychain(self, keychain, password=None):
        keychain = self.checkkeychainname(keychain) 
        if keychain[0] == False:
            return keychain

        if not password:
             from getpass import getpass 
             password = getpass('Password:')    
        k = commands.getstatusoutput("security unlock-keychain -p %s %s" % (password, keychain))
        if self.DEBUG:
            print k
        if k[0]:
            return False, 'Keychain could not be unlocked'
        if k[0] == False:
            return True, 'Keychain unlocked successfully'

    def createkeychain(self, keychain, password=None):
        if not password:
             from getpass import getpass
             password = getpass('Password:')

        keychain = keychain.find('.keychain') > -1 and keychain or '%s.keychain' % keychain
        k = commands.getstatusoutput("security create-keychain -p %s %s" % (password, keychain))
        if self.DEBUG:
            print k
        if k[0]:
            return False, 'Create creation failed'
        if k[0] == False:
            return True, 'Keychain created successfully'

#-----------------------------------------------------------------------
# Modified section
#-----------------------------------------------------------------------

    def setkeychain(self, keychain, lock=True, timeout=0):
        """ Allows setting the keychain configuration. 
        If lock is True the keychain will be locked on sleep. 
        If the timeout is set to anything other than 0 the keychain 
        will be set to lock after timeout seconds of inactivity 
        
        """
        keychain = self.checkkeychainname(keychain) 
        if keychain[0] == False:
            return keychain

        lock = lock and '-l' or ''
        timeout = timeout and '-u -t %s' % (timeout,) or ''
        k = commands.getstatusoutput("security keychain-settings %s %s %s" % (lock, timeout, keychain))
        if self.DEBUG:
            print k
        if k[0]:
            return False, 'Keychain settings failed'
        if k[0] == False:
            return True, 'Keychain updated successfully'

    def showkeychaininfo(self, keychain):
        """Returns a dictionary containing the keychain settings
        
        """
        keychain = self.checkkeychainname(keychain) 
        if keychain[0] == False:
            return keychain

        k = commands.getstatusoutput("security show-keychain-info %s" % (keychain))
        if self.DEBUG:
            print k
        if k[0]:
            return False, 'Keychain could not be found'
        if k[0] == False:
            result = {}
            result['keychain'] = keychain
            if k[1].find('lock-on-sleep') > -1:
                result['lock-on-sleep'] = True
            if k[1].find('no-timeout') > -1:
                result['timeout'] = 0
            else:
                rx = re.compile(r'timeout=(\d+)s', re.S)
                match = rx.search(k[1])
                result['timeout'] = match.group(1)
            return result

    def listgenericpasswords(self, keychain):
        """Returns account + password list from specified keychain
        
        """
        keychain = self.checkkeychainname(keychain)
        if keychain[0] == False:
            return keychain

        k = commands.getstatusoutput("security dump-keychain -d %s" % (keychain))
        if self.DEBUG:
            print k
        data = []
        rx0 = re.compile(r'keychain:', re.S)
        rx1 = re.compile(r'"acct"<blob>="(.*?)"', re.S)
        rx2 = re.compile(r'data:\n"(.*?)"', re.S)
        for kc in re.split(rx0, k[1]):
            account = rx1.search(kc)
            password = rx2.search(kc)
            if account and password:
                data.append({"account":account.group(1),"password":password.group(1)})
        return data

    def removekeychain(self, keychain):
        """Remove a keychain
        
        """
        keychain = self.checkkeychainname(keychain)
        if keychain[0] == False:
            return keychain

        k = commands.getstatusoutput("security delete-keychain %s" % (keychain))
        if self.DEBUG:
            print k
        if k[0]:
            return False, 'Keychain could not be found'
        if k[0] == False:
            return True, 'Keychain successfully removed'

    def removegenericpassword(self, keychain, keychainpassword, account):
        """Drop a generic password.
        
        Attentation: Servicename information of all passwords in 
        keychain gets lost on this process! 
        This is an ugly thing because the security tool does 
        not allow this by nature, as I know ;)
        
        """
        keychain = self.checkkeychainname(keychain)
        if keychain[0] == False:
            return keychain

        oldKc = self.showkeychaininfo(keychain)
        oldPasswords = self.listgenericpasswords(keychain)
        if self.removekeychain(keychain)[0] == False:
            return False, 'Keychain could not be modified'
        self.createkeychain(keychain, keychainpassword)
        self.setkeychain(keychain, oldKc["lock-on-sleep"], oldKc["timeout"])
        for password in oldPasswords:
            if password.has_key("account"):
                if password["account"] != account:
                        self.setgenericpassword(keychain, 
                                                password["account"], 
                                                password["password"])

    def changegenericpassword(self, keychain, keychainpassword, 
                              account, newaccountpassword):
        """Change a generic password.
        
        Attentation: Servicename information of all passwords in 
        keychain gets lost on this process! 
        This is an ugly thing because the security tool does 
        not allow this by nature, as I know ;)
        
        """
        keychain = self.checkkeychainname(keychain)
        if keychain[0] == False:
            return keychain

        self.removegenericpassword(keychain, keychainpassword, account)
        self.setgenericpassword(keychain, account, newaccountpassword)
