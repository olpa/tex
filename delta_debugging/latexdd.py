import os, sys, re, getopt, logging
import DD
import runlatex, decider

logger_deltas = logging.getLogger('deltas')

#
# LaTeX file consist of parts:
# * classname       - {} part of \documentclass
# * classoptions    - [] part of \documentclass
# * preamble        - everything after \documentclass{} till \begin{document}
# * document        - inside \begin{document}...\end{document}
# Parsing is fragile.
#
re_dclass = re.compile('\\\\documentclass(\\[([^]]*)\\])?\{([^}]*)\}\\s*')
class LatexFileDelta:
  def __init__(self):
    self.deltas = None

  def load_from_file(self, fname):
    h = open(fname)
    s = h.read()
    h.close()
    m = re_dclass.search(s)
    if not m:
      raise Exception("\\documentclass not found")
    self.classoptions = m.group(2)
    self.classname    = m.group(3)
    s = s[m.end():]
    pos = s.index('\\begin{document}')
    self.preamble = s[:pos].strip()
    pos2 = s.index('\\end{document}')
    self.document = s[16+pos:pos2].strip()

  def get_deltas(self):
    def nop(*ls):
      pass
    if self.deltas is None:
      self.create_deltas()
    return range(len(self.deltas))

  def start_new_doc(self, with_content):
    lf = LatexFileDelta()
    if with_content:
      lf.classname    = self.classname
      lf.classoptions = self.classoptions
      lf.preamble     = self.preamble
      lf.document     = self.document
    else:
      lf.classname = 'minimal'
      lf.classoptions = lf.preamble = lf.document = ''
    return lf

  #
  # Save file
  #
  def write_stream(self, h):
    h.write('\\documentclass')
    if self.classoptions:
      h.write('[%s]' % self.classoptions)
    h.write("{%s}" % self.classname)
    if self.preamble:
      h.write("\n")
      h.write(self.preamble)
    h.write("\n\\begin{document}\n")
    h.write(self.document)
    if not self.document:
      h.write('Some text to get pages')
    h.write("\n\\end{document}\n")

  def write_file(self, fname):
    h = open(fname, 'w')
    self.write_stream(h)
    h.close()

  def write_file_for_deltas(self, fname, idx_deltas):
    lf = self.apply_idx_deltas(idx_deltas)
    lf.write_file(fname)

  def apply_idx_deltas(self, idx_deltas):
    deltas = [self.deltas[i] for i in idx_deltas]
    return self.apply_deltas(deltas)

def debug_prepare_deltas_for_print(idces, chunker):
  d = [chunker.deltas[i] for i in idces]
  d = [s if len(s)<=16 else s[:13]+'...' for s in d]
  return d

class LatexFileDeltaLineChar(LatexFileDelta):

  def __init__(self, delta_mode, *ls, **kw):
    LatexFileDelta.__init__(self, *ls, **kw)
    self.delta_mode = delta_mode

  #
  # Each delta is one character. Not effective, but straightforward.
  # Technically, a delta is a three-item entry: (where, index, letter):
  # * where  - O (options), N (name), P (preamble), D (document)
  # * index&letter - which letter to change
  #
  def create_deltas(self):
    deltas = []
    if 'minimal' != self.classname:
      deltas.append(('N', None, None))
    def process_part(where, s):
      index = 1
      if s is not None:
        if 'line' == self.delta_mode:
          s = s.split("\n")
          s = [l+"\n" for l in s]
        for ch in s:
          deltas.append((where, index, ch))
          index = index + 1
    process_part('O', self.classoptions)
    process_part('P', self.preamble)
    process_part('D', self.document)
    self.deltas = deltas
    return deltas

  #
  # Apply deltas
  # According to DD documentation, the deltas are sorted
  #
  def apply_deltas(self, deltas):
    lf = self.start_new_doc(with_content=0)
    for (where, index, ch) in deltas:
      if 'D' == where:
        lf.document = lf.document + ch
      elif 'P' == where:
        lf.preamble = lf.preamble + ch
      elif 'O' == where:
        lf.classoptions = lf.classoptions + ch
      elif 'N' == where:
        lf.classname = self.classname
      else:
        raise Exception("Unsupported delta: " + where)
    return lf

#
class LatexFileDeltaBlock(LatexFileDelta):

  def __init__(self, re_list):
    LatexFileDelta.__init__(self)
    self.re_list = []
    for r in re_list:
      c = re.compile(r)
      self.re_list.append(c)

  def where_does_line_start_chunk(self, l):
    for r in self.re_list:
      m = r.search(l)
      if m:
        return m.start()
    return None

  def create_deltas(self):
    deltas = []
    a = []
    for l in self.document.split("\n"):
      i = self.where_does_line_start_chunk(l)
      if i is not None:
        if i > 0:
          a.append(l[:i])
          l = l[i:]
        if a:
          deltas.append("\n".join(a))
          a = []
      a.append(l)
    if a:
      deltas.append("\n".join(a))
    self.deltas = deltas
    return deltas

  def apply_deltas(self, deltas):
    lf = self.start_new_doc(with_content=1)
    lf.document = "\n".join(deltas)
    return lf

