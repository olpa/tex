# LyX-XML roundtrip converter
# Oleg Parashchenko <olpa@ http://uucode.com/>
import sys

#
# The mode of work
#
mode_lyx2xml = 0
mode_xml2lyx = 0
in_file      = None
out_file     = None

#
# Parse command line
#
for a in sys.argv[1:]:
  if '--lyx2xml' == a:
    mode_lyx2xml = 1
  elif '--xml2lyx' == a:
    mode_xml2lyx = 1
  else:
    if in_file is None:
      in_file = a
    elif out_file is None:
      out_file = a
    else:
      print >>sys.stderr, 'lyxml: too many command arguments'
      sys.exit(-1)
if mode_lyx2xml and mode_xml2lyx:
  print >>sys.stderr, 'lyxml: both --lyx2xml and --xml2lyx are given'
  sys.exit(-1)
if not(mode_lyx2xml) and not(mode_xml2lyx):
  if in_file is not None:
    ext = in_file[-4:].lower()
    if '.lyx' == ext:
      mode_lyx2xml = 1
    elif '.xml' == ext:
      mode_xml2lyx = 1
if not(mode_lyx2xml) and not(mode_xml2lyx):
  print >>sys.stderr, 'lyxml: no --lyx2xml or --xml2lyx is given, and can\'t guess direction'
  sys.exit(-1)
if out_file is None:
  out_file = '-'
if in_file is None:
  in_file = '-'

print '!!!!!!!!!!!!!!', in_file, out_file, mode_lyx2xml, mode_xml2lyx
