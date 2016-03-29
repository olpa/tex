import os, SCons, texloginfo

# =========================================================
# Builder: XML to TeXML
#

#
# Transformation of parameters from as associative array to command line
#
def texml_params_to_xslt_params(target, source, env, for_signature):
  x_params = []
  t_params = env.get('TEXML_PARAMS', {})
  for k,v in t_params.iteritems():
    x_params.append('--stringparam')
    x_params.append(k)
    x_params.append(v)
  return x_params

def texml_emitter(target, source, env):
  if env.get('XSLTPROC_TEXML_PARAMS') is None:
    env['XSLTPROC_TEXML_PARAMS'] = texml_params_to_xslt_params
  return (target, source)

XMLtoTeXML = SCons.Builder.Builder(action=[['$XSLTPROC', '$XSLTPROC_PARAMS', '$XSLTPROC_TEXML_PARAMS', '-o', '$TARGET', '$TEXML_XSLT', '$SOURCE']], emitter=texml_emitter)


# =========================================================
# Builder: TeX compilation
#

#
# Common code for running and printing what is going to run
#
def gen_cmdline(target, source, env):
  tex_file = str(source[0])
  tex_dir  = os.path.dirname(tex_file)
  tex_file = os.path.basename(tex_file)
  redir    = '>/dev/null'
  try:
    redir = ' >' + os.devnull
  except:
    if '\r' == os.linesep: # Mac
      redir = '>Dev:Nul'
    elif '\r\n' == os.linesep: # Windows
      redir = '>NUL'
  cmdline  = ['$TEX_COMMAND']
  cmdline.extend(env.get('TEX_COMMAND_PARAMS', []))
  cmdline.extend(['${SOURCE.file}', redir])
  if 'texenv' in SCons.Script.COMMAND_LINE_TARGETS:
    cmdline = 'bash'
  return cmdline

def calc_texinputs(env):
  texin = []
  for directory in env.get('TEX_INCLUDE_DIRS', []):
    texin.append(os.path.abspath(directory))
  for directory in env.get('TEX_IMAGES_DIRS', []):
    texin.append(os.path.abspath(directory))
  texin.append(env['ENV'].get('TEXINPUTS', ''))
  return os.pathsep.join(texin)

# Used only for debug purpose, to know the value of the OSFONTDIR
# variable for the default settings.
def calc_fonts(env):
  fd = []
  for d in env.get('TEX_INCLUDE_DIRS', []):
    if os.path.isdir(d):
      ls = os.listdir(d)
      for f in ls:
        if ('.ttf' in f) or ('.otf' in f) or ('.ttc' in f):
          fd.append(d)
          break
    d = os.path.join(d, 'fonts')
    if os.path.isdir(d):
      fd.append(d)
  return ':'.join(fd)

def run_tex_help(target, source, env):
  texin   = calc_texinputs(env)
  cmdline = gen_cmdline(target, source, env)
  cmdline = "TEXINPUTS=%s\n%s" % (texin, cmdline)
  fd = calc_fonts(env)
  if fd:
    cmdline = "OSFONTDIR=%s\n%s" % (fd, cmdline)
  return env.subst(cmdline, source=source)

