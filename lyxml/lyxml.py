# LyX-XML roundtrip converter
# Oleg Parashchenko <olpa@ http://uucode.com/>
import sys, os, codecs, re, cStringIO, xml.etree.ElementTree
import optparse, hashlib, anydbm

lx_ns = 'http://getfo.org/lyxml/'
template_file = os.path.join(os.path.dirname(__file__), 'template.lyx')

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
#
# More at
# http://wiki.lyx.org/Devel/LyXFileFormatReverse

# =========================================================
# LyX to XML

def html_escape(s):
  s = s.replace('&', '&amp;')
  s = s.replace('<', '&lt;')
  s = s.replace('>', '&gt;')
  return s

def lyx2xml(in_file, out_file, blob_file):
  if '-' == in_file:
    h_in = sys.stdin
  else:
    h_in = open(in_file)
  if '-' == out_file:
    h_out = sys.stdout
  else:
    h_out = open(out_file, 'w')
  lyx2xml_h(h_in, h_out, blob_file)
  if not (h_in == sys.stdin):
    h_in.close()
  if not (h_out == sys.stdout):
    h_out.close()

def lyx2xml_h(h_in, h_out, blob_file):
  blob  = BlobWriter(h_out, blob_file)
  stack = [('#dummy','#dummy')]
  re_begin_layout = re.compile("^\\\\begin_layout (?P<ename>\w+)\s*(?P<eann>.*)$")
  re_begin_inset  = re.compile("^\\\\begin_inset (?P<eann>\w+) (?P<ename>\w+)$")
  def begin_end_tag(l, name, ann, is_end):
    is_not_plain  = ('Plain' != name) or ('Layout' != ann)
    is_char_style = 'Flex' == ann
    if len(ann) and not(is_char_style):
      if is_not_plain:
        blob.write(l)
    else:
      blob.flush()
      h_out.write('<')
      if is_end:
        h_out.write('/')
      h_out.write(name)
      if is_char_style and not(is_end):
        h_out.write(' lx:ch="1"')
      if is_end and is_not_plain and not(is_char_style):
        h_out.write(">\n")
      else:
        h_out.write('>')
  skip_lines = -1 # -1: till \begin_body, -2: till \end_inset, N: how much (after \begin_inset)
  inset_level = 0
  h_out.write("<lx:lyx xmlns:lx='%s'>\n" % lx_ns)
  for l in h_in:
    if skip_lines:
      if skip_lines > 0:
        skip_lines = skip_lines - 1
        continue                                           # continue
      blob.write(l)
      if '\\begin_body' == l[:11]:
        skip_lines = 0
      elif '\\end_inset' == l[:10]:
        inset_level = inset_level - 1
        if not inset_level:
          skip_lines = 0
      elif '\\begin_inset' == l[:12]:
        inset_level = inset_level + 1
      continue                                             # continue
    l = l.rstrip("\r\n")
    if not len(l):
      continue                                             # continue
    ch = l[0]
    if not('\\' == ch):
      blob.flush()
      h_out.write(html_escape(l))
      continue                                             # continue
    if '\\backslash' == l:
      blob.flush()
      h_out.write('\\')
      continue                                             # continue
    if ('\\end_layout' == l) or ('\\end_inset' == l):
      (el_name, el_ann) = stack.pop()
      begin_end_tag(l, el_name, el_ann, 1)
      continue                                             # continue
    m = re_begin_layout.match(l)
    if not m:
      m = re_begin_inset.match(l)
      if m:
        skip_lines = 1
        if m.group('eann') != 'Flex':
          skip_lines  = -2
          inset_level = 1
          blob.write(l+"\n")
          continue                                         # continue
    if m:
      el_name = m.group('ename')
      el_ann  = m.group('eann')
      stack.append((el_name, el_ann))
      begin_end_tag(l, el_name, el_ann, 0)
      continue                                             # continue
    if ('\\end_body' == l) or ('\\end_document' == l):
      continue                                             # continue
    blob.write(l+"\n")
  blob.flush()
  blob.close_db()
  h_out.write("</lx:lyx>\n")

re_empty = re.compile('^\s*$')

class BlobWriter:
  def __init__(self, h, fname):
    self.h     = h
    self.fname = fname
    self.db    = None
    self.blob  = cStringIO.StringIO()

  def get_db(self):
    if not self.db:
      self.db = anydbm.open(self.fname, 'c')
    return self.db

  def close_db(self):
    if self.db:
      self.db.close()

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
      s_hash = hashlib.md5(s).hexdigest()
      self.h.write('<?LyXblob %s?>' % s_hash)
      db = self.get_db()
      db[s_hash] = s
    self.blob = cStringIO.StringIO()

# =========================================================
# XML to LyX
#
class BlobReader:
  def __init__(self, blob_file):
    self.blob_file     = blob_file
    self.db            = None
    self.nodb_reported = 0

  def get_db(self):
    if not self.db:
      if not self.nodb_reported:
        try:
          self.db = anydbm.open(self.blob_file, 'r')
        except anydbm.error, e:
          print >>sys.stderr, 'lyxml: can\'t open blob file: %s' % e
          self.nodb_reported = 1
    return self.db

  def get(self, key):
    db = self.get_db()
    if db:
      if db.has_key(key):
        return db[key]
      else:
        print >>sys.stderr, 'lyxml: blob not found: \'%s\'' % key
        return ''
    else:
      return ''

  def close_db(self):
    if self.db:
      self.db.close()

