import numpy as np
import glob
from astropy.io.fits import getdata, getheader, writeto, append, setval

def sort_seqid():
    # Setup NuSTAR time epochs:
    launch_met=77241600. # 2012-06-13T00:00:00
    # Quaterly plots
    
    # Set up data structure:
    seqid_list = {}
    mod = 'A'
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
            dt_quarter = dt_years * 2.
            epoch_ind = np.int(np.floor(dt_quarter))

            e_key = 'epoch{}'.format(epoch_ind)
            if e_key not in seqid_list:
                seqid_list[e_key] = [evtdir]
            else:
                seqid_list[e_key].append(evtdir)
    return seqid_list

seqid_list = sort_seqid()
for epoch in seqid_list:
    f = open('{}_list.txt'.format(epoch), 'w')
    for seq in seqid_list[epoch]:
        f.write('{}\n'.format(seq))
    f.close()

