import DD

class decider:
  def __init__(self):
    self.master_errors = ''
    self.reference     = ''

  def get_master_errors(self):
    return self.master_errors + self.reference

  def extract_master_errors(self, latex_run):
    latex_run.run_latex()
    self.master_errors = latex_run.get_errors()
    self.reference = latex_run.get_reference()
    assert self.master_errors or self.reference, "File should give master errors, but compiled successfully"

  def get_result(self, latex_run):
    errors = latex_run.get_errors()
    ref = latex_run.get_reference()
    # Empty must be PASS due to no-delta run
    if ('' == errors) and ('' == ref):
      return DD.DD.PASS
    # If digger is not used, then the log messages define the result
    if '' == self.reference:
      if errors == self.master_errors:
        return DD.DD.FAIL
      else:
        return DD.DD.UNRESOLVED
    # If digger is used, then the both are important
    if self.master_errors != errors:
      return DD.DD.UNRESOLVED
    if self.reference == ref:
      return DD.DD.FAIL
    return DD.DD.UNRESOLVED

  def sanity_check(self, dd_obj):
    def report():
      lf = dd_obj.get_last_run()
      print '[[[ last erros:', lf.get_errors(), ']]]'
      print ccode
    ccode = dd_obj.test_with_no_deltas()
    if DD.DD.PASS != ccode:
      report()
      assert DD.DD.PASS == ccode, "Run agains no-delta should give PASS"
    ccode = dd_obj.test_with_all_deltas()
    if DD.DD.FAIL != ccode:
      report()
      assert DD.DD.FAIL == ccode, "Run agains full-delta should give FAIL"
