PRO run_nupipe

;;infile = 'filtered_seqids.sav'
;;restore, infile

base = '~/fltops'

outdir = 'full_mission'

file_mkdir, outdir

socn = file_search(base+'/*/*', /test_directory)
soc_seqid = file_basename(socn)

FOR i = 0, n_elements(socn) - 1 DO BEGIN
;   print, i, ' of ', n_elements(socn) -1 
   ; Find the right socname:

;;   IF i LT 1201 THEN continue

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

   
;  this_one = where(soc_seqid EQ seqids[i], found)
;  IF ~found THEN stop


   datpath = socn[i]
  


   ;; Make the temporary softlink:
   seqid = file_basename(datpath)

   ;; file_mkdir, outdir+'/'+seqid
   ;; f = file_test(outdir+'/'+seqid+'/'+seqid)
   ;; IF ~f THEN BEGIN
   ;;    print, 'Setting up link: '+seqid
   ;;    spawn, 'ln -s '+datpath+' '+outdir+'/'+seqid+'/'+seqid
   ;; ENDIF
   
   ; Check to see if you need to run nupipeine:

   data_dir = outdir+'/'+seqid+'/'+seqid
   uf_test = data_dir+'/event_uf/nu'+seqid+'A_uf.evt'
   uf = file_test(uf_test)

   IF ~uf THEN begin
      print, 'Bad softlink?'
      print, uf_test
      CONTINUE

   ENDIF
   cl_test = outdir+'/'+seqid+'/nu'+seqid+'A02_cl.evt'

   f = file_test(cl_test)
   IF f THEN BEGIN
      print, 'File exists '+cl_test
      CONTINUE
   ENDIF

   log_test = outdir+'/'+seqid+'/nu'+seqid+'.log'
   logf = file_test(log_test)
   IF logf THEN BEGIN
      print, 'Log file exists '+log_test
      continue
   ENDIF
   


   

   print, 'Running: '+cl_test
   spawn, './run_nupipeline.sh '+seqid

ENDFOR



END
