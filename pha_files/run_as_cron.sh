#!/usr/local/bin/bash

source $HOME/SOC_setup_FLT.sh

# Go to where things live:
cd /disk/lif2/bwgref/git/nustar_background/pha_files


# Init correct python environment
export PATH=/home/nustar1/$HOSTNAME/src/miniconda3/bin:$PATH
source activate nustar_background

now=`date`
echo $now > phalog.log
echo "Updating PHA Files" >> phalog.log

# Update archive
echo "Updating PHA files for each epoch (takes a while)" >> phalog.log
python make_phas.py >> phalog.log
                    
