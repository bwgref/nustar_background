PRO run_nucalcpi

base = './full_mission'

socn = file_search(base+'/*', /test_directory)
soc_seqid = file_basename(socn)

FOR i = 0, n_elements(socn) - 1 DO BEGIN

   seqid = file_basename(socn[i])
   
   ; Check to see if you need to run nupipeine:
   cl_test = socn[i]+'/nu'+seqid+'A02_cl.evt'
   f = file_test(cl_test)
   IF f THEN BEGIN
;      print, 'File exists '+cl_test
      CONTINUE
   ENDIF

   log_test = socn[i]+'/nu'+seqid+'.log'
   
   
   print, seqid

   print, 'Running: '+seqid
   spawn, './run_nucalcpi.sh '+seqid
ENDFOR



END
