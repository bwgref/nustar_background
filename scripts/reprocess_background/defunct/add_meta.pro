PRO add_meta

base = 'full_mission'

seqdir = file_search(base+'/*', /test_directory)


ab  = ['A', 'B']
FOR i = 0, n_elements(seqdir) -1 DO BEGIN
   print, seqdir[i]
   seqid = file_basename(seqdir[i])

   ; First, check to make sure the file exists:

   FOR iab = 0, 1 DO begin
      evtf = seqdir[i]+'/nu'+seqid+ab[iab]+'02_cl.evt'
      f = file_info(evtf)
      IF ~f.exists THEN CONTINUE
      print, evtf

      evt_null = mrdfits(evtf, 0, null_hdr, /silent)
      evt = mrdfits(evtf, 1,evt_hdr, /silent)


      struct_add_field, evt, 'limb_angle', fltarr(n_elements(evt))+45



      attorbf = base+'/'+seqid+'/'+seqid+'/event_cl/nu'+seqid+ab[iab]+'.attorb'
      f = file_info(attorbf)
      IF ~f.exists THEN stop

      

      attorb = mrdfits(attorbf, 1, /silent)
                                ; Interpolate the attorb values onto the event times:

      evt.limb_angle = interpol(attorb.elv, attorb.time, evt.time)

      mwrfits, evt_null, evtf, null_hdr, /create
      mwrfits, evt, evtf, evt_hdr


      ;; new_evt.sunshine = interpol(attorb.sunshine, attorb.time, evt.time)
      ;; new_evt.ram_angle = interpol(attorb.ram_angle, attorb.time, evt.time)
      ;; new_evt.geomag = interpol(attorb.cor_asca, attorb.time, evt.time)
      ;; new_evt.lon = interpol(attorb.sat_lon, attorb.time, evt.time)
      ;; new_evt.lat = interpol(attorb.sat_lat, attorb.time, evt.time)
      ;; new_evt.alt = interpol(attorb.sat_alt, attorb.time, evt.time)
      ;; new_evt.limb_angle = interpol(attorb.elv, attorb.time, evt.time)


   ENDFOR
   






   
ENDFOR






END


