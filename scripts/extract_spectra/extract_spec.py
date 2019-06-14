import numpy as np
import glob
from astropy.io.fits import getdata, getheader, writeto, append, setval

def write_spec(outspec, exp, outname='draft.pha', det_id= 0, mod='A'):
    # Read the template
    null, hdr = getdata('nu30001039002_srcA_sr.pha', 0, header=True)
    writeto(outname, null, header=hdr, overwrite=True)
    spec, hdr = getdata('nu30001039002_srcA_sr.pha', 1, header=True)
    spec['COUNTS'] = outspec
    hdr['RESPFILE'] = 'det{}{}.rmf'.format(det_id, mod)
    hdr['BACKFILE'] = ''
    hdr['ANCRFILE'] = ''
    hdr['EXPOSURE'] = 1.0
    append(outname, spec, hdr)

def read_spec(infile, det_id=0):
    # returns spec, edges, exposure
    evdata = getdata(infile, 1)
    
    # Just take DET0 and GRADE==0 for now:
    filter = ((evdata['GRADE']==0) &
              (evdata['DET_ID']==det_id) &
              (evdata['LIMB_ANGLE'] < -2) &
              (evdata['DEPTHFLAG']==0) )
              inds = filter.nonzero()
              
              ehist, edges = np.histogram(evdata['PI'][inds[0]],
                                          range = [0, 4096],
                                          bins=4096)
              return ehist, edges

def load_data(mod='A', det_id = 0):
    # Returns the full mission data unbinned spectrum
    # set divided into epochs along with exposure.
    
    # Setup NuSTAR time epochs:
    launch_met=77241600. # 2012-06-13T00:00:00
    # Yearly plots for now
    epochs = 6
    multi=4 # quarterly
    
    spec = np.zeros([epochs*multi, 4096])
    exp = np.zeros(epochs)
    indir ='../scripts/reprocess_background/full_mission'
    for ind, evtdir in enumerate(glob.glob(indir+'/*/')):
        
        for file in glob.glob('{}/*{}_02.fits'.format(evtdir, mod)):
            
            
            # Skip these high background obsids
            if file.find("40101012") != -1:
                continue
            
            if file.find("30161002002") != -1:
                continue
            
            hdr= getheader(file, 1)
            epoch = np.float(hdr['TSTART'])
            dt_years = (epoch-launch_met) / 3.154e7 # years
            epoch_ind = np.int(np.floor(dt_years) * multi)
            
            
            ehist, edges = read_spec(file, det_id=det_id)
            spec[epoch_ind, :]+=ehist
            exp[epoch_ind] +=np.float(hdr['EXPOSURE'])

    return spec, exp


for mod in ['A', 'B']:
    for det_id in np.arange(4):
        
        spec, exp = load_data(mod=mod, det_id = det_id)
        
        for ind in np.arange(len(spec[:, 0])):
            #            if(exp[ind] == 0):
            #                continue
            outname='../pha_files/year{}_det{}_FPM{}_repro.pha'.format(ind, det_id, mod)
            print(outname)
            write_spec(spec[ind, :], exp[ind], det_id = det_id, mod = mod, outname=outname)
