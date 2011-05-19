import unittest
import xml.dom.minidom
import cals

class CalsTestCase(unittest.TestCase):

  def test_no_span(self):
    self.use_file('html', 'tests/test010.xml')

  def test_phantom_cell(self):
    self.use_file('html', 'tests/test020.xml')

  def test_horiz_span(self):
    self.use_file('html', 'tests/test030.xml')

  def test_vert_span(self):
    self.use_file('html', 'tests/test040.xml')

  def test_complex_span(self):
    self.use_file('html', 'tests/test050.xml')

  def test_cals(self):
    self.use_file('cals', 'tests/test060.xml')

  #
  #
  #
  def use_file(self, html_or_cals, fname):
    cals.reset_id_generator()
    #
    # Load the file, get the input and expected tables
    #
    doc = xml.dom.minidom.parse(fname)
    if 'html' == html_or_cals:
      res = doc.getElementsByTagName('table')
    else:
      res = doc.getElementsByTagName('tgroup')
    assert(len(res) == 2)
    tbl_in  = res[0]
    tbl_out = res[1]
    #
    # Process the table and compare with the expected result
    #
    if 'html' == html_or_cals:
      tblo = cals.html_table(doc, tbl_in)
    else:
      tblo = cals.cals_table(doc, tbl_in)
    tblo.split()
    s1 = tbl_in.toxml()
    s2 = tbl_out.toxml()
    s1 = s1.replace(' ', '').replace("\n", '').replace('>', "\n>")
    s2 = s2.replace(' ', '').replace("\n", '').replace('>', "\n>")
    if s1 != s2:
      h = open('f1.xml', 'w')
      h.write(s1)
      h.close()
      h = open('f2.xml', 'w')
      h.write(s2)
      h.close()
    self.assertEqual(s1, s2)
    #
    # Cleanup
    #
    doc.unlink()
    doc = None

if __name__ == '__main__':
  unittest.main()
