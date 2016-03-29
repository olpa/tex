#
# Preprocess tables, split spanned cells
# Usage:
#
# import cals
# ...
# doc        = xml.dom.....parse.....
# table_node = ... # "tgroup" element for cals or "table" for html
# tblo = cals.cals_table(doc, table_node) # or cals.html_table
# ...
# tblo.split()
#

import xml.dom
cals_ns = 'table:conversion:helper'

#
# Helper: generating new span IDs
#
cals_helper_unused_number = 1
def cals_generate_new_span_id():
  global cals_helper_unused_number
  s = 'tch%i' % cals_helper_unused_number
  cals_helper_unused_number = cals_helper_unused_number + 1
  return s
def reset_id_generator():
  global cals_helper_unused_number
  cals_helper_unused_number = 1

#
# DOM helpers
#
def dom_till_element(node):
  while node:
    if xml.dom.Node.ELEMENT_NODE == node.nodeType:
      return node
    node = node.nextSibling
  return node

def dom_first_elem_child(node):
  return dom_till_element(node.firstChild)

def dom_next_elem_sibling(node):
  return dom_till_element(node.nextSibling)

# =========================================================
# Unified interface to tables. Setters-getters.
#
class some_table:
  def __init__(self, doc, table_node):
    self.doc        = doc
    self.table_node = table_node

  #
  # Add a cell
  #
  def add_cell(self, row_node, right_sibling, name, span_id):
    node = self.doc.createElementNS(cals_ns, name)
    if span_id:
      node.setAttributeNS(cals_ns, 'tch:span', span_id)
    row_node.insertBefore(node, right_sibling)
    return node

  #
  # Create a fake cell
  #
  def fake_cell(self, row_node, right_sibling, span_id):
    return self.add_cell(row_node, right_sibling, 'tch:fakecell', span_id)

  #
  # Creating a missed cell
  #
  def phantom_cell(self, row_node, right_sibling):
    raise RuntimeError('the method "phantom_cell" should be defined in a child class')

  #
  # Number of rows and columns spanned
  #
  def get_rowspan(self, cur_cell):
    raise RuntimeError('the method "get_rowspan" should be defined in a child class')

  def get_colspan(self, cur_cell):
    raise RuntimeError('the method "get_colspan" should be defined in a child class')

  #
  # Split the cells.
  #
  def split(self):
    process_table_block(self, self.table_node)

# ---
# HTML-style tables
#
class html_table(some_table):

  #
  # Creating a missed cell
  #
  def phantom_cell(self, row_node, right_sibling):
    self.add_cell(row_node, right_sibling, 'td', None)

  #
  # Number of rows and columns spanned
  #
  def get_rowspan(self, cur_cell):
    try:
      return int(cur_cell.getAttribute('rowspan'))
    except TypeError:
      return 1
    except ValueError:
      return 1

  def get_colspan(self, cur_cell):
    try:
      return int(cur_cell.getAttribute('colspan'))
    except TypeError:
      return 1
    except ValueError:
      return 1

# ---
# CALS-style tables
#
class cals_table(some_table):

  #
  # Creating a missed cell
  #
  def phantom_cell(self, row_node, right_sibling):
    self.add_cell(row_node, right_sibling, 'entry', None)

  #
  # Number of rows and columns spanned
  #
  def get_rowspan(self, cur_cell):
    try:
      return int(cur_cell.getAttribute('morerows')) + 1
    except TypeError:
      return 1
    except ValueError:
      return 1

  def get_colspan(self, cur_cell):
    try:
      return self.colspec[cur_cell.getAttribute('nameend')] - self.colspec[cur_cell.getAttribute('namest')] + 1
    except KeyError:
      return 1

  #
  # CALS-version of the entry point. Table consist of three parts
  # (header, body, footer). Process each of them.
  #
  def split(self):
    self.colspec = {}
    col_n = 0
    node = dom_first_elem_child(self.table_node)
    while node:
      if 'colspec' == node.tagName:
        col_n = col_n + 1
        self.update_colspec(node, col_n)
      else:
        process_table_block(self, node)
      node = dom_next_elem_sibling(node)

  def update_colspec(self, node, default_col_n):
    colname = node.getAttribute('colname')
    colnum  = node.getAttribute('colnum')
    try:
      col_n = int(colnum)
    except ValueError:
      col_n = default_col_n
    self.colspec[colname] = col_n

