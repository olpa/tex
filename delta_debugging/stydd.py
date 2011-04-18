import sys

class OneCharDeltaFile:
  def __init__(self, fname):
    h = open(fname)
    s = h.read()
    h.close()
    self.deltas = zip(range(1, 1+len(s)), s)

  def get_deltas(self):
    return self.deltas

  def apply_deltas(self, deltas):
    s = ''
    for (_, ch) in deltas:
      s = s + ch
    return s

if '__main__' == __name__:
  fname = sys.argv[1]
  sty = OneCharDeltaFile(fname)
  deltas = sty.get_deltas()
  print sty.apply_deltas(deltas)
