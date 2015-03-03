import DD

class decider:
  def __init__(self):
    self.pass_errors = ''
    self.pass_extra  = ''
    self.fail_errors = ''
    self.fail_extra  = ''

  def extract_master_errors(self, dd_obj):
    ccode = dd_obj.test_with_no_deltas()
    lf = dd_obj.get_last_run()
    self.pass_errors = lf.get_errors()
    self.pass_extra  = lf.get_reference()
    ccode = dd_obj.test_with_all_deltas()
    lf = dd_obj.get_last_run()
    self.fail_errors = lf.get_errors()
    self.fail_extra  = lf.get_reference()

  def print_master_errors(self):
    print '[[[PASS error messages:[[[' + self.pass_errors + ']]]]]]'
    print '[[[PASS reference:[[[' + self.pass_extra + ']]]]]]'
    print '[[[FAIL error messages:[[[' + self.fail_errors + ']]]]]]'
    print '[[[FAIL reference:[[[' + self.fail_extra + ']]]]]]'

  def get_result(self, latex_run):
    errors = latex_run.get_errors()
    ref = latex_run.get_reference()
    if (errors == self.pass_errors) and (ref == self.pass_extra):
      return DD.DD.PASS
    if (errors == self.fail_errors) and (ref == self.fail_extra):
      return DD.DD.FAIL
    return DD.DD.UNRESOLVED
