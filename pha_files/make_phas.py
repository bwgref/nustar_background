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

def sort_seqid():
    # Setup NuSTAR time epochs:
    launch_met=77241600. # 2012-06-13T00:00:00
    # Quaterly plots
    
    # Set up data structure:
    seqid_list = {}

        
    for ind, evtdir in enumerate(glob.glob('../scripts/reprocess_background/full_mission/*/')):
        for file in glob.glob('{}/*{}02_cl.evt'.format(evtdir, mod)):
        # Skip these high background obsids
            if file.find("40101012") != -1:
                continue

            if file.find("30161002002") != -1:
                continue

            hdr= getheader(file, 1)
            epoch = np.float(hdr['TSTART'])
            dt_years = (epoch-launch_met) / 3.154e7 # years
            dt_quarter = dt_years
            epoch_ind = np.int(np.floor(dt_quarter))

            e_key = 'epoch{}'.format(epoch_ind)
            if e_key not in seqid_list:
                seqid_list[e_key] = [evtdir]
            else:
                seqid_list[e_key].append(evtdir)
    return seqid_list

def load_data_clean(evtdirs):
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
            data_table[mod][det_key] = {'spec':np.zeros(4096),
                                        'exp':0.}
    
    for ind, evtdir in enumerate(evtdirs):
        for mod in ['A', 'B']:
            for file in glob.glob('{}/*{}02_cl.evt'.format(evtdir, mod)):
            # Skip these high background obsids
                if file.find("40101012") != -1:
                    continue

                if file.find("30161002002") != -1:
                    continue

                hdr= getheader(file, 1)

                evdata = getdata(file, 1)
                
                for det_id in range(4):
                    det_key = 'det{}'.format(det_id)
 
                     evt_filter = ~ (
                                (evdata['STATUS'][:, 8]) | (evdata['STATUS'][:, 7]) \
                                | (evdata['STATUS'][:, 6]) | (evdata['STATUS'][:, 6]) \
                                | (evdata['STATUS'][:, 5]) | (evdata['STATUS'][:,4])
                                ) & (evdata['DET_ID'] == det_id)
                    good_inds = np.where(evt_filter)[0]
                    ehist, edges = np.histogram(evdata['PI'][good_inds],
                                        range = [0, 4096],
                                        bins=4096)
                    data_table[mod][det_key]['spec'] += ehist
                    data_table[mod][det_key]['exp'] +=np.float(hdr['EXPOSURE'])

        if (ind % 10) ==0:
            print('{} of {}'.format(ind, len(evtdirs)))
    return data_table
    



seqid_list = sort_seqid()
dtab = load_data()

for epoch in seqid_list:
    print(epoch)
    
    evtdirs = seqid_list[epoch]
    dtab = load_data_clean(evtdirs)
    
    for mod in dtab:
        for det_id in dtab[mod]:
            outname='{}_{}_FPM{}_repro.pha'.format(epoch, det_id, mod)
            print(outname)
            write_spec(dtab[mod][det_id]['spec'], 
                       dtab[mod][det_id]['exp'], det_id = det_id, outname=outname)
