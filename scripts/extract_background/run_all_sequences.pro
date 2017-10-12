PRO run_all_sequences

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

;   IF i LT 1000 THEN continue

   IF strmid(soc_seqid[i], 0, 1) EQ '0' OR $
      strmid(soc_seqid[i], 0, 1) EQ '2' OR $
      strmid(soc_seqid[i], 0, 1) EQ '1' THEN BEGIN
      print, 'Skipping '+soc_seqid[i]
      CONTINUE
   ENDIF
   
   IF stregex(soc_seqid[i], 'old', /boolean) OR $
      stregex(soc_seqid[i], 'bad', /boolean) THEN BEGIN
      print, 'Skipping '+soc_seqid[i]
      CONTINUE
   ENDIF

   
;  this_one = where(soc_seqid EQ seqids[i], found)
;  IF ~found THEN stop


   datpath = socn[i]
   
   print, 'Loading ', datpath
;   break
   extract_events, datpath, outdir = outdir, err = err


ENDFOR



END
