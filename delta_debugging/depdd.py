import getopt, sys

tipass = None
tifail = None
main_file = None

def usage():
  print "python depdd.py --main something.tex"
  print "  --tipass <TEXTINPUTS for PASS-compilation>"
  print "  --tifail <TEXTINPUTS for FAIL-compilation>"

def main():
  try:
    opts, args = getopt.getopt(sys.argv[1:], 'h', ['help', 'main=', 'tipass=', 'tifail=', 'help'])
  except getopt.GetoptError, err:
    print str(err)
    sys.exit(2)
  assert not len(args), "Extra unparsed arguments: " + str(args)
  for o, a in opts:
    if o in ('-h', '--help'):
      usage()
      sys.exit(0)
    else:
      assert 0, "unhandled option " + o
  o_pass = run_recording(main_file, ti_pass)

if '__main__' == __name__:
  main()