xetxtb_saved_init = xml.etree.ElementTree.XMLTreeBuilder.__init__
def xetxtb_new_init(self, *ls, **kw):
  def new_pi(target, data):
    self._parser.StartElementHandler('*PI*', ['target', target, 'data', data])
    self._parser.EndElementHandler('*PI*')
  xetxtb_saved_init(self, *ls, **kw)
  self._parser.ProcessingInstructionHandler = new_pi
xml.etree.ElementTree.XMLTreeBuilder.__init__ = xetxtb_new_init

def copy_header(template_file, h_out):
  h = open(template_file)
  for l in h:
    h_out.write(l)
    if '\\begin_body' == l.rstrip():
      break
  h.close()

def xml2lyx(in_file, out_file, blob_file):
  if '-' == in_file:
    xml_in = sys.stdin
  else:
    xml_in = in_file
  tree = xml.etree.ElementTree.ElementTree()
  tree.parse(xml_in)
  if '-' == out_file:
    h_out = sys.stdout
  else:
    h_out = codecs.open(out_file, 'w', 'utf8')
  blob = BlobReader(blob_file)
  # The document header is supposed to be stored in the first
  # processing instruction, before any styles. Otherwise use
  # the header from the template
  root = tree.getroot()
  if '*PI*' != root.getchildren()[0].tag:
    copy_header(template_file, h_out)
  xml2lyx_rec(root, h_out, do_drop_ws=1, blob=blob)
  h_out.write("\n\\end_body\n\\end_document\n")
  if not (h_out == sys.stdout):
    h_out.close()
  blob.close_db()

def xml2lyx_rec(tree, h_out, do_drop_ws, blob):
  on_text(tree.text, h_out, do_drop_ws)
  for kid in tree.getchildren():
    gi = kid.tag
    if '*PI*' == gi:
      if 'LyXblob' == kid.get('target'):
        h_out.write(blob.get(kid.get('data')))
      on_text(kid.tail, h_out, do_drop_ws)
      continue                                            # continue
    if '{http://getfo.org/lyxml/}newline' == gi:
      h_out.write("\n\\begin_inset Newline newline\n\\end_inset\n")
      on_text(kid.tail, h_out, do_drop_ws)
      continue                                            # continue
    if '1' == kid.get('{http://getfo.org/lyxml/}ch'):
      h_out.write("\n\\begin_inset Flex %s\nstatus collapsed\n" % gi)
      gi = 'Plain Layout'
    # namespaced GI: actually, we want style names with semicolon
    if '{' == gi[0]:
      gi = gi[1:].replace('}', ':')
    h_out.write("\n\\begin_layout %s\n" % gi)
    xml2lyx_rec(kid, h_out, 0, blob)
    h_out.write("\n\\end_layout\n")
    if 'Plain Layout' == gi:
      h_out.write("\n\\end_inset\n")
    on_text(kid.tail, h_out, do_drop_ws)

# split large line on smaller ones: taken from LyX source code,
# see 'Paragraph::write'
def on_text(s, h_out, do_drop_ws):
  if s is None:
    return
  if do_drop_ws and re_empty.match(s):
    return
  col = 0
  for ch in s:
    if '\\' == ch:
      h_out.write("\n\\backslash\n")
      col = 0
      continue                                             # continue
    if ((col > 70) and (' ' == ch)) or (col > 79) or ('\n' == ch):
      h_out.write("\n")
      col = 0
      if (' ' == ch) or ('\n' == ch):
        h_out.write(' ')
        col = 1
      continue                                             # continue
    h_out.write(ch)
    col = col + 1

def on_blob(s, h_out):
  s = base64.b64decode(s)
  h_out.write(s)

# =========================================================
# Parse command line
# TODO: template file
#
usage = "usage: %prog [options] source target"
parser = optparse.OptionParser(usage)
parser.add_option("-b", "--blob", dest="blob_file",
                      help="read/store blobs in BLOB_FILE")
parser.add_option("-x", "--xml2lyx", dest="x2l",
    action="store_true", help="mode: from LyXML to LyX")
parser.add_option("-l", "--lyx2xml", dest="l2x",
    action="store_true", help="mode: from LyX to LyXML")
parser.add_option("-t", "--template", dest="tpl",
    action="store", type="string", help="use the system header from the .lyx file")
(options, args) = parser.parse_args()
if options.l2x and options.x2l:
  parser.error("both --lyx2xml and --xml2lyx are given")
  sys.exit(-1)
if options.tpl:
  template_file = options.tpl
if len(args) > 2:
  parser.error("incorrect number of arguments")
  sys.exit(-1)

in_file  = None
out_file = None
for a in args:
  if in_file is None:
    in_file = a
  else:
    out_file = a
if not(options.l2x) and not(options.x2l):
  if in_file is not None:
    ext = os.path.splitext(in_file)[1].lower()
    if '.lyx' == ext:
      options.l2x = 1
    elif ext in ('.xml', '.lyxml'):
      options.x2l = 1
if not(options.l2x) and not(options.x2l):
  parser.error("no --lyx2xml or --xml2lyx is given, and can\'t guess direction")
  sys.exit(-1)
if out_file is None:
  out_file = '-'
if in_file is None:
  in_file = '-'

blob_file = options.blob_file
if blob_file is None:
  if options.l2x:
    f = out_file
  else:
    f = in_file
  if '-' != f:
    blob_file = os.path.splitext(f)[0] + '.dbm'
  else:
    blob_file = 'blobs.dbm'

#
# Open files and start conversion
#
if options.l2x:
  lyx2xml(in_file, out_file, blob_file)
else:
  xml2lyx(in_file, out_file, blob_file)
