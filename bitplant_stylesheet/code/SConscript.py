import os, glob

this_sconscript_file = (lambda x:x).func_code.co_filename
code_base   = os.path.dirname(this_sconscript_file)
support_dir = os.path.join(code_base, 'support')

include_path = [support_dir]
Export('include_path')

import os, glob
this_sconscript_file = (lambda x:x).func_code.co_filename
code_base   = os.path.dirname(this_sconscript_file)
support_dir = os.path.join(code_base, 'support')

Alias('sty_depends', glob.glob(os.path.join('support', '*.sty')))
Alias('xsl_depends', glob.glob(os.path.join('support', '*.xsl')))

if ARGUMENTS.get('dev', 0) == '1':
  Import('include_path')
  include_path.append(support_dir)

import os
this_sconscript_file = (lambda x:x).func_code.co_filename
code_base   = os.path.dirname(this_sconscript_file)
support_dir = os.path.join(code_base, 'support')

if ARGUMENTS.get('dev', 0) == '1':
  Import('include_path')
  include_path.append(support_dir)

import os
this_sconscript_file = (lambda x:x).func_code.co_filename
code_base   = os.path.dirname(this_sconscript_file)
support_dir = os.path.join(code_base, 'support')

Alias('sty_depends', os.path.join(support_dir, 'fnwing.sty'))

if ARGUMENTS.get('dev', 0) == '1':
  Import('include_path')
  include_path.append(support_dir)

import os, sys, glob, re, types, SCons.Builder
this_sconscript_file = (lambda x:x).func_code.co_filename
code_base   = os.path.dirname(this_sconscript_file)
support_dir = os.path.join(code_base, 'support')
sys.path.append(support_dir)
import ConsodocII

def get_default_vars():
  kw = ConsodocII.get_default_vars_copy()
  kw['PREPROCESS_PY']  =  '$SUPPORT/preprocess.py'
  kw['TEXML_RTL_MARKERS_PY']  =  '$SUPPORT/ltr-rtl-markers.py'
  kw['SUPPORT']        =  support_dir,
  kw['TEXML_XSLT']     =  '$SUPPORT/bitplant.xsl'
  if os.path.isdir('/Applications'): # we are working on a Mac
    kw['ITEXT']  = '/opt/local/share/java/iText.jar'
  elif os.path.exists('/usr/share/java/itext1.jar'):
    kw['ITEXT']  = '/usr/share/java/itext1.jar'
  else:
    kw['ITEXT']  = '/usr/share/java/itext.jar'
  return kw

import os
this_sconscript_file = (lambda x:x).func_code.co_filename
code_base   = os.path.dirname(this_sconscript_file)
support_dir = os.path.join(code_base, 'support')

Alias('sty_depends', os.path.join(support_dir, 'admon.sty'))
Alias('xsl_depends', os.path.join(support_dir, 'admon.xsl'))

if ARGUMENTS.get('dev', 0) == '1':
  Import('include_path')
  include_path.append(support_dir)

import os, glob
this_sconscript_file = (lambda x:x).func_code.co_filename
code_base   = os.path.dirname(this_sconscript_file)
support_dir = os.path.join(code_base, 'support')

Alias('sty_depends', glob.glob(os.path.join(support_dir, '*.fd')))
Alias('sty_depends', os.path.join(support_dir, 'multifont.sty'))

if ARGUMENTS.get('dev', 0) == '1':
  Import('include_path')
  include_path.append(support_dir)

def set_paths_to_fonts(env, include_path):
  fonts_include = []
  for inc_dir in include_path:
    fn_inc_dir = os.path.join(inc_dir, 'fonts')
    if os.path.isdir(fn_inc_dir):
      fonts_include.append(fn_inc_dir)
  macosx_pubserver_dir = '/opt/local/share/fonts'
  if os.path.isdir(macosx_pubserver_dir):
    for fname in os.listdir(macosx_pubserver_dir):
      font_dir = os.path.join(macosx_pubserver_dir, fname)
      if os.path.isdir(font_dir):
        fonts_include.append(font_dir)
  for fd in ('/usr/share/fonts/truetype/arphic',
      '/usr/share/fonts/ttf/cjkuni-ukai',
      '/usr/share/fonts/truetype/unfonts-core',
      '/usr/share/fonts/ttf/un-core',
      '/usr/share/fonts/opentype/ipafont-gothic',
      '/usr/share/fonts/ttf/ipa-gothic',
      '/usr/share/fonts/opentype/fonts-hosny-amiri',
      '/usr/share/fonts/ttf/amiri'
      ):
    if os.path.isdir(fd):
      fonts_include.append(fd)
  if len(fonts_include):
    env['ENV'] = os.environ
    env['ENV']['OSFONTDIR'] = os.pathsep.join(fonts_include)

Export('set_paths_to_fonts')

Import('*')

if ARGUMENTS.get('dev', 0) == '1':
  Import('include_path')
  include_path.append(support_dir)

