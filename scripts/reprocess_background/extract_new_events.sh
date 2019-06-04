#!/usr/local/bin/bash

source ~/SOC_setup_FLT.sh

IDL_LOC=/usr/local/rsi/idl71/bin

${IDL_LOC}/idl -quiet setup_links_nucalcpi.bat
${IDL_LOC}/idl -quiet run_nucalcpi.bat
${IDL_LOC}/idl -quiet run_extract_events.bat

