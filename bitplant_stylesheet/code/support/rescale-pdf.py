import sys, os
from Foundation import *
from Quartz import *

(dpi, in_file, out_file) = sys.argv[1:]
dpi = int(dpi)

filter_file = os.path.join(os.path.dirname(sys.argv[0]), 'DynSizeReduce.qfilter')
rf = NSMutableDictionary.dictionaryWithContentsOfFile_(filter_file)
o = rf
for step in ('FilterData', 'ColorSettings', 'ImageSettings', 'ImageScaleSettings'):
  o = o.objectForKey_(step)
o.setObject_forKey_(dpi, 'ImageResolution')


pdf_url = NSURL.fileURLWithPath_(in_file)
pdf_doc = PDFDocument.alloc().initWithURL_(pdf_url)

#furl = NSURL.fileURLWithPath_("/System/Library/Filters/Blue Tone.qfilter")
#fobj = QuartzFilter.quartzFilterWithURL_(furl)
fobj = QuartzFilter.quartzFilterWithProperties_(rf)
fdict = { 'QuartzFilter': fobj }
pdf_doc.writeToFile_withOptions_(out_file, fdict)

