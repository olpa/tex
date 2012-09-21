# LyX-XML roundtrip converter
# Oleg Parashchenko <olpa@ http://uucode.com/>
import sys, os, codecs, re, cStringIO, xml.etree.ElementTree
import optparse, hashlib, anydbm
import lyxparser

lx_ns = 'http://getfo.org/lyxml/'
template_file = os.path.join(os.path.dirname(__file__), 'template.lyx')

# =========================================================
# LyX to XML

def lyx2xml(in_file, out_file, blob_file):
  if '-' == in_file:
    h_in = sys.stdin
  else:
    h_in = codecs.open(in_file, 'r', 'utf-8')
  if '-' == out_file:
    h_out = sys.stdout
  else:
    h_out = open(out_file, 'w')
  lyx2xml_h(h_in, h_out, blob_file)
  if not (h_in == sys.stdin):
    h_in.close()
  if not (h_out == sys.stdout):
    h_out.close()

# Not exactly as XML specification says, but should work for 99.999%
def is_xml_name_char(ch, is_start_char=0):
  if (':' == ch) or ('_' == ch):
    return 1
  n = ord(ch)
  if (n >= 65) and (n <= 90): # A...Z
    return 1
  if (n >= 97) and (n <= 122): # a...z
    return 1
  if n >= 0xc0:
    return 1
  if is_start_char:
    return 0
  if ('-' == ch) or ('.' == ch):
    return 1
  return (n >= 48) and (n <= 57) # 0...9

def xml_safe_name(s):
  a = []
  b = 1
  for ch in s:
    if is_xml_name_char(ch, b):
      a.append(ch)
    else:
      a.extend('_0x%x_' % ord(ch))
    b = 0
  return ''.join(a)

class XmlBuilder:

  def __init__(self):
    self.root  = xml.etree.ElementTree.Element('lx:lyx', {'xmlns:lx': 'http://getfo.org/lyxml/'})
    self.node  = self.root
    self.stack = []

  def header_line(self, l):
    pass

  def begin_body(self):
    pass

  def end_body(self):
    pass

  def opt_with_prefix(self, opts):
    new_opts = {}
    for (k, v) in opts.iteritems():
      new_opts['lx:'+xml_safe_name(k.strip())] = v # for image attributes
    return new_opts

  def begin_layout(self, lname, opts):
    self.stack.append(self.node)
    if 'Plain Layout' == lname:
      return                                               # return
    node = xml.etree.ElementTree.Element(xml_safe_name(lname), self.opt_with_prefix(opts))
    self.node.append(node)
    self.node = node

  def end_layout(self):
    if self.node.tail is None:
      self.node.tail = '\n'
    self.node = self.stack.pop()

  def begin_inset(self, itype, isubtype, opts):
    self.stack.append(self.node)
    gi = 'lx:' + itype
    if 'Flex' == itype:
      opts['ch'] = '1'
      gi = xml_safe_name(isubtype)
    else:
      if itype in ('script', 'Float'):
        gi = 'lx:' + isubtype
        isubtype = None
      if isubtype is not None:
        opts['ann'] = isubtype
    opts = self.opt_with_prefix(opts)
    node = xml.etree.ElementTree.Element(gi, opts)
    self.node.append(node)
    self.node = node

  def end_inset(self):
    self.node = self.stack.pop()

  def text(self, s):
    kids = self.node.getchildren()
    if kids:
      el = kids[-1]
      if el.tail is None:
        el.tail = s
      else:
        el.tail = el.tail + s
    else:
      if self.node.text is None:
        self.node.text = s
      else:
        self.node.text = self.node.text + s

def lyx2xml_h(h_in, h_out, blob_file):
  xb = XmlBuilder()
  lp = lyxparser.LyXparser(xb, h_in)
  lp.parse()
  h_out.write(xml.etree.ElementTree.tostring(xb.root, 'utf-8'))

# =========================================================
# XML to LyX
#
re_safe_string = re.compile('[\x00-\x19]+')
def lyx_safe_string(s):
  return re_safe_string.sub('_', s)

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

