PRO run_extract_events

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
   
   print, 'Loading ', datpath

   ;; Make the temporary softlink:
   seqid = file_basename(datpath)

   file_mkdir, outdir+'/'+seqid
   f = file_test(outdir+'/'+seqid+'/'+seqid)
   IF ~f THEN $ 
      spawn, 'ln -s '+datpath+' '+outdir+'/'+seqid+'/'+seqid


   f = file_test(outdir+'/'+seqid+'/nu'+seqid+'A02_cl.evt')
   IF ~f THEN BEGIN
      continue
;      spawn, './run_nucalcpi.sh '+seqid
   ENDIF
   


 
   
   ; Extract the events
   extract_events, seqid



   
                                ; Cleanup files
;   spawn, 'rm '+outdir+'/'+seqid+'/nu*uf.evt'

  
ENDFOR



END
