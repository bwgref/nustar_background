#!/usr/local/bin/bash

for obs in full_mission/*
do
    obsid=`basename $obs`
    if [ ! -e ${obs}/nu${obsid}A02_cl.evt ]; then
        
        if [ ! -e ${obs}/${obsid}/event_cl/nu${obsid}A02_cl.evt ]; then
            echo No A02 file!
            echo Missing file!
            echo $obs
        else
            echo Some other reason!
            echo $obs
            echo
        fi
        rm -rf $obs
    fi
done
