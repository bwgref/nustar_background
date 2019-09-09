import numpy as np
import glob
from astropy.io.fits import getdata, getheader, writeto, append, setval

def write_spec(outspec, exp, outname='draft.pha', det_id='det0', mod='A'):
    # Read the template
    null, hdr = getdata('nu30001039002_srcA_sr.pha', 0, header=True)
    writeto(outname, null, header=hdr, overwrite=True)
    spec, hdr = getdata('nu30001039002_srcA_sr.pha', 1, header=True)
    spec['COUNTS'] = outspec
    hdr['RESPFILE'] = '{}{}.rmf'.format(det_id, mod)
    hdr['BACKFILE'] = ''
    hdr['ANCRFILE'] = ''
    hdr['EXPOSURE'] = exp
    append(outname, spec, hdr)



def load_data():
    # Returns the full mission data unbinned spectrum
    # set divided into epochs along with exposure.
    
    # Setup NuSTAR time epochs:
    launch_met=77241600. # 2012-06-13T00:00:00
    # Quaterly plots
    
    # Set up data structure:
    data_table = {'A':{}, 'B':{}}
    for mod in data_table:
        for det_id in range(4):
            det_key = 'det{}'.format(det_id)
            data_table[mod][det_key] = {}
    
    for ind, evtdir in enumerate(glob.glob('../scripts/reprocess_background/full_mission/*/')):
        for mod in ['A', 'B']:
            for file in glob.glob('{}/*{}_02.fits'.format(evtdir, mod)):
                print(file)
            # Skip these high background obsids
                if file.find("40101012") != -1:
                    continue

                if file.find("30161002002") != -1:
                    continue

                hdr= getheader(file, 1)
                epoch = np.float(hdr['TSTART'])
                dt_years = (epoch-launch_met) / 3.154e7 # years
                dt_quarter = dt_years
            # Change to per-quarter instead
                epoch_ind = np.int(np.floor(dt_quarter))

 
                e_key = 'epoch{}'.format(epoch_ind)

                evdata = getdata(file, 1)
                
                
                for det_id in range(4):
                    det_key = 'det{}'.format(det_id)
                    if e_key not in data_table[mod][det_key]:
                        data_table[mod][det_key][e_key] = {}
                        data_table[mod][det_key][e_key]['spec'] = np.zeros([4096])
                        data_table[mod][det_key][e_key]['exp'] = 0.

                    good_filter = ( (evdata['GRADE']==0) &
                               (evdata['DET_ID']==det_id) &
                               (evdata['LIMB_ANGLE'] < -2) & 
                               (evdata['STATUS']==0) )
                
                    inds = good_filter.nonzero()

                    ehist, edges = np.histogram(evdata['PI'][inds[0]], range = [0, 4096],
                                       bins=4096)

                    data_table[mod][det_key][e_key]['spec'] += ehist
                    data_table[mod][det_key][e_key]['exp'] +=np.float(hdr['EXPOSURE'])
    return data_table
    
dtab = load_data()


for mod in dtab:
    for det_id in dtab[mod]:
        for epoch in dtab[mod][det_id]:
            outname='{}_{}_FPM{}_repro.pha'.format(epoch, det_id, mod)
            print(outname)
            write_spec(dtab[mod][det_id][epoch]['spec'], 
                       dtab[mod][det_id][epoch]['exp'], det_id = det_id, outname=outname)