PreprocessXML = SCons.Builder.Builder(action=[['$PYTHON', '$PREPROCESS_PY', '$SOURCE', '$TARGET']])

TeXMLaddMarkers = SCons.Builder.Builder(action=[['$PYTHON', '$TEXML_RTL_MARKERS_PY', '--rtl', '$SOURCE', '$TARGET']])

XMLtoTeXML = ConsodocII.XMLtoTeXML

TeXMLtoTeX = ConsodocII.TeXMLtoTeX

GeneratePatchFile = ConsodocII.GeneratePatchFile

ApplyPatch = ConsodocII.ApplyPatch

TeXtoPDF = ConsodocII.TeXtoPDF

OutlinesToPDF = SCons.Builder.Builder(action=[['$JAVA', '-cp', '$ITEXT:$SUPPORT/java', 'XML2Bookmarks', '$OUTLINES_FILE', '$SOURCE', '$TARGET']])

#
# Setting up environment
#

# Import('set_paths_to_fonts') # Already imported, in "multifont"

def calc_images_dirs(first_dir, include_path):
  image_dirs = []
  if first_dir is not None:
    if isinstance(first_dir, types.StringTypes):
      image_dirs.append(first_dir)
    else:
      for d in first_dir:
        image_dirs.append(d)
  for inc_dir in include_path:
    im_inc_dir = os.path.normpath(os.path.join(inc_dir, '..', 'images', 'pdf'))
    if os.path.isdir(im_inc_dir):
      image_dirs.append(im_inc_dir)
  return image_dirs

