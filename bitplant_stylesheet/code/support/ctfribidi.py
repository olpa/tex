import ctypes, ctypes.util

fb_name = ctypes.util.find_library('fribidi')
fb = ctypes.CDLL(fb_name)

def _preamble(s):
  if isinstance(s, unicode):
    utf8_bytes = s.encode('utf-8')
    n = len(s)
  else:
    utf8_bytes = s # assume that the strings are utf8
    n = len(unicode(s, 'utf8'))
  c_buf1 = ctypes.create_string_buffer(4*n) # fribidi: 4 bytes per char,
  c_buf2 = ctypes.create_string_buffer(4*n) # utf8: max 4 bytes per char
  n2 = fb.fribidi_utf8_to_unicode(utf8_bytes, len(utf8_bytes), c_buf1)
  assert n == n2
  return (c_buf1, c_buf2, n)

def log2vis(s, pbase_dir):
  (c_buf1, c_buf2, n) = _preamble(s)
  c_dir = ctypes.c_int(pbase_dir)
  fb.fribidi_log2vis(c_buf1, n, ctypes.byref(c_dir), c_buf2, None, None, None)
  fb.fribidi_unicode_to_utf8(c_buf2, n, c_buf1)
  s = unicode(c_buf1.value, 'utf8')
  return s

def log2levels(s, pbase_dir):
  (c_buf1, c_buf2, n) = _preamble(s)
  c_dir = ctypes.c_byte(pbase_dir)
  c_levels = (ctypes.c_byte * n)()
  ctypes.cast(c_levels, ctypes.POINTER(ctypes.c_byte))
  fb.fribidi_log2vis(c_buf1, n, ctypes.byref(c_dir), None, None, None, c_levels)
  return c_levels

# For LRE also insert ZWNJ around a number:
# http://tex.stackexchange.com/questions/214773/
def insert_markers(s, levels, pbase_dir):
  if not s:
    return
  start_markers = (u'\u202a', u'\u202b') # LRE, RLE = l-r and r-l embedding
  end_marker    = u'\u202c' # PDF = pop directional formatting
  zwnj          = u'\u200c' # ZERO WIDTH NON-JOINER
  dir_i = pbase_dir
  assert (0 == dir_i) or (1 == dir_i)
  while pbase_dir > levels[0]:
    pbase_dir = pbase_dir - 2
  last_level = pbase_dir
  need_zwnj = 0
  a = []
  for (ch, lvl) in zip(s, levels):
    # end of a number?
    #if need_zwnj:
    #  if (lvl != last_level) or (not ch.isdigit()):
    #    a.append(zwnj)
    #    need_zwnj = 0
    while lvl > last_level:
      dir_i = 1 - dir_i
      a.append(start_markers[dir_i])
      last_level = last_level + 1
      need_zwnj = 0
    while lvl < last_level:
      dir_i = 1 - dir_i
      a.append(end_marker)
      last_level = last_level - 1
      need_zwnj = 0
    # begin of a number?
    #if ch.isdigit():
    #  if not(last_level % 2):
    #    if not need_zwnj:
    #      a.append(zwnj)
    #    need_zwnj = 1
    a.append(ch)
  #if need_zwnj:
  #  a.append(zwnj)
  while lvl > pbase_dir:
    a.append(end_marker)
    lvl = lvl - 1
  return u''.join(a)
