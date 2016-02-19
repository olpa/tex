#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This color package enables conversion of given color values in an easy way.
Some calling examples 

>>> #import
>>> from colors import colors

>>> #Initialize object
>>> myColor=colors("Gold")

>>> #Get converted Hex value as string
>>> myColor.getHex()                      # "#FFD700"

>>> #Get converted Cmyk value as tuple of integers. Value base is 255
>>> myColor.getCmyk()                     # (0, 40, 255, 0)

>>> #Get converted Cmyk value as tuple of integers. Value base is 100
>>> myColor.getCmyk100()                  # (0, 15, 100, 0)

>>> #Get converted Cmyk value as tuple of floats. Value base is 1
>>> myColor.getCmyk1()                    # (0.0, 0.15686274509803921, 1.0, 0.0)

>>> #Get converted Rgb value as tuple of integers. Value base is 255
>>> myColor.getRgb()                      # (255, 215, 0)

>>> #Get converted Rgb value as tuple of integers. Value base is 100
>>> myColor.getRgb100()                   # (100, 84, 0)

>>> #Get converted Rgb value as tuple of floats. Value base is 1
>>> myColor.getRgb1()                     # (1.0, 0.84313725490196079, 0.0)

>>> #Get the name of the color as string
>>> #This function uses the X11 color name definition 1.2
>>> If no color name is defined, then the method returns None
>>> myColor.getName()                     # "Gold"

>>> Get all calculated values as dictianary
>>> myColor.getAll()
{   "name"   : "Gold", 
    "rgb1"   : (1.0, 0.84313725490196079, 0.0), 
    "cmyk1"  : (0.0, 0.15686274509803921, 1.0, 0.0), 
    "hex"    : "#FFD700", "cmyk100": (0, 15, 100, 0), 
    "cmyk"   : (0, 40, 255, 0), 
    "rgb"    : (255, 215, 0), 
    "rgb100" : (100, 84, 0)}

>>> #Redefine color. Some examples now. 
>>> #If you define rgb or cmyk values, then only values with base of 255 
>>> #are correctly calculated for now.
>>> myColor.setColor("LightGoldenrodYellow")
>>> myColor.setColor("rgb 123 45 67")
>>> myColor.setColor("rgb(76,54,321)")
>>> myColor.setColor("cmyk ( 170 160 130 120 )")
>>> myColor.setColor("cmyk 60,70,80,90")
>>> myColor.setColor("#ffa500")
>>> myColor.setColor("# aa cc 66")
>>> myColor.setColor("#(12 34 56)")

"""

import gettext
trans = gettext.translation(domain="colors", localedir="i18n", fallback=True) 
trans.install("colors")

from colors import colors

class main(colors):
    def __init__(self):
        pass

main()
