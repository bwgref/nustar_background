#!/bin/bash

source ~/SOC_setup_FLT.sh

# The sequence ID
OBSID=$1

INDIR=full_mission/${OBSID}/${OBSID}
OUTDIR=full_mission/${OBSID}

# Default, but turn off depth cut for diagnostics.
type="STATUS==b00000000xx0xx000"

for MOD in A B
do

    infile=${INDIR}/event_cl/nu${OBSID}${MOD}_uf.evt
    hkfile=${INDIR}/event_cl/nu${OBSID}${MOD}_fpm.hk
    outfile=${OUTDIR}/nu${OBSID}${MOD}_uf.evt
    mkfile=${INDIR}/event_cl/nu${OBSID}${MOD}.mkf

    clfile=${OUTDIR}/nu${OBSID}${MOD}02_cl.evt

    gainfile=/home/nustar1/SOC/CALDB/data/nustar/fpm/bcf/gain/nu${MOD}gain20100101v005.fits
    logfile=${OUTDIR}/nu${OBSID}${MOD}.log
    clobber=yes
    
    cmd="nucalcpi \
    infile=$infile gainfile=$gainfile \
    hkfile=$hkfile outfile=$outfile clobber=yes"

    echo $cmd
    $cmd > $logfile 2>&1 


    cmd="nuscreen obsmode=OCCULTATION \
     infile=$outfile \
     gtiscreen=yes evtscreen=no gtiexpr=DEFAULT \
     createattgti=yes \
     createinstrgti=yes \
     outdir=$OUTDIR \
     hkfile=$hkfile \
     mkffile=$mkfile \
     cleancols=no \
     outfile=DEFAULT clobber=yes"

    echo $cmd
    $cmd >> $logfile 2>&1

    # Cleanup
    rm $outfile

done




