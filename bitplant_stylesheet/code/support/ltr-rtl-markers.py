import sys
import libxml2
import ctfribidi

pbase_dir = 1 # 0 for LTR and 1 for RTL

def should_be_skipped(node):
  # TeXML/@escape=0
  pnode = node.parent
  if 'TeXML' == pnode.name:
    aval = pnode.prop('escape')
    return '0' == aval                                     # return
  # opt
  if pnode.name in ('opt', ):
    return 1                                               # return
  # cmd/@name=usepackage
  ppnode = pnode.parent
  if 'cmd' == ppnode.name:
    cname = ppnode.prop('name')
    return cname in ('usepackage', 'hypertarget', 'Chapter', 'Image', 'note', 'nullcell')          # return
  pppnode = ppnode.parent
  if 'cmd' == pppnode.name:
    cname = pppnode.prop('name')
    return cname == 'colwidths'                            # return
  # ok
  return 0

def insert_markers_node(node):
  s = unicode(node.content, 'utf8')
  lvl = ctfribidi.log2levels(s, pbase_dir)
  s2 = ctfribidi.insert_markers(s, lvl, pbase_dir)
  b = s2.encode('utf8')
  node.setContent(b)

def insert_markers_doc(xmldoc):
  el = xmldoc.getRootElement()
  while el:
    if 'text' == el.type:
      if not should_be_skipped(el):
        insert_markers_node(el)
    if el.children:
      el = el.children
      continue
    while el:
      if el.next:
        el = el.next
        break
      el = el.parent

(bdir, in_file, out_file) = sys.argv[1:]
assert '--rtl' == bdir

xmldoc = libxml2.parseFile(in_file)
assert xmldoc
insert_markers_doc(xmldoc)
assert xmldoc.saveFile(out_file)
sys.exit(0)
