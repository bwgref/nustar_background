from numpy import pi
import numpy as np
from numpy import pi, cos, sin, arctan2, sqrt, dot

def geo2mag(incoord):
    '''
    Code to convert geographic to geomagnetic cooridnates.
    This is a port of geo2mag.pro from here:
    https://idlastro.gsfc.nasa.gov/ftp/pro/astro/geo2mag.pro

    '''
    # SOME 'constants'...
    lon=288.59   # longitude (in degrees) of Earth's magnetic south pole
    #(which is near the geographic north pole!) (1995)
    lat=79.30     # latitude (in degrees) of same (1995)
    r = 1.0          # distance from planet center (value unimportant -- 
                    # just need a length for conversion to 
                    # rectangular coordinates)

    # Convert first to radians
    lon, lat = [x*pi/180 for x in (lon,lat)]
    glat = incoord[0] * pi / 180.0
    glon = incoord[1] * pi / 180.0
    galt = glat * 0. + r
    
    # Convert to rectangular coordinates
    x=galt*cos(glat)*cos(glon)
    y=galt*cos(glat)*sin(glon)
    z=galt*sin(glat)
    xyz = np.vstack((x,y,z))

    # computer 1st rotation matrix:
    geo2maglon = np.zeros((3,3), dtype='float64')
    geo2maglon[0,0] = cos(lon)
    geo2maglon[0,1] = sin(lon)
    geo2maglon[1,0] = -sin(lon)
    geo2maglon[1,1] = cos(lon)
    geo2maglon[2,2] = 1.
    out = dot(geo2maglon , xyz)

    tomaglat = np.zeros((3,3), dtype='float64')
    tomaglat[0,0] = cos(.5*pi-lat)
    tomaglat[0,2] = -sin(.5*pi-lat)
    tomaglat[2,0] = sin(.5*pi-lat)
    tomaglat[2,2] = cos(.5*pi-lat)
    tomaglat[1,1] = 1.
    out = dot(tomaglat , out)
    
    
    mlat = arctan2(out[2], 
            sqrt(out[0]*out[0] + out[1]*out[1]))
    mlat = mlat * 180 / pi
    mlon = arctan2(out[1], out[0])
    mlon = mlon * 180 / pi

    outcoord = np.vstack((mlat, mlon))
    return outcoord

if __name__ == '__main__':
    mag =  geo2mag(np.array([[79.3,288.59]]).T).T
    print(mag)  # should be [90,0]

    mag =  geo2mag(np.array([[90,0]]).T).T
    print(mag)  # should be [79.3,*]

    mag =  geo2mag(np.array([
        [79.3,288.59],
        [90,0]
        ]).T).T

    print(mag)  # should be [ [90,0]. [79.3,*] ]

    # kyoto, japan
    mag =  geo2mag(np.array([[35.,135.45]]).T).T
    print(mag)  # should be [25.18, -155.80], according to 
               # this site using value for 1995
               # http://wdc.kugi.kyoto-u.ac.jp/igrf/gggm/index.html