#
# To PDF
#
def bitplant_process(in_file, *ls, **kw):
  orig_in_file = in_file
  basename = os.path.basename(in_file)
  basename = os.path.splitext(basename)[0]
  basename = re.sub('[^A-Za-z0-9]', '_', basename)
  in_file  = os.path.join(os.path.dirname(in_file), basename)
  outlines_file   = os.path.join('tmp', basename + '.outlines')
  indexterms_file = os.path.join('tmp', basename + '_idxterms.xml')
  tex_file        = os.path.join('tmp', basename + '.tex')
  patch_file      = os.path.splitext(in_file)[0] + '.patch'
  #
  # Setup environment
  #
  images_dirs = calc_images_dirs(kw.get('imgdir',None), include_path)
  env_va = get_default_vars()
  for k,v in kw.iteritems():
    env_va[k] = v
  env_va['XSLTPROC_PARAMS'].extend(['--path', os.pathsep.join(include_path)])
  env_va['TEX_INCLUDE_DIRS'] = include_path
  env_va['TEX_IMAGES_DIRS']  = images_dirs
  env = Environment(**env_va)
  set_paths_to_fonts(env, include_path)
  env['ENV']['BITPLANT_LATEX'] = support_dir
  path_parts = os.environ['PATH'].split(os.pathsep)
  path_parts.reverse()
  for path_part in path_parts:
    ep = env['ENV']['PATH']
    if path_part not in ep:
      env['ENV']['PATH'] = path_part + os.pathsep + ep
  #
  # Fix environment
  #
  if '0.' == SCons.__version__[:2]:
    print '*** old SCons version detected, activating compatibility layer'
    old_depends = env.Depends
    def new_depends(target, deps):
      if isinstance(target, SCons.Node.NodeList):
        for t in target:
          old_depends(t, deps)
      else:
        old_depends(target, deps)
    env.Depends = new_depends
    def compat096(node):
      assert 1 == len(node)
      return node[0]
  else:
    def compat096(node):
      return node
  #
  # Reverse patch
  #
  if 'patch' in COMMAND_LINE_TARGETS:
    node = GeneratePatchFile(env, patch_file, tex_file)
    Alias('patch', node)
    return
  #
  # Preprocess
  #
  node = PreprocessXML(env, 'tmp/%s.xml' % basename, orig_in_file)
  Clean(compat096(node), 'tmp')
  py_files = glob.glob(os.path.join(support_dir, '*.py'))
  env.Depends(node, py_files)
  #
  # TeXML
  #
  texml_file    = os.path.join('tmp', basename + '.texml')
  texml_node = XMLtoTeXML(env, texml_file, compat096(node))
  tp = env.get('TEXML_PARAMS', {})
  tp['outlines_file']            = os.path.basename(outlines_file)
  tp['indexterms_file_basename'] = os.path.splitext(os.path.basename(indexterms_file))[0]
  if ARGUMENTS.get('dev', 0) == '1':
    tp['dev'] = 1
  env['TEXML_PARAMS'] = tp
  env.Alias('xsl_depends', glob.glob(os.path.join(support_dir, '*.xsl')))
  env.Depends(texml_node, Alias('xsl_depends'))
  cfg_file = env.File('configuration.xml')
  if cfg_file.exists():
    env.Depends(node, cfg_file)
  env.SideEffect(outlines_file, compat096(texml_node))
  #
  # Maybe LTR markers in RTL text
  #
  do_markers = cfg_file.exists()
  if do_markers:
    h = open(cfg_file.get_abspath())
    s = h.read()
    h.close()
    m = re.search('''id\s*=\s*['"]language['"][^<]+<value>(\w\w)<''', s)
    if m:
      language = m.group(1)
    else:
      do_markers = 0
  if do_markers:
    lang_xml = os.path.join(support_dir, 'lang.xml')
    if not os.path.exists(lang_xml):
      do_markers = 0
    else:
      h = open(lang_xml)
      s = h.read()
      h.close()
      m = re.search('''<string\s+id=\s*['"]font-profile['"]''', s)
      if not m:
        do_markers = 0
      else:
        i = m.end()
        re_fp=re.compile('''<lang\s+id=\s*['"]%s['"]\s*>([^<]+)<''' % language)
        m = re_fp.search(s, i)
        if not m:
          do_markers = 0
        else:
          do_markers = 'FontProfileArabian' == str(m.group(1))
  if do_markers:
    node = TeXMLaddMarkers(env, 'tmp/%s.rllr.texml' % basename, compat096(texml_node))
    texml_node = node
  #
  # TeXML to TeX
  #
  node = TeXMLtoTeX(env, 'tmp/%s.tex.orig' % basename, compat096(texml_node))
  #
  # Patch
  #
  if os.path.exists(patch_file):
    node = ApplyPatch(env, tex_file, compat096(node), PATCH_FILE=patch_file)
  else:
    node = env.Command(tex_file, compat096(node), Copy('$TARGET', '$SOURCE'))
  #
  # TeX to PDF
  #
  tmppdf_file = 'tmp/%s.pdf' % basename
  node = TeXtoPDF(env, tmppdf_file, compat096(node))
  env['TEX_COMMAND_PARAMS'].extend(['--src', '--output-driver=xdvipdfmx'])
  #
  # Outlines / final PDF
  #
  node = OutlinesToPDF(env, os.path.join('out', basename + '.pdf'), compat096(node), OUTLINES_FILE=env.File(outlines_file))
  sty_files = glob.glob(os.path.join(support_dir, '*.sty'))
  sty_node  = env.Alias('sty_depends', sty_files)
  env.Depends(node, sty_node)
  env.Alias('pdf', compat096(node))
  Clean(compat096(node), 'out')
  #
  # Optionally: re-scale PDF
  # Should be executed after inserting outlines, otherwise IDs are lost
  #
  dpi = kw.get('dpi', 1200)
  if (0 != dpi) and ('darwin' == sys.platform) and 0: # FIXME
    AddPostAction(compat096(node), action=[
      Move('${TARGET}.rescale', '$TARGET'),
      ['$PYTHON', os.path.join(support_dir, 'rescale-pdf.py'), dpi, '${TARGET}.rescale', '$TARGET'],
      Delete('${TARGET}.rescale')
    ])
  #
  # Subtask: index
  #
  h_infile = open(orig_in_file)
  index_required = '<IndexAnnex' in h_infile.read()
  h_infile.close()
  if index_required:
    env.SideEffect(indexterms_file, texml_file)
    index_xml = os.path.join('tmp', basename + '_idx.xml')
    index_py  = os.path.join(support_dir, 'make_index.py')
    env.Command(index_xml, indexterms_file, action=[['$PYTHON', index_py, '$SOURCE', '$TARGET']])
    env.Depends(index_xml, index_py)
    index_texml = os.path.join('tmp', basename + '_idx.texml')
    index_xslt  = os.path.join(support_dir, 'convidx.xsl')
    env.Command(index_texml, index_xml, action=[['$XSLTPROC', '$XSLTPROC_PARAMS', '-o', '$TARGET', index_xslt, '$SOURCE']])
    env.Depends(index_texml, index_xslt)
    index_tex   = os.path.join('tmp', basename + '_idx.tex')
    env.Command(index_tex, index_texml, action=[['$TEXML_TOOL', '$TEXML_TOOL_PARAMS', '$SOURCE', '$TARGET']])
    env.Depends(tmppdf_file, index_tex)
  return env

Export('bitplant_process')

import os
this_sconscript_file = (lambda x:x).func_code.co_filename
code_base   = os.path.dirname(this_sconscript_file)
support_dir = os.path.join(code_base, 'support')

if ARGUMENTS.get('dev', 0) == '1':
  Import('include_path')
  include_path.append(support_dir)

Alias('sty_depends', glob.glob(os.path.join('support', '*.sty')))
Alias('xsl_depends', glob.glob(os.path.join('support', '*.xsl')))

Import('bitplant_process')
def stbitplant_process(in_file, *ls, **kw):
  if not kw.has_key('TEXML_XSLT'):
    kw['TEXML_XSLT'] = os.path.join(support_dir, 'bitplant_st.xsl')
  bitplant_process(in_file, *ls, **kw)
Export('stbitplant_process')