#
# Execute LaTeX
#
def run_tex_func(target, source, env):
  # Setup TeX environment
  texin = calc_texinputs(env)
  env['ENV']['TEXINPUTS'] = texin
  env['ENV']['HOME']      = os.getenv('HOME')
  s = env['ENV'].get('OSFONTDIR', '')
  s = s + ':' + calc_fonts(env)
  env['ENV']['OSFONTDIR'] = s
  # TeX command-line action
  cmdline = gen_cmdline(target, source, env)
  action  = SCons.Action.CommandAction(cmdline)
  #
  # Run TeX
  #
  reruns    = 0
  rerun_why = ''
  rerun_max = env.get('TEX_RERUN_MAX', 3)
  while reruns < rerun_max:
    reruns = reruns + 1
    if reruns > 1:
      print '*** re-running TeX: %s' % rerun_why
    #
    # Run LaTeX
    #
    old_dir = os.getcwd()
    tex_file = str(source[0])
    tex_dir  = os.path.dirname(tex_file)
    os.chdir(tex_dir)
    ccode = action.execute(target, source, env)
    os.chdir(old_dir)
    if ccode > 1:
      return ccode
    #
    # Parse TeX log, decide if re-run is required
    #
    tli = texloginfo.texloginfo()
    log_fname = env.get('TEX_LOG_FILE')
    log_fname = env.subst(log_fname, source=source, target=target)
    tli.parse_log_file(log_fname)
    tex_warnings = tli.get_warnings()
    tex_errors   = tli.get_errors()
    need_rerun   = tli.get_rerun()
    #
    # 1) If error, no re-run. 2) If the log says so, re-run
    #
    if tex_errors != '': break
    if 0 != need_rerun:
      rerun_why = 'advice from the log file'
      continue
    break
  else:
    #
    # Too much re-runs
    #
    raise SCons.Errors.BuildError(target, 'After %i attempts, re-run is still required. Human inspection is required.' % rerun_max)
  if tex_warnings:
    print tex_warnings,
  if tex_errors != '':
    raise SCons.Errors.BuildError(target, "\n" + tex_errors)
  return 0

#
# Add more dependencies
#
def tex_emitter(target, source, env):
  env['TEX_COMMAND_PARAMS'] = ['--interaction', 'batchmode']
  env['TEX_LOG_FILE']       = '${TARGET.base}.log'
  node = env.Alias(['tmppdf', 'texenv'], target)
  if 'texenv' in SCons.Script.COMMAND_LINE_TARGETS:
    env.AlwaysBuild(target)
  fbase = os.path.splitext(str(target[0]))[0]
  for ext in ['.aux', '.log', '.toc', '.out', '.pdfsync', '.pdfsync.gz']:
    env.Clean(target, fbase + ext)
  return (target, source)

tex_action = SCons.Action.Action(run_tex_func, run_tex_help)
TeXtoPDF = SCons.Builder.Builder(action=tex_action, emitter=tex_emitter)

#
# Parsing LaTeX log file
#
def grep_log(target, source, env):
  log_file   = str(source[0])
  str_target = str(target[0])
  tli = Consodoc.Builders.texloginfo.texloginfo()
  tli.parse_log_file(log_file)
  if 'warnings' == str_target:
    print tli.get_warnings(),
    return None
  if 'errors' == str_target:
    print tli.get_errors(),
    return None
  assert 'missed' == str_target
  print tli.get_missed(),

# =========================================================
# Common
#

TeXMLtoTeX = SCons.Builder.Builder(action=[['$TEXML_TOOL', '$TEXML_TOOL_PARAMS', '$SOURCE', '$TARGET']])

ApplyPatch = SCons.Builder.Builder(action=[SCons.Defaults.Copy('$TARGET', '$SOURCE'), ['$PATCH', '$TARGET', '<', '$PATCH_FILE']], PATCH_FILE='patch-file-here')

GeneratePatchFile = SCons.Builder.Builder(action=[['-$DIFF', '-u', '--text', '--strip-trailing-cr', '$NOEDIT_SOURCE', '$SOURCE', '>', '$TARGET']], NOEDIT_SOURCE='${SOURCE}.orig')

def get_default_vars_copy():
  kw = {
    'PYTHON':        'python',
    'JAVA':          'java',
    'XSLTPROC':      'xsltproc',
    'XSLTPROC_PARAMS':       ['--nonet'],
    'TEXML_TOOL':         'texml',
    'TEXML_TOOL_PARAMS':  ['--encoding', 'utf-8'],
    'DIFF':               'diff',
    'PATCH':              'patch',
    'TEX_COMMAND':        'xelatex',
    }
  return kw.copy()
