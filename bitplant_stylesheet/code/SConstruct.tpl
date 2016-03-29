sconscript = r'''...''' # Option SCONSCRIPT
SConscript(sconscript)
Import('stbitplant_process')

in_file  = r'''...''' # Option INFILE
imgdir   = r'''...''' # Option IMGDIR

stbitplant_process(
  in_file      = in_file,
  imgdir       = imgdir+'/pdf',
)
