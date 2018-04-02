#!/bin/bash

source $NUSTARSETUP

# The sequence ID
OBSID=$1

INDIR=full_mission/${OBSID}/${OBSID}
OUTDIR=full_mission/${OBSID}


#infile=${INDIR}/event_cl/nu${OBSID}${MOD}_uf.evt
#hkfile=${INDIR}/event_cl/nu${OBSID}${MOD}_fpm.hk
#outfile=${OUTDIR}/nu${OBSID}${MOD}_uf.evt
mastfile=${INDIR}/event_cl/nu${OBSID}_mast.fits
psdcorfile=${INDIR}/event_cl/nu${OBSID}_psdcorr.fits

gainfile=/home/nustar1/SOC/CALDB/data/nustar/fpm/bcf/gain/nu${MOD}gain20100101v005.fits
logfile=${OUTDIR}/nu${OBSID}${MOD}.log
clobber=yes

cmd="nupipeline \
      obsmode=OCCULTATION \
      pntra=OBJECT pntdec=OBJECT \
      indir=${INDIR} \
      steminputs=nu${OBSID} \
      inmastaspectfile=$mastfile runmetrology=no \
      inpsdfilecor=$psdcorfile \
      outdir=${OUTDIR}"

echo $cmd
$cmd > $logfile 2>&1 
#done




