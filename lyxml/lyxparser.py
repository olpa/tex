# Callback-parser of a LyX document
# There is no official grammar, but there is enough regularity
# to suggest our own.
#
# LYX      := HEADER, BEGIN_DOCUMENT, DOCUMENT, END_DOCUMENT
# DOCUMENT := LAYOUT*
#
# LAYOUT   := LAYOUT_BEGIN, LAYOUT_OPTION*, (CHARDATA | INSET)*, LAYOUT_END
# LAYOUT_BEGIN   := \begin_layout LAYOUT_NAME
#                   Can contain spaces (special name "Plain Layout")
# LAYOUT_OPTION  := OPTION_NAME OPTION_VALUE?
# OPTION_NAME    := Name prefixed with slash. Should not be confused
#                   with character data '\backslash' .....
# LAYOUT_END     := \end_layout
#
# INSET          := INSET_BEGIN, INSET_OPTION*, LAYOUT*, INSET_END
# INSET_BEGIN    := \begin_inset INSET_NAME INSET_ANNOTATION*
# INSET_OPTION   := OPTION_NAME OPTION_VALUE
# INSET_END      := \end_inset
#
class LyXparserException(Exception):
  pass

LEX_STATE_EOF = 0

class LyXparser:

  def __init__(self, callback, in_stream):
    self.lex_state  = 1
    self.callback   = callback
    self.lineno     = 0
    self.in_stream  = in_stream
    self.line_back  = None

  def read_next_line(self):
    if self.line_back:
      l = self.line_back
      self.line_back = None
      return l
    self.lineno = self.lineno + 1
    l = h.readline()
    if '' == l:
      self.lex_state = LEX_STATE_EOF
    return l.rstrip("\r\n")

  def read_next_line_not_empty(self):
    while self.lex_state:
      l = self.read_next_line()
      if not('' == l):
        return l
    return ''

  def put_line_back(self, l):
    assert(self.line_back is None)
    self.line_back = l

  def error(self, msg):
    raise LyXparserException("parse error, line %i: %s" % (self.lineno, msg))

  def parse(self):
    while self.lex_state:
      l = self.read_next_line()
      if '\\begin_body' == l:
        self.callback.begin_body()
        break                                               # break
      else:
        self.callback.header_line(l)
    if not self.lex_state:
      self.error('No ''\\begin_body'' ')                    # raise
    self.parse_layout_list()
    l = self.read_next_line_not_empty()
    if not ('\\end_body' == l):
      self.error('Expected ''\\end_body'', got ' + l)       # raise
    self.callback.end_body()

  def parse_layout_list(self):
    while self.lex_state:
      # Get '\\begin_layout'
      while self.lex_state:
        l = self.read_next_line_not_empty()
        if not ('\\begin_layout ' == l[:14]):
          self.put_line_back(l)
          return                                           # return
        layout_name = l[14:].lstrip()
        break                                              # break
      # Get options
      opts = {}
      while self.lex_state:
        l = self.read_next_line_not_empty()
        if '\\' == l[0]:
          a = l[1:].split(' ', 2)
          opt_name = a[0]
          if opt_name in ('end_layout', 'begin_inset', 'backslash'):
            break                                          # break
          if 2 == len(a):
            opts[opt_name] = a[1]
          else:
            opts[opt_name] = None
      self.callback.begin_layout(layout_name, opts)
      # Parse text till end_layout
      self.put_line_back(l)
      while self.lex_state:
        l = self.read_next_line_not_empty()
        if '\\' == l[0]:
          a = l.split(' ', 2)
          cmd_name = a[0]
          if '\\end_layout' == cmd_name:
            self.callback.end_layout()
            break                                          # break
          if '\\begin_inset' == cmd_name:
            self.parse_inset(l)
            continue                                       # continue
          if not ('\\backslash' == cmd_name):
            self.error("Unknown command while parsing layout: " + cmd_name) # raise
        l = l.replace('\\backslash', '\\')
        self.callback.text(l)
      #
      if not (l == '\\end_layout'):
        self.error('Missed \\end_layout')                  # raise

  def parse_inset(self, l):
    a = l.split(' ', 3)
    inset_type = a[1]
    if len(a) == 3:
      inset_subtype = a[2]
    else:
      inset_subtype = None
    opts = {}
    while self.lex_state:
      l = self.read_next_line_not_empty()
      if '\\' == l[0]:
        break
      a = l.split(' ', 2)
      if len(a) == 2:
        opts[a[0]] = a[1]
      else:
        opts[a[0]] = None
    if not self.lex_state:
      self.error('End of file while parsing an inset')     # raise
    self.callback.begin_inset(inset_type, inset_subtype, opts)
    cmd = l.split(' ')[0]
    if '\\begin_layout' == cmd:
      self.put_line_back(l)
      self.parse_layout_list()
      l = self.read_next_line_not_empty()
    if '\\end_inset' == l:
      self.callback.end_inset()
      return                                               # return
    self.error('Unknown command in inset: ' + l)           # raise

if '__main__' == __name__:
  import sys
  class LyXparserCallback:
    def header_line(self, s):
      print '(hl)',
    def begin_body(self):
      print '(bd)',
    def end_body(self):
      print '(ed)',
    def begin_layout(self, lname, opts):
      print '(%s:%s)' % (lname, opts),
    def end_layout(self):
      print '(el)',
    def begin_inset(self, itype, isubtype, opts):
      print '(%s:%s:%s)' % (itype, isubtype, opts),
    def end_inset(self):
      print '(ei)',
    def text(self, t):
      print '(t)',
  fname = sys.argv[1]
  cb = LyXparserCallback()
  h = open(fname)
  lp = LyXparser(cb, h)
  lp.parse()
  h.close()