def copy_header(template_file, h_out, root):
  h = open(template_file)
  for l in h:
    l2 = l.rstrip()
    if '\\end_header' == l2:
      branches_seen = []
      for kid in root.findall('.//{http://getfo.org/lyxml/}branch'):
        branch_name = lyx_safe_string(kid.get('name', ''))
        if branch_name in branches_seen:
          continue
        branches_seen.append(branch_name)
        h_out.write("\\branch %s\n\\selected 1\n\\color linen\n\\end_branch\n" % branch_name)
    h_out.write(l)
    if '\\begin_body' == l2:
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
  root = tree.getroot()
  copy_header(template_file, h_out, root) # and insert branch names
  for kid in root.getchildren():
    x2l_layout(kid, None, {}, h_out)
  h_out.write("\n\\end_body\n\\end_document\n")
  if not (h_out == sys.stdout):
    h_out.close()
  blob.close_db()

# we want style names with semicolon
def xml_name_to_lyx_name(s):
  if '{' == s[0]:
    s = s[1:].replace('}', ':')
  return lyx_safe_string(s)

def x2l_layout(node, force_name, attr_from_inset, h_out):
  if force_name is None:
    gi = node.tag
    if '{http://getfo.org/lyxml/}' == gi[:25]: # an inset
      if gi[25:] in ('image', 'caption'):
        gi = 'Plain Layout'
      else:
        gi = 'Standard'
      h_out.write("\n\\begin_layout %s\n" % gi)
      x2l_inset(node, h_out)
      h_out.write("\n\\end_layout\n")
      return                                               # return
    gi = xml_name_to_lyx_name(gi)
  else:
    gi = force_name
  h_out.write("\n\\begin_layout %s\n" % gi)
  # TODO: parameters
  x2l_text(node.text, h_out)
  for kid in node.getchildren():
    x2l_inset(kid, h_out)
    x2l_text(kid.tail, h_out)
  h_out.write("\n\\end_layout\n")

inset_param_order = ('wide', 'sideways', 'status')
inset_param_order = ['{http://getfo.org/lyxml/}'+s for s in inset_param_order]

def x2l_inset(node, h_out):
  gi = node.tag
  if '{http://getfo.org/lyxml/}' != gi[:25]:
    h_out.write("\n\\begin_inset Flex %s\nstatus collapsed\n" % gi)
    x2l_layout(node, 'Plain Layout', {}, h_out)
    h_out.write("\n\\end_inset\n")
    return                                                 # return
  gi = xml_name_to_lyx_name(gi[25:])
  subtype = node.get('{http://getfo.org/lyxml/}ann')
  def_param = None
  if 'branch' == gi:
    gi = 'Branch'
    del(node.attrib['{http://getfo.org/lyxml/}ann'])
    def_param = {'status': 'open'}
  elif 'figure' == gi:
    gi      = 'Float'
    subtype = 'figure'
    def_param = {'wide': 'false', 'sideways': 'false', 'status': 'open'}
  elif 'image' == gi:
    gi = 'Graphics'
    def_param = {'filename': 'dummy.pdf', 'width': '5cm', 'height': '5cm'}
  elif 'caption' == gi:
    gi = 'Caption'
  elif gi in ('superscript', 'subscript'):
    subtype = gi
    gi = 'script'
  if subtype:
    h_out.write("\n\\begin_inset %s %s\n" % (gi, lyx_safe_string(subtype)))
  else:
    h_out.write("\n\\begin_inset %s\n" % gi)
  if def_param:
    for (k,v) in def_param.iteritems():
      node.attrib.setdefault('{http://getfo.org/lyxml/}'+k, v)
  xml_attr = {}
  for k in inset_param_order:
    v = node.attrib.get(k, None)
    if v is not None:
      h_out.write("%s %s\n" % (lyx_safe_string(k[25:]), lyx_safe_string(v)))
      del node.attrib[k]
  for (k, v) in node.attrib.iteritems():
    if '{http://getfo.org/lyxml/}' == k[:25]:
      h_out.write("%s %s\n" % (lyx_safe_string(k[25:]), lyx_safe_string(v)))
    else:
      xml_attr[k] = v
  # TODO: parameters
  # TODO: send parameters to layout
  # TODO: if there are children, two variants: layouts or insets
  if gi in ('Caption', 'script'):
    x2l_layout(node, 'Plain Layout', xml_attr, h_out)
  else:
    for kid in node.getchildren():
      x2l_layout(kid, None, xml_attr, h_out)
  h_out.write("\n\\end_inset\n")

