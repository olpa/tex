tmpdir          = 'tmp'
rundir_basename = 'run'
latex_cmdline   = 'latex -interaction batchmode -output-directory ${RUNDIR} ${FILENAME} 2>&1 >${RUNDIR}/stdout.txt'

import os, tempfile, string, sys

#
# Create a directory to run TeX. Design decision name:
#      ./tmp/run
# If exist, first rename existing, then create new.
#
def create_run_dir(tmpdir, rundir_basename):
  rundir = os.path.join(tmpdir, rundir_basename)
  if os.path.isdir(rundir):
    tempfile.tempdir = tmpdir
    newdir = tempfile.mktemp(prefix='run_')
    os.rename(rundir, newdir)
  os.makedirs(rundir)
  return rundir

def run_latex(rundir, filename):
  sub = {
      'RUNDIR':   rundir,
      'FILENAME': filename
      }
  cmdline = string.Template(latex_cmdline).substitute(sub)
  os.system(cmdline)

if '__main__' == __name__:
  fname = sys.argv[1]
  rundir = create_run_dir(tmpdir, rundir_basename)
  run_latex(rundir, fname)
