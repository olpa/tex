# Copy LyX style from file to file
usage = 'python stylecp.py from_file to_file style_mask'

import sys

def read_header(h):
  s = ''
  for l in h:
    s = s + l
    l = l.rstrip()
    if '\\end_header' == l:
      break
  return s

if len(sys.argv) not in (3,4):
  print >>sys.stderr, 'Usage: ' + usage
  sys.exit(-1)
in_file  = sys.argv[1]
out_file = sys.argv[2]
if 4 == len(sys.argv):
  mask = sys.argv[3]
else:
  mask = '*'

h = open(in_file)
s = read_header(h)
print s
h.close()
