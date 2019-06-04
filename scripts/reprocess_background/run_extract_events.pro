PRO run_extract_events


base = './full_mission'

socn = file_search(base+'/*', /test_directory)

FOR i = 0, n_elements(socn) - 1 DO BEGIN
   seqid = file_basename(socn[i])

   f = file_test(socn[i]+'/nu'+seqid+'A02_cl.evt')
   IF ~f THEN BEGIN
      print, 'run_extract_events missing 02 file: '+seqid
      continue
;      spawn, './run_nucalcpi.sh '+seqid
   ENDIF
   



 
   ; Extract the events
   extract_events, seqid

  
ENDFOR



END
