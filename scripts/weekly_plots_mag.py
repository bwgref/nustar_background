import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as colors
import pandas as pd
import glob
from astropy.io.fits import getdata, getheader

from geo2mag import geo2mag


def show_map(map, exposure, thist, tbins):
    fig = plt.figure(figsize=(28, 12))
    ax = fig.add_subplot(211, title='Counts')
    plt.imshow(
                map,
                interpolation='nearest', origin='low',
                cmap=cm.jet, extent=[-180, 180, -20, 20],
                aspect=4,
                vmin=1.0, vmax=20.)
#                norm=colors.LogNorm(vmin=1.0, vmax = 10.))
    plt.colorbar()

    ax = fig.add_subplot(212, title='imshow: square bins')
#     plt.show()

    plt.imshow(
                exposure,
                interpolation='nearest', origin='low',
                cmap=cm.jet, extent=[-180, 180, -20, 20],
                aspect=4,vmin=1.0, vmax =5.)
    plt.colorbar()
#     
#     ax = fig.add_subplot(312, title='Rate')
# 
#     plt.semilogy(tbins[:-1], thist/timebin, 'b-')
#     plt.ylim(0.01, 1e2)

    plt.show(block=False)
    input("Press Enter to continue...")

    plt.close(fig)



# Step one, sort all of the data:

for ind, file in enumerate(glob.glob('../full_mission/*A_02*')):
    # Load the header:
    hdr = getheader(file, 1)
#    dt_weeks = np.floor((hdr['TSTART'] - launch_met) / (7 * 86400.))
#    print(dt_weeks)
    stub= {'TSTART':np.float(hdr['TSTART']),
           'FNAME':file,
           'DATE-OBS':hdr['DATE-OBS']}
    if(ind==0):
        dbase = [stub]
    else:
        dbase.append(stub)


df = pd.DataFrame(dbase)
df_sorted = df.sort_values(by='TSTART')

interval = 38*86400. # Weekly
reset_interval=1

nlatbins = 90
nlonbins = 360
timebin = 100. # seconds

#for ind, file in enumerate(df_sorted['FNAME']):
c=0
for ind, row in df_sorted.iterrows():    
    c+=1
#     if(c<2650):
#         continue
        
    file = row['FNAME']
    print(c, ind, file, row['DATE-OBS'])
    evt = getdata(file, 1)
    hdr = getdata(file, 1)
    if(reset_interval == 1):
        tmin = evt['TIME'].min()

    time_filter=( ((evt['TIME'] - tmin) < interval) &
                   (evt['LIMB_ANGLE'] < -5)
                ).nonzero()

    incoords = np.array([evt['LAT'][time_filter],
                         evt['LON'][time_filter] ])

    magcoords = geo2mag(incoords)
    

#    thismap, xedges, yedges = np.histogram2d(evt['LON'][time_filter],
#                             evt['LAT'][time_filter],
#                             range = [[0, 360], [-6.5, 6.5]],
#                             bins=[nlonbins, nlatbins])

    thismap, xedges, yedges = np.histogram2d(magcoords[1],
                             magcoords[0],
                             range = [[-180, 180], [-20, 20]],
                             bins=[nlonbins, nlatbins])


    thist, tedges = np.histogram(evt['TIME'][time_filter],
        range=[tmin, tmin+interval],
        bins = interval / timebin)

    if(reset_interval == 1):
        tmin = evt['TIME'].min()
        reset_interval=0
        allmap = thismap
        exposure = np.zeros_like(allmap)
        all_thist = thist
        all_tedges = tedges
        
    else:
        allmap+=thismap  
        filled = (thismap > 0).nonzero()
        exposure[filled] += 1.0
        all_thist += thist

    if(max(evt['TIME']) > tmin + interval):    
        filled = (exposure > 0).nonzero()
        allmap[filled] = allmap[filled] / exposure[filled]

        plotmap = allmap.T
        plotexp = exposure.T

        empty =(plotmap == 0).nonzero()
        plotmap[empty]=np.nan
        plotexp[empty] = np.nan

        show_map(plotmap, plotexp, all_thist, tedges)
 
        reset_interval=1


