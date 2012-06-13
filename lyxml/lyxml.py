# LyX-XML roundtrip converter
# Oleg Parashchenko <olpa@ http://uucode.com/>
import sys, codecs, re, cStringIO

def lyx2xml(in_file, out_file):
  if '-' == in_file:
    h_in = sys.stdin
  else:
    h_in = open(in_file)
  if '-' == out_file:
    h_out = sys.stdout
  else:
    h_out = open(out_file, 'w')
  lyx2xml_h(h_in, h_out)
  if not (h_in == sys.stdin):
    h_in.close()
  if not (h_out == sys.stdout):
    h_out.close()

def lyx2xml_h(h_in, h_out):
  blob = BlobWriter(h_out)
  in_blob = 1
  stack   = []
  re_begin_layout = re.compile("^\\\\begin_layout \s*(\w+)$")
  h_out.write("<lyx>\n")
  for l in h_in:
    m = re_begin_layout.match(l)
    if m:
      blob.flush()
      el_name = m.group(1)
      stack.append((in_blob, el_name))
      in_blob = 0
      h_out.write('<' + el_name + '>')
      continue                                             # continue
    if '\\end_layout' == l.rstrip():
      (in_blob, el_name) = stack.pop()
      h_out.write('</' + el_name + ">\n")
      continue                                             # continue
    if in_blob:
      blob.write(l)
    else:
      h_out.write(l) # FIXME: decode, escape
  blob.flush()
  h_out.write("</lyx>\n")

re_empty = re.compile('^\s*$')

class BlobWriter:
  def __init__(self, h):
    self.blob = cStringIO.StringIO()
    self.h    = h

  def write(self, s):
    self.blob.write(s)

  def flush(self):
    s = self.blob.getvalue()
    self.blob.close()
    if not re_empty.match(s):
      self.h.write("<blob>TODO</blob>\n")
    self.blob = cStringIO.StringIO()

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
