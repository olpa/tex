# Index preprocessing
import locale, sys

#
# Entry hash
# 'elem'             XML element
# 'first_word'       The primary index
# 'second_word'      The secondary index
# 'letter'           The first letter
# 'xfrm_letter', 'xfrm_first_word', 'xfrm_second_word' -- strxfrm versions
# 'sort_pos_letter', 'sort_pos_first_word', 'sort_pos_second_word'  position in sorted
#
class word_rec:
  def __init__(self, elem, first_word, second_word):
    self.elem                 = elem
    self.first_word           = first_word
    self.second_word          = second_word
    self.letter               = None
    self.xfrm_letter          = None
    self.xfrm_first_word      = None
    self.xfrm_second_word     = None
    self.sort_pos_letter      = None
    self.sort_pos_first_word  = None
    self.sort_pos_second_word = None
  def __str__(self):
    return '%s:%s (%s): %d-%d-%d' % (self.first_word, self.second_word, self.letter, self.sort_pos_letter, self.sort_pos_first_word, self.sort_pos_second_word)
  def __repr__(self):
    return self.__str__()

#
# Input: array. output: array of arrays, each subarray contains
# equivalent items.
#
def group_by(arr, eq_func):
  if not len(arr):
    return arr
  new_arr  = []
  old_item = arr[0]
  eq_arr   = [old_item]
  for cur_item in arr[1:]:
    if not eq_func(old_item, cur_item):
      new_arr.append(eq_arr)
      old_item = cur_item
      eq_arr   = []
    eq_arr.append(cur_item)
  new_arr.append(eq_arr)
  return new_arr

#
# Preprocessing: extract letters, set xforms
#
def preprocess_words(words, use_locale):
  try:
    old_locale = locale.setlocale(locale.LC_COLLATE, use_locale)
  except:
    print >>sys.stderr, "Can't set locale '%s'" % use_locale
    old_locale = None
  for word in words:
    s_word = word.first_word
    if not len(s_word):
      letter = '*'
    else:
      letter = s_word[0]
    if not letter.isalpha():
      letter = '*'
    else:
      letter = letter.upper()
    word.letter           = letter
    word.xfrm_letter      = locale.strxfrm(letter.encode('UTF-8'))
    word.xfrm_first_word  = locale.strxfrm(word.first_word.upper().encode('UTF-8'))
    word.xfrm_second_word = locale.strxfrm(word.second_word.upper().encode('UTF-8'))
  if old_locale != None:
    locale.setlocale(locale.LC_COLLATE, old_locale)

#
# Initial grouping
#
def group_words_by_the_letter(words):
  #
  # Sort
  #
  words.sort(
      cmp = lambda o1, o2: cmp(o1.xfrm_letter, o2.xfrm_letter))
  words = group_by(words,
      eq_func = lambda o1, o2: o1.xfrm_letter == o2.xfrm_letter)
  #
  # Postprocess: positions
  #
  i = 0
  for eq_group in words:
    i = i + 1
    for word in eq_group:
      word.sort_pos_letter = i
  return words

#
# First-level grouping
#
def group_words_by_the_first_word(words):
  i = 0
  new_words = []
  for eq_letter_arr in words:
    eq_letter_arr.sort(
        cmp = lambda w1, w2: cmp(w1.xfrm_first_word, w2.xfrm_first_word))
    sorted_joined_arr = group_by(eq_letter_arr,
        lambda w1, w2: w1.xfrm_first_word == w2.xfrm_first_word)
    for eq_first_word_arr in sorted_joined_arr:
      i = i + 1
      for word in eq_first_word_arr:
        word.sort_pos_first_word = i
    new_words.append(sorted_joined_arr)
  return new_words

#
# Second-level grouping
#
def group_words_by_the_second_word(words):
  i = 0
  new_words = []
  for eq_letter_arr in words:
    new_eq_first = []
    for eq_first_word_arr in eq_letter_arr:
      eq_first_word_arr.sort(
          cmp = lambda w1, w2: cmp(w1.xfrm_second_word, w2.xfrm_second_word))
      sorted_joined_arr = group_by(eq_first_word_arr,
          lambda w1, w2: w1.xfrm_second_word == w2.xfrm_second_word)
      for eq_second_word_arr in sorted_joined_arr:
        i = i + 1
        for word in eq_second_word_arr:
          word.sort_pos_second_word = i
      new_eq_first.append(sorted_joined_arr)
    new_words.append(new_eq_first)
  return new_words

#
# Test
#
if '__main__' == __name__:
  words = []
  h = open('words.txt')
  for s in h:
    s = s.strip()
    word = word_rec(None, first_word=s[:2], second_word=s[2:])
    words.append(word)
  h.close()
  preprocess_words(words, ('en', 'UTF-8'))
  words = group_words_by_the_letter(words)
  words = group_words_by_the_first_word(words)
  words = group_words_by_the_second_word(words)
  print words
