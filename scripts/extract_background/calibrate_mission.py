import glob
from astropy.io.fits import getdata
import pandas as pd
import os
#%matplotlib notebook
#import matplotlib.pyplot as plt
import numpy as np
neigh_x = [-1,  0, 1, -1, 0, 1, -1,  0, 1]
neigh_y = [-1, -1, -1,  0, 0,  0, +1, +1, +1]


def calibrate_files():

    allev = None
    for file in glob.glob('./full_mission/*'):
        if 'notime' in file:
            continue
        
        print(file)
        temperature_calibrate_phas(file)

    return allev
    
def read_calibrated_files(fpm='A'):
    allev = None
    for file in glob.glob('./full_mission/*'+fpm+'*notime*'):
        print(file)
        from astropy.table import Table
        evts = Table.read(file, hdu=1)
        print(len(evts))
        if allev is None:
            allev = evts.to_pandas()
        else:
            allev = allev.append(evts.to_pandas(), ignore_index=True)
            print(len(allev))
    return allev
    
def temperature_calibrate_phas(file):
    """
    Read in the data and apply the baseline temperature calibration
    """
    
    from astropy.io.fits import getdata
    from astropy.table import Table
    import numpy as np
    import os.path


    outfile = file.rstrip('.fits')+'_notime.fits'

    if os.path.isfile(outfile):
        return
    
    
    evts = Table.read(file, hdu=1)
    evts['PI'] = np.nan


    if 'A' in file :
        FPM = 'A'
    else:
        FPM='B'

    CALDB='/Users/bwgref/science/local/CALDB'
    gain_file = CALDB+'/data/nustar/fpm/bcf/gain/nu'+FPM+'gain20100101v007.fits'
    clc_file = CALDB+'/data/nustar/fpm/bcf/clc/nu'+FPM+'clc20100101v004.fits'

    for det in range(4):
        print(det)

        gainpar = getdata(gain_file, det + 1)
        clcpar = getdata(clc_file, det +1 )


        # Loop over all events:
        for ind in range(len(evts)):
            if evts['GRADE'][ind] != 0:
                continue
            rawx = evts['RAWX'][ind]
            rawy = evts['RAWY'][ind]
            phas = evts['PHAS'][ind]
            temp = evts['TEMP'][ind]

            for jj in range(9):
                if jj != 4:
                    continue
                thisx = rawx + neigh_x[jj]
                thisy = rawy + neigh_y[jj]
                caldb_ind = 2*(thisx *32 + thisy)
                clc_ind = (thisx *32 + thisy)
                slope = np.interp(temp, gainpar['TEMP'][caldb_ind],gainpar['SLOPE'][caldb_ind])
                offset = np.interp(temp, gainpar['TEMP'][caldb_ind],gainpar['OFFSET'][caldb_ind])

                pis_gain = phas[jj] * slope + offset

                # Skip CLC correction for multiple grades and just apply Grade-Gain Correction 
                evts['PI'][ind] = pis_gain * clcpar['GR_SLOPE'][clc_ind][0] + clcpar['GR_OFFSET'][clc_ind][0]


    #                print(rawx, rawy)
    #             thisevt = np.where( (evts['DET_ID'] == det) & 
    #                                 (evts['RAWX'] == rawx) & 
    #                                 (evts['RAWY'] == rawy) &
    #                                 (evts['GRADE'] == 0))
    #             thisevt = thisevt[0]

    #             pis = np.zeros([len(thisevt), 9])
    #             for jj in range(9):
    #                 if (thisx < 0) | (thisx > 31) | (thisy < 0) | (thisy > 31):
    #                     continue

    #                 pis = slope*evts['PHAS'][thisevt] * slope + offset
    # #               evts['PIS'][thisevt][jj] = slope*evts['PHAS'][thisevt][jj] * slope + offset

    #                 break
    #             if thisevt is not None:
    #                 break
    #         if thisevt is not None:
    #             break
    #     break
    #                evts['PI'] = slope*evts['PPHAS']
                    #                evts['PI'][thisevt] = (slope*evts['PI'][thisevt]+offset)
    evts[np.where(~np.isnan(evts['PI']))]
    evts.remove_column('PHAS')
    evts.write(outfile, format='fits')

    return
    
calibrate_files()