def xml2lyx_rec_x(tree, h_out, do_drop_ws, blob, want_char):
  if want_char:
    on_attrib(tree.attrib, h_out)
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
    if '{http://getfo.org/lyxml/}branch' == gi:
      inset_name = lyx_safe_string(kid.get('name', ''))
      h_out.write("\n\\begin_layout Standard\n\\begin_inset Branch %s\nstatus open\n" % inset_name)
      xml2lyx_rec(kid, h_out, 0, blob, want_char=0)
      h_out.write("\n\\end_inset\n\\end_layout\n")
      on_text(kid.tail, h_out, do_drop_ws)
      continue                                            # continue
    if '{http://getfo.org/lyxml/}figure' == gi:
      h_out.write("\n\\begin_layout Standard\n\\begin_inset Float figure\nwide false\nsideways false\nstatus open\n")
      xml2lyx_rec(kid, h_out, 0, blob, want_char=0)
      h_out.write("\n\\end_inset\n\\end_layout\n")
      on_text(kid.tail, h_out, do_drop_ws)
      continue                                            # continue
    if '{http://getfo.org/lyxml/}caption' == gi:
      h_out.write("\n\\begin_layout Standard\n\\begin_inset Caption\n\\begin_layout Plain Layout\n")
      xml2lyx_rec(kid, h_out, 0, blob, want_char=1)
      h_out.write("\n\\end_layout\n\\end_inset\n\\end_layout\n")
      on_text(kid.tail, h_out, do_drop_ws)
      continue                                            # continue
    if '{http://getfo.org/lyxml/}image' == gi:
      h_out.write("\n\\begin_layout Standard\n\\begin_inset Graphics\n")
      h_out.write("\tfilename %s\n" % lyx_safe_string(kid.get('file', 'dummy.png')))
      h_out.write("\twidth %s\n" % lyx_safe_string(kid.get('width', '')))
      h_out.write("\theight %s\n" % lyx_safe_string(kid.get('height', '')))
      h_out.write("\n\\end_inset\n\\end_layout\n")
      on_text(kid.tail, h_out, do_drop_ws)
      continue                                            # continue
    if gi in ('{http://getfo.org/lyxml/}superscript','{http://getfo.org/lyxml/}subscript'):
      ann = gi[gi.index('}')+1:]
      h_out.write("\n\\begin_inset script %s\n" % ann)
      gi = 'Plain Layout'
    elif want_char or ('1' == kid.get('{http://getfo.org/lyxml/}ch')):
      if 1 != kid.get('{http://getfo.org/lyxml/}ch'):
        print >>sys.stderr, 'lyxml: nested paragraph styles are not supported (%s)' % gi
      h_out.write("\n\\begin_inset Flex %s\nstatus collapsed\n" % gi)
      gi = 'Plain Layout'
    # namespaced GI: actually, we want style names with semicolon
    if '{' == gi[0]:
      gi = gi[1:].replace('}', ':')
    h_out.write("\n\\begin_layout %s\n" % gi)
    xml2lyx_rec(kid, h_out, 0, blob, want_char=1)
    h_out.write("\n\\end_layout\n")
    if 'Plain Layout' == gi:
      h_out.write("\n\\end_inset\n")
    on_text(kid.tail, h_out, do_drop_ws)

# split large line on smaller ones: taken from LyX source code,
# see 'Paragraph::write'
def x2l_text(s, h_out):
  if s is None:
    return                                                 # return
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

def on_attrib(attrib, h_out):
  for aitem in attrib.iteritems():
    h_out.write("\\begin_inset Flex XmlAttribute\nstatus collapsed\n")
    h_out.write("\n\\begin_layout Plain Layout\n")
    on_text("%s=%s" % aitem, h_out, 0)
    h_out.write("\n\\end_layout\n")
    h_out.write("\n\\end_inset\n\n")

# =========================================================
# Parse command line
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
