import numpy as np
import glob
from astropy.io.fits import getdata, getheader, writeto, append, setval


from os.path import normpath, basename

import pickle






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
            data_table[mod][det_key] = {'exp':0.}

    for ind, evtdir in enumerate(evtdirs):
        for mod in ['A', 'B']:

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
                
                for det_id in range(4):
                    det_key = 'det{}'.format(det_id)
 
                    elec_filter = ~ ( \
                                (evdata['STATUS'][:, 10]) | \
                                (evdata['STATUS'][:, 8]) | \
                                (evdata['STATUS'][:, 7]) | \
                                (evdata['STATUS'][:, 6]) | \
                                (evdata['STATUS'][:, 5]) | \
                                (evdata['STATUS'][:, 4]) ) 

                    evt_filter = (elec_filter) & \
                        (evdata['DET_ID'] == det_id) & \
                        (ev_elv < -1) 

                    good_inds = np.where(evt_filter)[0]

                    depth_im, xedges, yedges = np.histogram2d(evdata['PI'][good_inds], evdata['SURRPI'][good_inds],
                                                            bins = [500, 300], range = [[-40, 960], [-500, 100]])


                    elec_filter = ~ ( \
                                      (evdata['STATUS'][:, 10]) | \
                                      (evdata['STATUS'][:, 7]) | \
                                      (evdata['STATUS'][:, 6]) | \
                                      (evdata['STATUS'][:, 5]) | \
                                      (evdata['STATUS'][:, 4]) ) 

                    evt_filter = (elec_filter) & \
                        (evdata['DET_ID'] == det_id) & \
                        (ev_elv < -1) & (evdata['STATUS'][:, 8])

                    good_inds = np.where(evt_filter)[0]
                    
                    depth_im_flagged, xedges, yedges = np.histogram2d(evdata['PI'][good_inds], evdata['SURRPI'][good_inds],
                                                            bins = [500, 300], range = [[-40, 960], [-500, 100]])


                    if 'depth_im' not in data_table[mod][det_key]:
                        data_table[mod][det_key]['depth_im'] = depth_im
                        data_table[mod][det_key]['depth_im_flaged'] = depth_im_flagged
                        data_table[mod][det_key]['pi_edges'] = xedges
                        data_table[mod][det_key]['surrpi_edges'] = yedges
                    else:
                        data_table[mod][det_key]['depth_im'] += depth_im
                        data_table[mod][det_key]['depth_im_flaged'] += depth_im_flagged

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

    outname='{}_depth_lowe.pkl'.format(epoch)
    pickle_out = open(outname,"wb")
    pickle.dump(dtab, pickle_out)
    pickle_out.close()



    
