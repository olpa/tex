#
# Parse TeX log and display the boxes as a tree
# Usage: python viewboxes.py [-pt] <log_file_name>
# Requires wxPython
#
import wx, sys, re

re_isboxdef  = re.compile('^> \\\\box\d+=[\r\n]*$')
re_isboxdef2 = re.compile('^Completed box being shipped out \[\\d+\]$')

pt_to_mm = 1

re_find_pt = re.compile('(\d+\\.\d+)([^0-9f])')
pt_to_mm_coeff = 25.4/72.27  # 1in=72.27pt, 25.4mm=1in -> 72.27pt=25.4mm
def convert_pt_to_mm(s):
  def pt_to_mm(match):
    s_pt = match.group(1)
    if '0.0' == s_pt:
      return match.group(0)
    n_pt = float(s_pt)
    n_mm = n_pt * pt_to_mm_coeff
    s_mm = '%.5rmm' % n_mm
    return s_mm + match.group(2)
  s = s + ' ' # workaround: can't write 'end of line' in a RE alternative
  s = re_find_pt.sub(pt_to_mm, s)
  s = s[:-1]
  return s

class ViewFrame(wx.Frame):

  def __init__(self):
    wx.Frame.__init__(self, None, title="Tree of boxes", size=(600, 800))
    self.tree = wx.TreeCtrl(self)
    self.popup_menu = wx.Menu()
    menu_item = self.popup_menu.Append(-1, "Reload")
    self.Bind(wx.EVT_MENU, self.OnReload, menu_item)
    self.tree.Bind(wx.EVT_CONTEXT_MENU, self.OnShowPopup)

  def OnShowPopup(self, evt):
    pos = evt.GetPosition()
    pos = self.tree.ScreenToClient(pos)
    self.tree.PopupMenu(self.popup_menu, pos)

  def OnReload(self, evt):
    self.load_tree_from_file(self.fname)

  def load_tree_from_file(self, fname):
    self.fname = fname
    self.tree.DeleteAllItems()
    root_id = self.tree.AddRoot(fname)
    self.tree.Expand(root_id)
    top_level_items = [root_id]
    h = open(fname)
    box_line  = ''
    lineno     = 0
    is_in_box  = 0
    for line in h:
      lineno = lineno + 1
      # Detect is a box is started
      if re_isboxdef.match(line) or re_isboxdef2.match(line):
        box_line   = '(line %d) %s' % (lineno, line.strip())
        is_in_box  = 1
        open_items = [root_id]
        id         = None
        last_line  = None
        overfull   = 0
        continue
      # Skip non-box lines
      if not is_in_box:
        continue
      line         = line.rstrip("\r\n")
      was_overfull = overfull
      overfull     = 79 == len(line)
      if pt_to_mm:
        line = convert_pt_to_mm(line)
      # Special case: the previous box line continues
      if was_overfull:
        line = last_line + line[1:]
        try:
          self.tree.SetItemText(id, line)
        except UnicodeDecodeError: # XeTeX utf-8 input is broken
          line = unicode(line, 'utf-8', 'replace')
          self.tree.SetItemText(id, repr(line))
        last_line = line
        continue
      # Check if the box is finished
      if not len(line):
        is_in_box = 0
        continue
      # Extract text and nesting level
      new_item_level = 1
      while len(line) > 0:
        if '.' == line[0]:
          new_item_level = new_item_level + 1
          line = line[1:]
        else:
          break
      if 1 == new_item_level:
        line = box_line + '  ' + line
      last_line = line
      # Find the parent
      if new_item_level < len(open_items):
        while new_item_level < len(open_items):
          open_items.pop()
      # Append to the tree
      id = self.tree.AppendItem(open_items[-1], line)
      open_items.append(id)
      if 1 == new_item_level:
        top_level_items.append(id)
    h.close()
    # Expand the top-level items
    for id in top_level_items:
      self.tree.Expand(id)
      self.tree.SetItemBold(id, 1)

args = sys.argv[1:]
if not len(args):
  print "Usage: viewboxes.py [-pt] tex_lof_file.log"
  sys.exit(0)
if '-pt' == args[0]:
  pt_to_mm = 0
  args = args[1:]
fname = args[0]
app = wx.PySimpleApp()
frame = ViewFrame()
frame.load_tree_from_file(fname)
frame.Show()
app.MainLoop()
