import DD

PASS_NO_ERRORS     =   0b1
#FAIL_ARE_ERRORS    =  0b10
FAIL_MASTER_ERRORS = 0b100

class decider:
  def __init__(self, ok_is, fail_is):
    self.ok_is   = ok_is
    self.fail_is = fail_is
    self.master_errors = ''

  def get_master_errors(self):
    return self.master_errors

  def extract_master_errors(self, latex_run):
    if (FAIL_MASTER_ERRORS & self.fail_is):
      latex_run.run_latex()
      self.master_errors = latex_run.get_errors()
      assert self.master_errors, "File should give master errors, but compiled successfully"

  def get_result(self, latex_run):
    errors = latex_run.get_errors()
    if (PASS_NO_ERRORS & self.ok_is) and ('' == errors):
      return DD.DD.PASS
    #if (FAIL_ARE_ERRORS & self.fail_is) and ('' != errors):
    #  return DD.DD.FAIL
    if (FAIL_MASTER_ERRORS & self.fail_is) and (self.master_errors == errors):
      return DD.DD.FAIL
    return DD.DD.UNRESOLVED

  def sanity_check(self, dd_obj):
    def report():
      lf = dd_obj.get_last_run()
      print lf.get_errors()
      print ccode
    ccode = dd_obj.test_with_no_deltas()
    if DD.DD.PASS != ccode:
      report()
      assert DD.DD.PASS == ccode, "Run agains no-delta should give PASS"
    ccode = dd_obj.test_with_all_deltas()
    if DD.DD.FAIL != ccode:
      repor()
      assert DD.DD.FAIL == ccode, "Run agains full-delta should give FAIL"
