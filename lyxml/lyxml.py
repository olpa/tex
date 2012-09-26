# LyX-XML roundtrip converter
# Oleg Parashchenko <olpa@ http://uucode.com/>
import sys, os, codecs, re, cStringIO, xml.etree.ElementTree
import optparse, hashlib, anydbm
import lyxparser

lx_ns = 'http://getfo.org/lyxml/'
template_file = os.path.join(os.path.dirname(__file__), 'template.lyx')

# =========================================================
# LyX to XML

def lyx2xml(in_file, out_file):
  if '-' == in_file:
    h_in = sys.stdin
  else:
    h_in = codecs.open(in_file, 'r', 'utf-8')
  if '-' == out_file:
    h_out = sys.stdout
  else:
    h_out = open(out_file, 'w')
  lyx2xml_h(h_in, h_out)
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

def reformat_lyx_xml(node):
  no_cdata = node.text is None
  if no_cdata:
    for kid in node.getchildren():
      if kid.tail:
        no_cdata = 0
        break
  if no_cdata:
    node.text = '\n'
  for kid in node.getchildren():
    if kid.tail is None:
      kid.tail = '\n'

class XmlBuilder:
  re_xml_tag_name  = re.compile('<(\\w+)')
  re_xml_attr_pair = re.compile('''(\\w+)\\s*=\\s*["']([^"']*)["']''')

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
    self.node = self.stack.pop()

  def begin_inset(self, itype, isubtype, opts):
    self.stack.append(self.node)
    itype = itype.lower()
    if itype in ('tabular', 'text'):
      # Tabular is created by XML option 'lyxtabular'.
      # 'Text' appears inside a table cell. Probably redundant.
      return                                               # return
    gi = 'lx:' + itype
    if 'flex' == itype:
      gi = xml_safe_name(isubtype)
    else:
      if itype in ('script', 'float'):
        gi = 'lx:' + isubtype
        isubtype = None
      if isubtype is not None:
        opts['ann'] = isubtype
    opts = self.opt_with_prefix(opts)
    node = xml.etree.ElementTree.Element(gi, opts)
    self.node.append(node)
    self.node = node

  def end_inset(self):
    reformat_lyx_xml(self.node)
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

  def xml_line(self, l):
    if '/' == l[1]:
      reformat_lyx_xml(self.node)
      self.node = self.stack.pop()
      return                                               # return
    m = XmlBuilder.re_xml_tag_name.match(l)
    gi = 'lx:' + str(m.group(1))
    opts = {}
    for m in XmlBuilder.re_xml_attr_pair.finditer(l):
      opts['lx:' + str(m.group(1))] = str(m.group(2))
    node = xml.etree.ElementTree.Element(gi, opts)
    self.node.append(node)
    if gi not in ('lx:features', 'lx:column'):
      self.stack.append(self.node)
      self.node = node

def lyx2xml_h(h_in, h_out):
  xb = XmlBuilder()
  lp = lyxparser.LyXparser(xb, h_in)
  lp.parse()
  reformat_lyx_xml(xb.root)
  h_out.write(xml.etree.ElementTree.tostring(xb.root, 'utf-8'))

# =========================================================
# XML to LyX
#
re_safe_string = re.compile('[\x00-\x19]+')
def lyx_safe_string(s):
  return re_safe_string.sub('_', s)

def copy_header(template_file, h_out, root):
  h = open(template_file)
  for l in h:
    l2 = l.rstrip()
    if '\\end_header' == l2:
      branches_seen = []
      for kid in root.findall('.//{http://getfo.org/lyxml/}branch'):
        branch_name = lyx_safe_string(kid.get('{http://getfo.org/lyxml/}ann', ''))
        if branch_name in branches_seen:
          continue
        branches_seen.append(branch_name)
        h_out.write("\\branch %s\n\\selected 1\n\\color linen\n\\end_branch\n" % branch_name)
    h_out.write(l)
    if '\\begin_body' == l2:
      break
  h.close()

def xml2lyx(in_file, out_file):
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
  root = tree.getroot()
  copy_header(template_file, h_out, root) # and insert branch names
  for kid in root.getchildren():
    x2l_layout(kid, None, {}, h_out)
  h_out.write("\n\\end_body\n\\end_document\n")
  if not (h_out == sys.stdout):
    h_out.close()

# we want style names with semicolon
def xml_name_to_lyx_name(s):
  if '{' == s[0]:
    s = s[1:].replace('}', ':')
  return lyx_safe_string(s)

