PRO setup_links_nucalcpi

;;infile = 'filtered_seqids.sav'
;;restore, infile

base = '~/fltops'

outdir = 'full_mission'

file_mkdir, outdir

socn = file_search(base+'/*/*', /test_directory)
soc_seqid = file_basename(socn)

FOR i = 0, n_elements(socn) - 1 DO BEGIN
   IF strmid(soc_seqid[i], 0, 1) EQ '0' OR $
      strmid(soc_seqid[i], 0, 1) EQ '2' OR $
      strmid(soc_seqid[i], 0, 1) EQ '1' THEN BEGIN
      print, 'Skipping '+soc_seqid[i]
      CONTINUE
   ENDIF
   
   IF stregex(soc_seqid[i], 'old', /boolean) OR $
      stregex(soc_seqid[i], 'bad', /boolean) OR $
      stregex(soc_seqid[i], 'backup', /boolean) OR $
      stregex(soc_seqid[i], 'fail', /boolean) OR $
      stregex(soc_seqid[i], 'orig', /boolean) OR $
      stregex(soc_seqid[i], 'pre', /boolean) THEN BEGIN
      print, 'Skipping '+soc_seqid[i]
      CONTINUE
   ENDIF

   

   datpath = socn[i]
   

   seqid = file_basename(datpath)
   f = file_test(datpath+'/event_cl/nu'+seqid+'A02_cl.evt')
   IF ~f THEN BEGIN
      print, 'No 02 file for: ', datpath
      continue
   ENDIF


   file_mkdir, outdir+'/'+seqid
   f = file_test(outdir+'/'+seqid+'/'+seqid)
   IF ~f THEN BEGIN
      spawn, 'ln -s '+datpath+' '+outdir+'/'+seqid+'/'+seqid
   ENDIF

   
  
ENDFOR



END
