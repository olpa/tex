#!/usr/bin/env python
# -*- coding: utf-8 -*-

import inspect

class Safety:
    """This class is designed to be called rom any 
    derived Subclass of wxWindow with self as only parameter
    
    It searches the name of the wxWindow and executes a method
    with the name of the wxWindow. This is currently only used to
    disable end enable Widgets from inside the wxWindow depend on
    the status of the variable wxWindow.safetyMode.
    
    This stuff is not done directly inside the panel to earn a central
    point for modifications of that manner
    
    """
    def __init__(self, parent):
        self.frame = parent.GetTopLevelParent()
        self.mode = self.frame.safetyMode

        if parent.GetName() in dir(self):
            eval("self." + parent.GetName() + "(parent)")

    def setParent(self, parent=None):
        self.parent = parent

    def colorCmykPanel(self, parent):
        if self.mode == "viewAccess":
            parent.cSpin.Disable()
            parent.mSpin.Disable()
            parent.ySpin.Disable()
            parent.kSpin.Disable()

    def colorHexPanel(self, parent):
        if self.mode == "viewAccess":
            parent.input.Disable()

    def colorRgbPanel(self, parent):
        if self.mode == "viewAccess":
            parent.rSpin.Disable()
            parent.gSpin.Disable()
            parent.bSpin.Disable()

    def colorSelectPanel(self, parent):
        if self.mode == "viewAccess":
            parent.color.Disable()

    def colorUnitPanel(self, parent):
        if self.mode == "viewAccess":
            parent.choice.Disable()

    def contentTypePanel(self, parent):
        if self.mode == "viewAccess":
            parent.choice.Disable()

    def dimensionPanel(self, parent):
        if self.mode == "viewAccess":
            parent.spinHeight.Disable()
            parent.spinWidth.Disable()

    def imagePanel(self, parent):
        if self.mode == "viewAccess":
            parent.inputFile.Disable()

    def inheritancePanel(self, parent):
        if self.mode == "viewAccess":
            parent.inheritance.Disable()

    def measureUnitPanel(self, parent):
        if self.mode == "viewAccess":
            parent.choice.Disable()

    def paperFormatPanel(self, parent):
        if self.mode == "viewAccess":
            parent.choice.Disable()

    def paperLayoutPanel(self, parent):
        if self.mode == "viewAccess":
            parent.radio.Disable()

    def paperOrientationPanel(self, parent):
        if self.mode == "viewAccess":
            parent.radio.Disable()

    def positionPanel(self, parent):
        if self.mode == "viewAccess":
            parent.topSpin.Disable()
            parent.leftSpin.Disable()
            parent.rightSpin.Disable()
            parent.bottomSpin.Disable()

    def rotationPanel(self, parent):
        if self.mode == "viewAccess":
            parent.topSpin.Disable()
            parent.leftSpin.Disable()
            parent.rightSpin.Disable()
            parent.bottomSpin.Disable()

    def textPanel(self, parent):
        if self.mode == "viewAccess":
            parent.text.Disable()

    def vartextPanel(self, parent):
        if self.mode == "viewAccess":
            parent.text.Disable()
            parent.dateButton.Disable()
            parent.documentButton.Disable()

    def informationPanel(self, parent):
        if self.mode != "fullAccess":
            parent.inputName.Disable()
        if self.mode == "viewAccess":
            parent.inputDescription.Disable()

    def designerInformationPanel(self, parent):
        if self.mode != "fullAccess":
            parent.inputName.Disable()

    def passwordPanel(self, parent):
        if self.mode != "fullAccess":
            parent.fullAccessLabel.Disable()
            parent.fullAccessSet.Disable()
            parent.fullAccessUnset.Disable()
            parent.restrictedAccessLabel.Disable()
            parent.restrictedAccessSet.Disable()
            parent.restrictedAccessUnset.Disable()
            parent.viewAccessLabel.Disable()
            parent.viewAccessSet.Disable()
            parent.viewAccessUnset.Disable()

    def clientPathPanel(self, parent):
        if self.mode != "fullAccess":
            parent.clientTemplateDirLabel.Disable()
            parent.clientTemplateDirInput.Disable()
            parent.clientImageDirLabel.Disable()
            parent.clientImageDirInput.Disable()

    def serverPathPanel(self, parent):
        if self.mode != "fullAccess":
            parent.serverTemplateDirLabel.Disable()
            parent.serverTemplateDirInput.Disable()
            parent.serverImageDirLabel.Disable()
            parent.serverImageDirInput.Disable()

    def templateDesignerFrame(self, parent):
        if self.mode!= "fullAccess":
            parent.addButton.Disable()
            parent.deleteButton.Disable()
