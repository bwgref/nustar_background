import numpy as np
import glob
from astropy.io.fits import getdata, getheader, writeto, append, setval


from os.path import normpath, basename

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


def load_data_clean(evtdirs, maxload=False):
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
        for mod in ['B']:

            seqid = basename(normpath(evtdir))
            
            attorb_file = evtdir+'/'+seqid+'/event_cl/nu'+seqid+'{}.attorb'.format(mod)
            attorb = getdata(attorb_file)

            

            for file in glob.glob('{}/*{}02_cl.evt'.format(evtdir, mod)):
            # Skip these high background obsids
                if file.find("40101012") != -1:
                    continue

                if file.find("30161002002") != -1:
                    continue

                hdr= getheader(file, 1)

                evdata = getdata(file, 1)
                ev_elv = np.interp(evdata['TIME'],attorb['TIME'], attorb['ELV'])
                ev_sunshine = np.interp(evdata['TIME'],attorb['TIME'], attorb['SUNSHINE'])

                for det_id in range(4):
                    if det_id != 1:
                        continue

                    det_key = 'det{}'.format(det_id)
 
                    elec_filter = ~ ( \
                                (evdata['STATUS'][:, 10]) | \
                                (evdata['STATUS'][:, 8]) | \
                                (evdata['STATUS'][:, 7]) | \
                                (evdata['STATUS'][:, 6]) | \
                                (evdata['STATUS'][:, 5]) | \
                                (evdata['STATUS'][:, 4]) | \
                                (evdata['STATUS'][:, 3]) ) 
                    
                    evt_filter = (elec_filter) & \
                        (evdata['DET_ID'] == det_id) & \
                        (evdata['GRADE'] == 0) & \
                        (ev_elv < -1) & (ev_sunshine == 0)

                    good_inds = np.where(evt_filter)[0]
                    ehist, edges = np.histogram(evdata['PI'][good_inds],
                                        range = [0, 4096],
                                        bins=4096)
                    data_table[mod][det_key]['spec'] += ehist
                    data_table[mod][det_key]['exp'] +=np.float(hdr['EXPOSURE'])

        if (ind % 10) ==0:
            print('{} of {}'.format(ind, len(evtdirs)))

        if maxload is not False:
            if ind > maxload:
                break
    return data_table
    


for epoch_file in sorted(glob.glob('epoch*_list.txt')):
    print(epoch_file)
    epoch = (epoch_file.split('_'))[0]


    evtdirs = np.loadtxt(epoch_file, dtype='str')
    dtab = load_data_clean(evtdirs)

    for mod in dtab:
        for det_id in dtab[mod]:
            outname='{}_{}_FPM{}_repro_nosun.pha'.format(epoch, det_id, mod)
            print(outname)
            write_spec(dtab[mod][det_id]['spec'], 
                       dtab[mod][det_id]['exp'],
                       det_id = det_id, mod = mod,
                       outname=outname)

    break
