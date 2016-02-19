#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This module is a gateway to the gui compositions which are relevant for setting 
up the applications properties panel (The right one in the main frame).
"""

import sys
sys.path.append("../")

#Main compositions
import designer
designer = designer.designer

import frame
frame = frame.frame

import nothing
nothing = nothing.nothing

import page
page = page.page

import template
template = template.template

#core components
import color
color = color.color

import colorcmyk
colorCmyk = colorcmyk.colorCmyk

import colorhex
colorHex = colorhex.colorHex

import colorrgb
colorRgb = colorrgb.colorRgb

import colorselect
colorSelect = colorselect.colorSelect

import colorunit
colorUnit = colorunit.colorUnit

import contenttype
contentType = contenttype.contentType

import dimension
dimension = dimension.dimension

import image
image = image.image

import information
information = information.information

import inheritance
inheritance = inheritance.inheritance

import position
position = position.position

import measureunit
measureUnit = measureunit.measureUnit

import paperformat
paperformat = paperformat.paperFormat

import paperlayout
paperlayout = paperlayout.paperLayout

import paperorientation
paperorientation = paperorientation.paperOrientation

import rotation
rotation = rotation.rotation

import settingstemplate
settingstemplate = settingstemplate.settingsTemplate
