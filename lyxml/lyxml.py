# LyX-XML roundtrip converter
# Oleg Parashchenko <olpa@ http://uucode.com/>
import sys, codecs, re, cStringIO

#
# LyX file format
#
# Paragraph style:
# see lyx-2.0.3/src/Paragraph.cpp, Paragraph::write
#
# * \begin_layout name [annotations]
# * Options
# * For each child:
# . - META_INSET: direct write, or begin_inset ... end_inset
# . - '\':        \\backslash\n
# . - '.':        drops the trailing whitespace while writing .lyx
# * \end_layout
#
# Character style
# see lyx-2.0.3/src/insets/InsetFlex.cpp, InsetCollapsable.cpp,
# InsetText.cpp, Text.cpp
#
# 1. \begin_inset Flex name
# 2. "status collapsed" or "status open"
# 3. For each item in style: print. Usually it is a paragraph style
#    of name "Plain" and option "Layout":
#    3b. \begin_layout Plain Layout
#        ... text ...
#        \end_layout
# 4 \end_inset
# comes from
# (1):  Paragraph::write, InsetFlex::write
# (2):  InsetCollapsable::write
# (3):  Text::write
# (3b): Paragraph::write
# (4):  Paragraph::write
#
# There are also \begin_deeper and \end_deeper

# =========================================================

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
  blob  = BlobWriter(h_out)
  stack = []
  re_begin_layout = re.compile("^\\\\begin_layout \s*(\w+)\s*(.*)$")
  skip_lines = 1 # 1: till \begin_body, 2: one line after \begin_inset
  h_out.write("<lyx>\n")
  for l in h_in:
    if skip_lines:
      if 2 == skip_lines:
        skip_lines = 0
        continue                                           # continue
      blob.write(l)
      if '\\begin_body' == l[:11]:
        skip_lines = 0
      continue                                             # continue
    if not len(l):
      continue                                             # continue
    ch = l[0]
    if not('\\' == ch):
      blob.flush()
      h_out.write(l) # TODO: unescape and escape
      continue                                             # continue
    l = l.rstrip()
    if '\\backslash' == l:
      blob.flush()
      h_out.write('\\')
      continue                                             # continue
    if '\\end_layout' == l:
      blob.flush()
      (el_name, el_ann) = stack.pop()
      if not len(el_ann):
        h_out.write('</' + el_name + ">\n")
      continue                                             # continue
    m = re_begin_layout.match(l)
    if m:
      blob.flush()
      el_name = m.group(1)
      el_ann  = m.group(2)
      stack.append((el_name, el_ann))
      if not len(el_ann):
        h_out.write('<' + el_name + '>')
      continue                                             # continue
    if ('\\end_body' == l) or ('\\end_document' == l):
      continue                                             # continue
    blob.write(l)
  blob.flush()
  h_out.write("</lyx>\n")

re_empty = re.compile('^\s*$')

class BlobWriter:
  def __init__(self, h):
    self.blob = cStringIO.StringIO()
    self.h    = h

  def write(self, s):
    self.blob.write(s)

  def len(self):
    return self.blob.tell()

  def flush(self):
    if not(self.blob.tell()):
      return
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
