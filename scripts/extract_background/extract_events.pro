pro extract_events, socd, outdir = outdir, err = err

seqid = file_basename(socd)
datpath = socd+'/event_cl/'
ab = ['A', 'B']

record = {exp:fltarr(2), tstart:0.d, $
          date_obs:'', mjdref:0.d}


; Set the fields that you want to extract here:
ev_stub = {TIME:-999d, DET_ID:-1, PI:0., RAWX:-1, RAWY:-1, $
           DEPTHFLAG:0, GRADE:0, GEOMAG:-999., SUNSHINE:-1, $
           ram_angle:-999., lat:-999., lon:-999., alt:-999., $
           limb_angle:-999., SURRPI:0., TEMP:-10.}

; Depth cut flag for status cut below
depth_cut=128B

err = -1 

FOR iab = 0, 1 DO BEGIN

   evtfile = datpath+'nu'+seqid+ab[iab]+'_uf.evt'
   f = file_info(evtfile)
   IF ~f.exists THEN CONTINUE


   outfits = outdir+'/'+seqid+ab[iab]+'_02.fits'
   f = file_info(outfits)
   IF f.exists THEN BEGIN
      print, outfits+' exists, skipping'
      CONTINUE
   ENDIF


   err = 0

   print, 'Extracting: ', evtfile
   
   hkfile = datpath+'../hk/nu'+seqid+ab[iab]+'_fpm.hk'
   gtifile = datpath+'nu'+seqid+ab[iab]+'02_gti.fits'
   
   
   
   
   

   ; Get header information
   inhead = headfits(evtfile, exten='EVENTS')
   tstart = fxpar(inhead, 'TSTART')
   mjdref = fxpar(inhead, 'MJDREF')
   date_obs = fxpar(inhead, 'DATE-OBS')
   ra = fxpar(inhead, 'RA_OBJ')
   dec = fxpar(inhead, 'DEC_OBJ')
   exp = float(fxpar(inhead, 'EXPOSURE'))


    ; Load in unfiltered events
   ufevt = mrdfits(evtfile, 'EVENTS', /silent, /unsigned)


    ; Load in housekeeping data
    hkdata = mrdfits(hkfile, 'HK1FPM', /silent)
    hk4data = mrdfits(hkfile, 'HK4FPM', /silent)
    
    ; Load in GTI data
    gtis = mrdfits(gtifile, 1, /silent)

    ; Filter on GTIs:
    print, 'Filtering events...'
    evt = filter_nustar(ufevt, hkdata, gti=gtis)
    nevt = n_elements(evt) 
   
   ; Get event data:
    new_evt = replicate(ev_stub, nevt) 
    new_evt.time = evt.time
    new_evt.det_id = evt.det_id
    new_evt.grade = evt.grade
    new_evt.rawx = evt.rawx
    new_evt.rawy = evt.rawy
    new_evt.depthflag = (evt.status[1] EQ depth_cut)
    new_evt.pi = evt.pi_clc
    new_evt.surrpi = evt.surrpi
    
;;    IF nevt GT 1000 THEN stop

   ; Get the info you want from the attorb file:

    attorb = mrdfits(datpath+'/nu'+seqid+ab[iab]+'.attorb', 1, /silent)
   ; Interpolate the attorb values onto the event times:
    new_evt.sunshine = interpol(attorb.sunshine, attorb.time, evt.time)
    new_evt.ram_angle = interpol(attorb.ram_angle, attorb.time, evt.time)
    new_evt.geomag = interpol(attorb.cor_asca, attorb.time, evt.time)
    new_evt.lon = interpol(attorb.sat_lon, attorb.time, evt.time)
    new_evt.lat = interpol(attorb.sat_lat, attorb.time, evt.time)
    new_evt.alt = interpol(attorb.sat_alt, attorb.time, evt.time)
    new_evt.limb_angle = interpol(attorb.elv, attorb.time, evt.time)
    

    ; Interpolate temperatures from the HK file:
;    new_evt.temp = interpol(hkdata.
    temps = fltarr(4, n_elements(hk4data)) 
    FOR det = 0, 3 DO begin
       thisdet = where(new_evt.det_id EQ det)
       new_evt[thisdet].temp = interpol(hk4data.(10+det), hk4data.time, new_evt[thisdet].time)
    ENDFOR



    mwrfits, new_evt, outfits, /create, /silent

   ; Reread to fix the header:
   evt = mrdfits(outfits, 1, evth, /silent)
   fxaddpar, evth, 'TSTART', tstart
   fxaddpar, evth, 'MJDREF', mjdref
   fxaddpar, evth, 'DATE-OBS', date_obs
   fxaddpar, evth, 'RA_OBJ', ra
   fxaddpar, evth, 'DEC_OBJ', dec
   fxaddpar, evth, 'EXPOSURE', exp
   mwrfits, new_evt, outfits, evth, /create, /silent

ENDFOR
   

   

   
   

   




END





   

