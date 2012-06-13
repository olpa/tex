# LyX-XML roundtrip converter
# Oleg Parashchenko <olpa@ http://uucode.com/>
import sys, codecs

def lyx2xml(in_file, out_file):
  if '-' == in_file:
    h_in = sys.stdin
  else:
    h_in = open(in_file)
  if '-' == out_file:
    h_out = sys.stdout
  else:
    h_out = open(out_file, 'w')
  for l in h_in:
    h_out.write(l)
  if not (h_in == sys.stdin):
    h_in.close()
  if not (h_out == sys.stdout):
    h_out.close()

# =========================================================
# Parse command line
#
mode_lyx2xml = 0
mode_xml2lyx = 0
in_file      = None
out_file     = None
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

#
# Open files and start conversion
#
if mode_lyx2xml:
  lyx2xml(in_file, out_file)
if mode_xml2lyx:
  print >>sys.stderr, 'lyxml: XML to LyX is not supported yet.'
  sys.exit(-1)