# =========================================================

#
# A direct approach is two-step:
# - first, expland column spanning
# - second, expand row spanning
# Thanks to span_track, we can perform the two steps at the same time:
# while doing the step one, we collect the data for the step two.
# span_track is a list of annotations for each column in a row.
# If a cell does not participate in a row spanning, the value is "0".
# Otherwise, the annotation is a tuple (id, n, is_left, is_right), where
# - id is a unique identifier of the spanning group,
# - n is how much rows left for spanning,
# - is_left if it is the left column,
# - is_right if it is the right column
#

def process_table_block(tblo, table_node):
  # Let the namespace declaration be only at the root element
  # I have no idea if I create it correctly
  tblo.doc.documentElement.setAttribute('xmlns:tch', cals_ns)
  span_track = []
  row_node = dom_first_elem_child(table_node)
  while row_node:
    span_track = process_row(row_node, span_track, tblo)
    row_node = dom_next_elem_sibling(row_node)

def process_row(row_node, span_track, tblo):
  new_span_track = []
  is_left  = 0
  is_right = 0
  is_top   = 0
  rowspan  = 0
  cur_cell = None
  #
  # Helper to update the span control list
  #
  def add_to_span_control(span_id, rowspan):
    if rowspan:
      new_span_track.append((span_id, rowspan, is_left, is_right))
    else:
      new_span_track.append(0)
  #
  # Helpers to set attributes
  #
  def set_location(elem):
    if is_left:
      elem.setAttributeNS(cals_ns, 'tch:left', '1')
    if is_right:
      elem.setAttributeNS(cals_ns, 'tch:right', '1')
    if is_top:
      elem.setAttributeNS(cals_ns, 'tch:top', '1')
    if rowspan == 1:
      elem.setAttributeNS(cals_ns, 'tch:bottom', '1')
  #
  # The main loop
  #
  cur_cell = dom_first_elem_child(row_node)
  while span_track or cur_cell:
    #
    # Lookup the control list for spanning marker
    #
    span_marker = 0
    if span_track:
      span_marker = span_track.pop(0)
    #
    # Some other spanned cell continued
    #
    if span_marker:
      (span_id, rowspan, is_left, is_right) = span_marker
      if is_top:
        is_top = is_top - 1
      fake_cell = tblo.fake_cell(row_node, cur_cell, span_id)
      set_location(fake_cell)
      add_to_span_control(span_id, rowspan-1)
      continue                                             # continue
    #
    # Bad table: number of cell less than in the previous row
    #
    if not cur_cell:
      tblo.phantom_cell(row_node, cur_cell)
      continue                                             # continue
    #
    # Get spanning status of the current cell
    #
    rowspan = tblo.get_rowspan(cur_cell)
    colspan = tblo.get_colspan(cur_cell)
    if (1 == rowspan) and (1 == colspan):
      span_id = 0
    else:
      is_left  = 1
      is_right = 1 == colspan
      is_top   = colspan # countdown true
      span_id = cals_generate_new_span_id()
      cur_cell.setAttributeNS(cals_ns, 'tch:span', span_id)
      set_location(cur_cell)
    #
    # Update the span control for the next row
    #
    add_to_span_control(span_id, rowspan-1)
    #
    # Column spanning? Update the _current_ span control list
    #
    i = 0
    while i < colspan - 1: # current column is already processed
      entry = (span_id, rowspan, 0, i == colspan - 2)
      if len(span_track) < i + 1:
        span_track.append(entry)
      else:
        span_track[i] = entry
      i = i + 1
    #
    # Go to the next node
    #
    cur_cell = dom_next_elem_sibling(cur_cell)
    continue                                               # continue
  #
  # Return the new span control list
  #
  return new_span_track
