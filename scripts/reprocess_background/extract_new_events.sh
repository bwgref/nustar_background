#!/usr/local/bin/bash

source ~/SOC_setup_FLT.sh

IDL_STARTUP=$HOME/SOC/Level1/idl/startup/defb.pro
IDL_LOC=/usr/local/rsi/idl71/bin

${IDL_LOC}/idl -quiet setup_links_nucalcpi.bat > updates.log
${IDL_LOC}/idl -quiet run_nucalcpi.bat >> updates.log
${IDL_LOC}/idl -quiet run_extract_events.bat >> updates.log

./push_slack.sh updates.log >> /dev/null