#
class LatexFileDeltaCmd(LatexFileDelta):

  def create_deltas(self):
    re_cmd = re.compile('\\\\[A-Za-z@]+')
    self.deltas = deltas = []
    s = self.document
    while 1:
      m = re_cmd.search(s)
      if not m:
        break
      i = m.start()
      if i > 0:
        deltas.append(s[:i])
      j = m.end()
      deltas.append(s[i:j])
      s = s[j:]
    if s:
      deltas.append(s)
    return deltas

  def apply_deltas(self, deltas):
    lf = self.start_new_doc(with_content=1)
    lf.document = "".join(deltas)
    return lf

# =========================================================
# DD
#
class LatexDD(DD.DD):
  def __init__(self, env, fname, digger, chunker):
    DD.DD.__init__(self)
    self.env = env
    self.chunker = chunker
    self.base_fname = os.path.basename(fname)
    chunker.load_from_file(fname)
    if logger_deltas.isEnabledFor(logging.DEBUG):
      logger_deltas.debug("LatexDD:__init__: " + str(debug_prepare_deltas_for_print(chunker.get_deltas(), chunker)))
    self.last_run = None
    self.decider = decider.decider()
    self.decider.extract_master_errors(self)

  def _test(self, deltas):
    if logger_deltas.isEnabledFor(logging.DEBUG):
      logger_deltas.debug("LatexDD:_test: " + str(debug_prepare_deltas_for_print(deltas, self.chunker)))
    self.last_run = rl = runlatex.RunLatex(self.env)
    rundir = rl.create_run_dir()
    fname = os.path.join(rundir, self.base_fname)
    self.chunker.write_file_for_deltas(fname, deltas)
    rl.run_latex_collect_errors(fname)
    ccode = self.decider.get_result(rl)
    return ccode

  def get_last_run(self):
    return self.last_run

  def test_with_no_deltas(self):
    return self._test([])

  def test_with_all_deltas(self):
    return self._test(self.get_deltas())

  def coerce(self, c):
    if len(c) < 10:
      s = str(c)
    else:
      s = str(c[:10]) + '........'
    return s

  def get_deltas(self):
    deltas = self.chunker.get_deltas()
    if logger_deltas.isEnabledFor(logging.DEBUG):
      logger_deltas.debug("LatexDD:get_deltas: " + str(debug_prepare_deltas_for_print(deltas, self.chunker)))
    return deltas

# ---------------------------------------------------------

def usage():
  print "python latexdd.py --main something.tex --out new.tex"
  print "  [--stop-after-master]"
  print "  [--chunker char/line/cmd[2]/section] [--chunker-ini settings]*"
  print "The default chunker is \"line\"."
  print "Only \"section\" chunker gets required initial settings."
  print "Each chunker-ini is an regular expression for a start of a section."

def main(digger=None, chunker=None):
  main_file         = None
  stop_after_master = 0
  arg_chunker       = "line"
  arg_chunker_ini   = []
  out_file          = None
  args = sys.argv[1:]
  if not args:
    args = ['-h']
  try:
    opts, args = getopt.getopt(args, 'h', ['help', 'main=', 'out=', 'chunker=', 'chunker-ini=', 'stop-after-master', 'help'])
  except getopt.GetoptError, err:
    print str(err)
    sys.exit(2)
  assert not len(args), "Extra unparsed arguments: " + str(args)
  for o, a in opts:
    if o in ('-h', '--help'):
      usage()
      sys.exit(0)
    elif '--main' == o:
      main_file = a
    elif '--stop-after-master' == o:
      stop_after_master = 1
    elif '--out' == o:
      out_file = a
    elif '--chunker' == o:
      arg_chunker = a
    elif '--chunker-ini' == o:
      arg_chunker_ini.append(a)
    else:
      assert 0, "unhandled option " + o
  assert main_file, "Main .tex-file is required"
  if not stop_after_master:
    assert out_file, "Output .tex-file is required"
  if not chunker:
    if 'line' == arg_chunker:
      chunker = LatexFileDeltaLineChar('line')
    elif 'char' == arg_chunker:
      chunker = LatexFileDeltaLineChar('char')
    elif 'section' == arg_chunker:
      chunker = LatexFileDeltaBlock(arg_chunker_ini)
    elif 'cmd' == arg_chunker:
      chunker = LatexFileDeltaCmd()
    else:
      assert 0, "Unknown chunker name (expected line/char/section): '%s'" % arg_chunker
  env = runlatex.RunEnv()
  runlatex.guess_latex_tool(env, main_file)
  dd = LatexDD(env, main_file, digger, chunker)
  dd.decider.print_master_errors()
  if stop_after_master:
    sys.exit(0)
  deltas = dd.get_deltas()
  c = dd.ddmin(deltas)
  chunker.write_file_for_deltas(out_file, c)

if '__main__' == __name__:
  logging.basicConfig(filename='latex_dd_log', level=logging.DEBUG)
  main()
