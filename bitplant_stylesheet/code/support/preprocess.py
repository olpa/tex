import sys, libxml2, re, os, xml.dom.minidom, codecs
import cals, indexer

if os.path.isdir('/home/olpa/p/hp/python-common'):
  sys.path.append('/home/olpa/p/hp/python-common')
import Bitplant.FramemakerXml

in_file  = sys.argv[1]
out_file = sys.argv[2]

try:
  doc = Bitplant.FramemakerXml.parse_fm_file(in_file, drop_dtd_system=1)
except TypeError:
  doc = Bitplant.FramemakerXml.parse_fm_file(in_file)

# ========================================================
# Delete "suppresshy"
#
ctxt = doc.xpathNewContext()
res = ctxt.xpathEval('//suppresshy')
for node in res:
  node.unlinkNode()

# =========================================================
# Resolve image entities, change extension
#
res = ctxt.xpathEval('//Figure | //SafetyPicto | //Icon')
for node in res:
  try:
    fname = node.prop('file')
    if fname is None:
      ename = node.prop('entity')
      edef  = doc.docEntity(ename)
      fname = edef.getBase(doc)
    fname  = fname.replace('\\', '/')
    fname  = os.path.basename(fname)
    fname  = os.path.splitext(fname)[0] + '.pdf'
    node.setProp('file', fname)
  except libxml2.treeError:
    pass

# =========================================================
# "Unpack" the elements "Variant"
#
res = ctxt.xpathEval('//Variant')
for node in res:
  s1 = unicode(node.prop('Variable') or '', 'utf-8').strip()
  s2 = unicode(node.prop('KeySequence') or '', 'utf-8').strip()
  s3 = unicode(node.prop('Comment') or '', 'utf-8').strip()
  s = ''
  if s1 or s2:
    s = s1 + s2 + '; '
  if s3:
    s = s + '(' + s3 + ')'
  if s:
    s = s.encode('utf-8')
    pi_node = node.doc.newDocPI('variant-begin', s)
    node.addPrevSibling(pi_node)
    pi_node = node.doc.newDocPI('variant-end', s)
    node.addNextSibling(pi_node)
    while node.children:
      kid_node = node.children
      kid_node.unlinkNode()
      node.addPrevSibling(kid_node)
    node.unlinkNode()

# =========================================================
# ID/IDREF: allow only ASCII and digits
#
def as_hex(m):
  ch = str(m.group(0))
  return 'X%X' % ord(ch)
re_nonascii=re.compile('[^a-zA-Z0-9]') # \W does not work due to underscore
res = ctxt.xpathEval('//@id | //@idref')
for node in res:
  node.parent.setProp(node.name, re_nonascii.sub(as_hex, node.content))

# =========================================================
# Index generation
#
def regenerate_index(doc, index_node, ctxt, use_locale):
  #
  # Indexing
  #
  res = ctxt.xpathEval('//IndexEntry/@text')
  words = []
  for node in res:
    first_word = node.content
    first_word = unicode(first_word, 'UTF-8')
    pos = first_word.find(':')
    if -1 == pos:
      second_word = ''
    else:
      (first_word, second_word) = (first_word[:pos], first_word[pos+1:])
    words.append(indexer.word_rec(node.parent, first_word, second_word))
  indexer.preprocess_words(words, use_locale)
  words = indexer.group_words_by_the_letter(words)
  words = indexer.group_words_by_the_first_word(words)
  words = indexer.group_words_by_the_second_word(words)
  #
  # Index to XML
  #
  ids_seen = []
  while index_node.children:
    index_node.children.unlinkNode()
  def add_title_node(doc, parent_node, title_text):
    parent_node.newTextChild(None, 'Title', title_text.encode('UTF-8'))
  for eq_letter in words:
    letter_node = doc.newDocNode(None, 'IndexGroupLetter', None)
    index_node.addChild(letter_node)
    add_title_node(doc, letter_node, eq_letter[0][0][0].letter)
    for eq_first in eq_letter:
      first_node = doc.newDocNode(None, 'IndexGroupFirst', None)
      letter_node.addChild(first_node)
      add_title_node(doc, first_node, eq_first[0][0].first_word)
      for eq_second in eq_first:
        second_node = doc.newDocNode(None, 'IndexGroupSecond', None)
        first_node.addChild(second_node)
        add_title_node(doc, second_node, eq_second[0].second_word)
        for word in eq_second:
          leaf_node = doc.newDocNode(None, 'IndexLeaf',None)
          second_node.addChild(leaf_node)
          s_id = 'autoidx%dx%dx%d' % (word.sort_pos_letter, word.sort_pos_first_word, word.sort_pos_second_word)
          while s_id in ids_seen:
            s_id = s_id + 'x'
          ids_seen.append(s_id)
          leaf_node.newProp('idref', s_id)
          word.elem.newProp('id',    s_id)

res = ctxt.xpathEval('//IndexAnnex')
if len(res): # should be only once
  regenerate_index(doc, res[0], ctxt, 'de_DE.UTF-8')

# =========================================================
# Save and cleanup
#
tmp_file = out_file + '0'
doc.saveFile(tmp_file)
ctxt.xpathFreeContext()
del ctxt
doc.freeDoc()

# =========================================================
# And now re-load and split tables
doc = xml.dom.minidom.parse(tmp_file)
res = doc.getElementsByTagName('tgroup')
for node in res:
  tblo = cals.cals_table(doc, node)
  tblo.split()
if '-' == out_file:
  h = codecs.getwriter('utf8')(sys.stdout)
else:
  h = codecs.open(out_file, 'w', 'utf-8')
doc.writexml(h)
h.close()

os.unlink(tmp_file)
