#!/bin/bash

source $NUSTARSETUP

# The sequence ID
OBSID=$1

INDIR=full_mission/${OBSID}/${OBSID}
OUTDIR=full_mission/${OBSID}

for MOD in A B
do

    infile=${INDIR}/event_cl/nu${OBSID}${MOD}_uf.evt
    hkfile=${INDIR}/event_cl/nu${OBSID}${MOD}_fpm.hk
    outfile=${OUTDIR}/nu${OBSID}${MOD}_uf.evt

    gainfile=/home/nustar1/SOC/CALDB/data/nustar/fpm/bcf/gain/nu${MOD}gain20100101v005.fits
    logfile=${OUTDIR}/nu${OBSID}${MOD}.log
    clobber=yes
    
    cmd="nucalcpi \
    infile=$infile gainfile=$gainfile \
    hkfile=$hkfile outfile=$outfile clobber=yes"

    echo $cmd
    $cmd > $logfile 2>&1 
done




