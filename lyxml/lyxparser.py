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
    l = self.read_next_line()
    if not ('\\end_body' == l):
      self.error('Expected ''\\end_body'', got ' + l)       # raise
    self.callback.end_body()

  def parse_layout_list(self):
    while self.lex_state:
      l = self.read_next_line()
      if '\\end_body' == l:
        self.put_line_back(l)
        return                                             # return

class LyXparserCallback:

  def header_line(self, s):
    print '(hl)',

  def begin_body(self):
    print '(bd)',

  def end_body(self):
    print '(ed)',

cb = LyXparserCallback()
h = open('chap1.lyx')
lp = LyXparser(cb, h)
lp.parse()
h.close()
