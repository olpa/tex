import getopt, sys, os, shutil
import runlatex

def run_recording(tex_file, ti):
  env = runlatex.RunEnv()
  runlatex.guess_latex_tool(env, tex_file)
  env.set_extra_latex_opt('-recorder')
  env.set_texinputs(ti)
  rl = runlatex.RunLatex(env)
  env.set_rundir('run_recording_pass')
  rundir = rl.create_run_dir()
  rl.run_latex_collect_errors(tex_file)
  tbname = os.path.basename(tex_file)
  fls_file = os.path.join(rundir, os.path.splitext(tbname)[0]+'.fls')
  seen = [tbname]
  for l in open(fls_file):
    if 'INPUT ' != l[:6]:
      continue
    fname = l[6:].strip()
    if not os.path.isabs(fname):
      continue
    bname = os.path.basename(fname)
    if bname in seen:
      continue
    seen.append(bname)
    tgt_fname = os.path.join(rundir, bname)
    shutil.copy(fname, tgt_fname)

def usage():
  print "python depdd.py --main something.tex"
  print "  --tipass <TEXTINPUTS for PASS-compilation>"
  print "  --tifail <TEXTINPUTS for FAIL-compilation>"

def main():
  ti_pass = None
  ti_fail = None
  main_file = None
  args = sys.argv[1:]
  if not args:
    args = ['-h']
  try:
    opts, args = getopt.getopt(args, 'h', ['help', 'main=', 'tipass=', 'tifail=', 'help'])
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
    elif '--tipass' == o:
      ti_pass = a
    elif '--tifail' == o:
      ti_fail = a
    else:
      assert 0, "unhandled option " + o
  assert main_file, "Main .tex-file is required"
  o_pass = run_recording(main_file, ti_pass)

if '__main__' == __name__:
  main()