def x2l_layout(node, force_name, attr_from_inset, h_out):
  if force_name is None:
    gi = node.tag
    if '{http://getfo.org/lyxml/}' == gi[:25]: # an inset
      local_gi = gi[25:]
      if local_gi in ('features', 'column', 'row', 'cell'):
        x2l_inset(node, h_out)
        return                                             # return
      if local_gi in ('image', 'lyxtabular', 'caption'):
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
  xml_attr = {}
  for (k, v) in node.attrib.iteritems():
    if '{http://getfo.org/lyxml/}' == k[:25]:
      h_out.write("\\%s %s\n" % (lyx_safe_string(k[25:]), lyx_safe_string(v)))
    else:
      xml_attr[k] = v
  xml_attr.update(attr_from_inset)
  for (k, v) in xml_attr.iteritems():
    fake_node = xml.etree.ElementTree.Element('XmlAttribute')
    fake_node.children = []
    fake_node.text = '%s=%s' % (k, v)
    x2l_inset(fake_node, h_out)
  x2l_text(node.text, h_out)
  for kid in node.getchildren():
    x2l_inset(kid, h_out)
    x2l_text(kid.tail, h_out)
  h_out.write("\n\\end_layout\n")

inset_param_order = ('wide', 'sideways', 'status')
inset_param_order = ['{http://getfo.org/lyxml/}'+s for s in inset_param_order]

# lx-namespace and local name, or None and full name
def split_gi(gi):
  if '{http://getfo.org/lyxml/}' == gi[:25]:
    return ('http://getfo.org/lyxml/', gi[25:])
  else:
    return (None, gi)

def x2l_inset(node, h_out):
  gi = node.tag
  (ns, local_gi) = split_gi(gi)
  if ns is None:
    h_out.write("\n\\begin_inset Flex %s\nstatus collapsed\n" % gi)
    x2l_layout(node, 'Plain Layout', {}, h_out)
    h_out.write("\n\\end_inset\n")
    return                                                 # return
  if '{http://getfo.org/lyxml/}lyxtabular' == gi:
    x2l_tabular(node, h_out)
    return                                                 # return
  gi = local_gi
  subtype = node.get('{http://getfo.org/lyxml/}ann')
  def_param = None
  if 'branch' == gi:
    gi = 'Branch'
    del(node.attrib['{http://getfo.org/lyxml/}ann'])
    def_param = {'status': 'open'}
  elif 'figure' == gi:
    gi      = 'Float'
    subtype = 'figure'
  elif 'table' == gi:
    gi      = 'Float'
    subtype = 'table'
  elif 'image' == gi:
    gi = 'Graphics'
    def_param = {'filename': 'dummy.pdf', 'width': '5cm', 'height': '5cm'}
  elif 'caption' == gi:
    gi = 'Caption'
  elif gi in ('superscript', 'subscript'):
    subtype = gi
    gi = 'script'
  if 'Float' == gi:
    def_param = {'wide': 'false', 'sideways': 'false', 'status': 'open'}
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
  if gi in ('Caption', 'script'):
    x2l_layout(node, 'Plain Layout', xml_attr, h_out)
  else:
    for kid in node.getchildren():
      x2l_layout(kid, None, xml_attr, h_out)
  h_out.write("\n\\end_inset\n")

def x2l_xmlline(node, local_name, postponed_attr, h_out):
  h_out.write("\n<" + local_name)
  for k,v in node.attrib.iteritems():
    (k1, k2) = split_gi(k)
    if k1 is None:
      postponed_attr[k] = v
    else:
      h_out.write(' %s="%s"' % (k2, lyx_safe_string(v)))
  h_out.write('>')

def x2l_tabular(node, h_out):
  userattr = {}
  h_out.write("\n\\begin_inset Tabular")
  x2l_xmlline(node, 'lyxtabular', userattr, h_out)
  for kid_tbl in node.getchildren():
    if '{http://getfo.org/lyxml/}features' == kid_tbl.tag:
      x2l_xmlline(kid_tbl, 'features', userattr, h_out)
    elif '{http://getfo.org/lyxml/}column' == kid_tbl.tag:
      x2l_xmlline(kid_tbl, 'column', userattr, h_out)
    elif '{http://getfo.org/lyxml/}row' == kid_tbl.tag:
      x2l_xmlline(kid_tbl, 'row', userattr, h_out)
      for kid_row in kid_tbl.getchildren():
        if '{http://getfo.org/lyxml/}cell' == kid_row.tag:
          x2l_xmlline(kid_row, 'cell', userattr, h_out)
          h_out.write("\n\\begin_inset Text")
          a = kid_row.getchildren()
          if len(a):
            for kid_cell in a:
              x2l_layout(kid_cell, None, userattr, h_out)
          else:
            kid_row.attrib = {}
            x2l_layout(kid_row, 'Plain Layout', userattr, h_out)
          h_out.write("\n\\end_inset\n</cell>")
        else:
          print >>sys.stderr, "lyxml: unknown row child '%s'" % kid_tbl.tag
      h_out.write("\n</row>")
    else:
      print >>sys.stderr, "lyxml: unknown table child '%s'" % kid_tbl.tag
  h_out.write("\n</lyxtabular>\n\\end_inset")

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

# =========================================================
# Parse command line
#
usage = "usage: %prog [options] source target"
parser = optparse.OptionParser(usage)
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

#
# Open files and start conversion
#
if options.l2x:
  lyx2xml(in_file, out_file)
else:
  xml2lyx(in_file, out_file)
