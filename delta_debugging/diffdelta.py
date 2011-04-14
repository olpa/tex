import sys, difflib

class DiffDelta:

  def __init__(self, fname_pass, fname_fail):
    self.lines_pass = open(fname_pass, 'U').readlines()
    self.lines_fail = open(fname_fail, 'U').readlines()
    diff = difflib.SequenceMatcher(None, self.lines_pass, self.lines_fail)
    self.opcodes = diff.get_opcodes()

  def get_deltas(self):
    deltas = []
    i = 0
    for tag, _, _, _, _ in self.opcodes:
      if 'equal' != tag:
        deltas.append(i)
      i = i + 1
    return deltas

  def write_stream(self, h, deltas):
    i = -1
    for (tag, a1, a2, b1, b2) in self.opcodes:
      i = i + 1
      if i not in deltas:
        tag = 'equal'
      if ('replace' == tag) or ('insert' == tag):
        ll = self.lines_fail[b1:b2]
      elif 'delete' == tag:
        continue
      elif 'equal' == tag:
        ll = self.lines_pass[a1:a2]
      else:
        raise Exception("Unknown tag: " + tag)
      for l in ll:
        h.write(l)

  def write_file(self, fname, deltas):
    h = open(fname, 'w')
    self.write_stream(h, deltas)
    h.close()

  def write_diff(self, h, deltas):
    def write_range(x1, x2):
      if x1 == x2:
        h.write(str(x1))
      else:
        h.write("%i,%i" % (x1+1, x2))
    def write_tag(tag):
      if 'replace' == tag:
        h.write('c')
      elif 'delete' == tag:
        h.write('d')
      elif 'insert' == tag:
        h.write('a')
      else:
        raise Exception("Unknown diff tag: " + tag)
    for i in deltas:
      (tag, a1, a2, b1, b2) = self.opcodes[i]
      write_range(a1, a2)
      write_tag(tag)
      write_range(b1, b2)
      h.write("\n")
      for l in self.lines_pass[a1:a2]:
        h.write("< " + l)
      if (a1 != a2) and (b1 != b2):
        h.write("---\n")
      for l in self.lines_fail[b1:b2]:
        h.write("> " + l)

if '__main__' == __name__:
  (fname_pass, fname_fail) = sys.argv[1:]
  fd = DiffDelta(fname_pass, fname_fail)
  deltas = fd.get_deltas()
  print deltas
  #fd.write_diff(sys.stdout, deltas)
  fd.write_file('out', deltas)
