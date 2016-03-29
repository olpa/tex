import sys
import re
try:
  import icu
except:
  import PyICU
  icu = PyICU
import unicodedata
import xml.etree.ElementTree

(in_file, out_file) = sys.argv[1:]
etree = xml.etree.ElementTree.parse(in_file)
lang = etree.getroot().get('language')
lang_locale = icu.Locale.createFromName(lang)

re_space_collapse = re.compile('\\s\\s+')

# Format: hash of hashes of hashes etc
# title points to primaries, which point to secondaries,
# which point to IDs.
dict_sections = {}

#
# Does not work for all languages. Also, using "string[0]"
# is incorrect to get the first letter.
#
def get_section_title(ch):
  nkfd_form = unicodedata.normalize('NFKD', unicode(ch))
  nkfd_ch   = nkfd_form[0]
  cat = unicodedata.category(nkfd_ch)
  if 'L' != cat[0]:   # Not a letter
    return ''
  if 'l' != cat[1]:   # Not a lower-case letter (uppercase or special)
    return nkfd_ch
  return unicode(icu.UnicodeString(nkfd_ch).toUpper(lang_locale))

def add_entry(title, primary, secondary, idx_id, nopage):
  dict_primaries   = dict_sections.setdefault(title, {})
  dict_secondaries = dict_primaries.setdefault(primary, {})
  arr_ids          = dict_secondaries.setdefault(secondary, [])
  if not nopage:
    arr_ids.append(idx_id)

def process_entry(idx_id, idx_text):
  #
  # One entry is actually several entries at once.
  #
  if ';' in idx_text:
    for var in idx_text.split(';'):
      process_entry(idx_id, var)
    return
  #
  # Detect a nopage-marker
  #
  nopage = 0
  pos = idx_text.find('<$nopage>')
  if -1 != pos:
    nopage = 1
    idx_text = idx_text[:pos] + idx_text[pos+9:]
  #
  # Split on term and subterm. Skip empty entries.
  #
  idx_text = re_space_collapse.sub(' ', idx_text)
  pos = idx_text.find(':')
  if pos < 0:
    primary   = idx_text
    secondary = ''
  else:
    primary   = idx_text[:pos]
    secondary = idx_text[pos+1:].strip()
  primary = primary.strip()
  if '' == primary:
    primary = secondary
  if not primary:
    return
  add_entry(get_section_title(primary[0]), primary, secondary, idx_id, nopage)

def entries_to_xml():
  collator = icu.Collator.createInstance(lang_locale)
  root = xml.etree.ElementTree.Element('index')
  root.text = "\n"
  for section_title in sorted(dict_sections.keys(), cmp=collator.compare):
    node_sect  = xml.etree.ElementTree.SubElement(root, 'index_section')
    node_sect.tail = "\n"
    node_title = xml.etree.ElementTree.SubElement(node_sect, 's')
    node_title.text = section_title
    node_title.tail = "\n"
    dict_primary = dict_sections[section_title]
    for primary in sorted(dict_primary.keys(), cmp=collator.compare):
      node_prim = xml.etree.ElementTree.SubElement(node_sect, 'primary')
      node_prim.tail = "\n"
      node_s = xml.etree.ElementTree.SubElement(node_prim, 's')
      node_s.text = primary
      node_s.tail = "\n"
      dict_secondary = dict_primary[primary]
      primary_refs = dict_secondary.pop('', None)
      if primary_refs:
        node_prim.set('idrefs', " ".join(primary_refs))
      for secondary in sorted(dict_secondary.keys(), cmp=collator.compare):
        node_sec = xml.etree.ElementTree.SubElement(node_prim, 'secondary')
        node_sec.tail = "\n"
        node_s = xml.etree.ElementTree.SubElement(node_sec, 's')
        node_s.text = secondary
        node_sec.set('idrefs', "".join(dict_secondary[secondary]))
  return root

for elem in etree.findall('IndexEntry'):
  process_entry(elem.get('id'), elem.get('text'))
idx_root = entries_to_xml()

h = open(out_file, 'w')
h.write(xml.etree.ElementTree.tostring(idx_root, 'utf-8'))
h.close()
