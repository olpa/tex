import getopt, sys
import runlatex

def run_recording(tex_file, ti_pass):
  env = runlatex.RunEnv()
  runlatex.guess_latex_tool(env, tex_file)
  rl = runlatex.RunLatex(env)
  rl.create_run_dir()
  rl.run_latex_collect_errors(tex_file)

ti_pass = None
ti_fail = None
main_file = None

def usage():
  print "python depdd.py --main something.tex"
  print "  --tipass <TEXTINPUTS for PASS-compilation>"
  print "  --tifail <TEXTINPUTS for FAIL-compilation>"

def main():
  global main_file
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
    elif o in ('--main'):
      main_file = a
    else:
      assert 0, "unhandled option " + o
  assert main_file, "Main .tex-file is required"
  o_pass = run_recording(main_file, ti_pass)

if '__main__' == __name__:
  main()
