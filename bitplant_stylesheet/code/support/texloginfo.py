#!/usr/bin/python
"""Filter TeX log file for error ("--errors") or warning
("--warnings") messages, missed images ("--missed"),
or check if re-run is required ("--rerun").

Return codes:
0           no need for re-run
1           re-run is required (set only if "--rerun" is given)
not 0 or 1  some error

Author:  Oleg Parashchenko <olpa uucode com>
Home page: http://consodoc.com/texloginfo/
License: public domain"""
usage = __doc__

import re
import StringIO

#
# Re-usable class to parse LaTeX log
#
class texloginfo:

  #
  # Expected output streams are 'sys.stderr' or None
  #
  def __init__(self, warn_stream = None, err_stream = None, miss_stream = None):
    self.need_rerun  = 0
    if None == warn_stream: self.warn_stream = StringIO.StringIO()
    else:                   self.warn_stream = warn_stream
    if None == err_stream:  self.err_stream  = StringIO.StringIO()
    else:                   self.err_stream  = err_stream
    if None == miss_stream: self.miss_stream = StringIO.StringIO()
    else:                   self.miss_stream = miss_stream
    self.missed_seen = []
    
  #
  # Process TeX log data in the input stream
  #
  def parse_log_stream(self, in_stream):
    re_warning = re.compile('(at lines \\d+\\-\\-\\d+|at line \\d+)$')
    re_missed  = re.compile('''^! LaTeX (Error|warning): File `([^']+)' not found.$''')
    #
    # Loop over the file strings
    #
    for l in in_stream:
      #
      # Check for missed image
      #
      if None != self.miss_stream:
        matched = re_missed.match(l)
        if matched:
          file = matched.group(2)
          if not file in self.missed_seen:
            self.missed_seen.append(file)
            print >>self.miss_stream, file
      #
      # Check if the line is a warning message
      #
      if None != self.warn_stream:
        if re_warning.search(l):
          print >>self.warn_stream, l,
      #
      # Check if re-run is expected
      #
      if (-1 != l.find('Rerun to')) and (-1 != l.find('LaTeX Warning')):
        self.need_rerun = 1
        if None != self.warn_stream:
          print >>self.warn_stream, l,
      #
      # Check if the line is an error message
      #
      if (len(l) > 1) and ('!' == l[0]) and (' ' == l[1]):
        # Actually, it might be a warning:
        # ! pdfTeX warning (ext4): destination with the same identifier...
        if -1 != l.find('warning'):
          if None != self.warn_stream:
            print >>self.warn_stream, l,
        else:
          # Print the error
          if None != self.err_stream:
            print >>self.err_stream, l,
  #
  # Process TeX log file. If file doesn't exist, we consider that
  # there are no errors and warnings, and no re-run required.
  #
  def parse_log_file(self, file_name):
    try:
      in_stream = file(file_name)
    except IOError:
      return
    self.parse_log_stream(in_stream)
    in_stream.close()

  #
  # Return collected data. Close the in-memory streams.
  #
  def get_warnings(self):
    s = self.warn_stream.getvalue()
    self.warn_stream.close()
    self.warn_stream = None
    return s

  def get_errors(self):
    s = self.err_stream.getvalue()
    self.err_stream.close()
    self.err_stream = None
    return s

  def get_missed(self):
    s = self.miss_stream.getvalue()
    self.miss_stream.close()
    self.miss_stream = None
    return s

  def get_rerun(self):
    return self.need_rerun

#
# Command-line program starts here
#
if __name__ == '__main__':
  import sys
  import getopt

  #
  # Parse command line
  #
  opt_errors   = 0
  opt_warnings = 0
  opt_missed   = 0
  opt_rerun    = 0
  if len(sys.argv) < 3:
    print >>sys.stderr, usage
    sys.exit(2)
  try:
    opts, args = getopt.getopt(sys.argv[1:], 'hrewm', ['help', 'rerun', 'errors', 'warnings', 'missed'])
  except getopt.GetoptError, e:
    print >>sys.stderr, 'texml: Can\'t parse command line: %s' % e
    print >>sys.stderr, usage
    sys.exit(2)
  for o, a in opts:
    if o in ('-h', '--help'):
      print >>sys.stderr, usage;
      sys.exit(1)
    if o in ('-e', '--errors'):
      opt_errors = 1
    if o in ('-w', '--warnings'):
      opt_warnings = 1
    if o in ('-r', '--rerun'):
      opt_rerun = 1
    if o in ('-m', '--missed'):
      opt_missed = 1

  #
  # Get the file name
  #
  if 0 == len(args):
    opt_file = '-'
  elif 1 == len(args):
    opt_file = args[0]
  else:
    print >>sys.stderr, 'texloginfo: only one file name is expected'
    sys.exit(2)

  #
  # Parse log
  #
  exit_code  = 0
  if opt_warnings: warn_stream = sys.stderr
  else:            warn_stream = None
  if opt_errors:   err_stream  = sys.stderr
  else:            err_stream  = None
  if opt_missed:   miss_stream = sys.stderr
  else:            miss_stream = None
  tli = texloginfo(1, 1, 1) # Avoid construction of StringIO
  tli.warn_stream = warn_stream
  tli.err_stream  = err_stream
  tli.miss_stream = miss_stream
  if '-' == opt_file:
    tli.parse_log_stream(sys.stdin)
  else:
    tli.parse_log_file(opt_file)
  if opt_rerun:
    exit_code = tli.get_rerun()

  #
  # Finish the program
  #
  sys.exit(exit_code)
