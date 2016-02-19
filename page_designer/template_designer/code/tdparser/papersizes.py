#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

class PaperSizes:

    def getAllowedSizes(self):
        return self.get.keys()

    def getMmSizes(self):
        return self.get.values()

    def getMmSize(self, format):
        if format in self.getAllowedSizes():
            return self.get.get(format)

    def getAll(self):
        return self.get

    get = {
"4a0" : (1682, 2378),
"2a0" : (1189, 1682),

"a0" : (841, 1189),
"a1" : (594, 841),
"a2" : (420, 594),
"a3" : (297, 420),
"a4" : (210, 297),
"a5" : (148, 210),
"a6" : (105, 148),
"a7" : (74, 105),
"a8" : (52, 74),
"a9" : (37, 52),
"a10" : (26, 37),

"b0" : (1000, 1414),
"b1" : (707, 1000),
"b2" : (500, 707),
"b3" : (353, 500),
"b4" : (250, 353),
"b5" : (176, 250),
"b6" : (125, 176),
"b7" : (88, 125),
"b8" : (62, 88),
"b9" : (44, 62),
"b10" : (31, 44),

"c0" : (917, 1297),
"c1" : (648, 917),
"c2" : (458, 648),
"c3" : (324, 458),
"c4" : (228, 324),
"c5" : (162, 229),
"c6" : (114, 162),
"c67" : (81, 162),
"c7" : (81, 114.9),
"c8" : (57, 81),
"c9" : (40, 57),
"c10" : (28, 40),

"dl" : (110, 220),

"a2extra" : (445, 619),
"a3extra" : (322, 445),
"a3super" : (305, 508),
"supera3" : (305, 487),
"a4extra" : (235, 322),
"a4super" : (229, 322),
"supera4" : (227, 356),
"a4long" : (210, 348),
"a5extra" : (173, 235),
"sob5extra" : (202, 276),

"ra0" : (860, 1220),
"ra1" : (610, 860),
"ra2" : (430, 610),
"ra3" : (305, 430),
"ra4" : (215, 305),

"rsa0" : (900, 1280),
"rsa1" : (640, 900),
"rsa2" : (450, 640),
"rsa3" : (320, 450),
"rsa4" : (225, 320),

"jis-b0" : (1030, 1456),
"jis-b1" : (728, 1030),
"jis-b2" : (515, 728),
"jis-b3" : (364, 515),
"jis-b4" : (257, 364),
"jis-b5" : (182, 257),
"jis-b6" : (128, 182),
"jis-b7" : (91, 128),
"jis-b8" : (64, 91),
"jis-b9" : (45, 64),
"jis-b10" : (32, 45),
"jis-b11" : (22, 32),
"jis-b12" : (16, 22),

"shirokubanbase" : (788, 1091),
"shirokuban4" : (264, 379),
"shirokuban5" : (189, 262),
"shirokuban6" : (191, 259),
"shirokuban7" : (127, 188),

"kikubase" : (636, 939),
"kiku4" : (227, 306),
"kiku5" : (151, 227),

"kai8" : (260, 370),
"kai16" : (185, 260),
"kai32" : (130, 185),
"kai32big" : (140, 203),

"p1" : (560, 860),
"p2" : (430, 560),
"p3" : (280, 430),
"p4" : (215, 280),
"p5" : (140, 215),
"p6" : (107, 140),

"invoice" : (140, 216),
"executive" : (184, 267),
"letter" : (216, 279),
"legal" : (216, 356),
"governmentletter" : (203, 267),
"governmentlegal" : (216, 330),
"ledger" : (432, 279),
"tabloid" : (279, 432),
"broadsheet" : (457, 610),

"post" : (394, 489),
"largepost" : (419, 533),
"elephant" : (584, 711),
"medium" : (457.2, 584.2),
"crown" : (381, 508),
"doublecrown" : (508, 762),
"royal" : (508, 635),
"quarto" : (229, 279),
"foolscap" : (210, 330),
"demy" : (445, 572),
"doubledemy" : (572, 889),
"quaddemy" : (889, 1143),
"dollarbill" : (76, 178),
"memo" : (140, 216),
"superb" : (330, 483),
"medium": (457, 584),

"ansi-a" : (216, 279),
"ansi-b" : (279, 432),
"ansi-c" : (432, 559),
"ansi-d" : (559, 864),
"ansi-e" : (864, 1118),

"arch-a" : (229, 305),
"arch-b" : (305, 457),
"arch-c" : (457, 610),
"arch-d" : (610, 914),
"arch-e" : (914, 1219),
"arch-e1" : (762, 1067),

"wt" : (86, 145),
"monarch" : (216, 279),
"deskfax" : (176, 250),
"classic" : (140, 216),
"franklincoveycompact" : (108, 171),
"timesystemcompact" : (85, 169),
"timesystempocket" : (100, 172),
"franklincoveypocket" : (89, 152),
"filofaxpocket" : (81, 120),
"midi" : (96, 172),
"personal" : (95, 171),
"chronoplanmini" : (79, 125),
"filofaxmini" : (67, 105),
"partner" : (75, 130),
"m2" : (64, 103),

"id0" : (25, 15),
"id1" : (85.60, 53.98),
"id2" : (105, 74),
"id3" : (125, 88),

"cdsingle" : (125.5, 123.5),
"cddouble" : (125.5, 247),
"dvdsingle" : (135, 190),
"dvddouble" : (135, 278)}
