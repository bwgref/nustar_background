


!quiet=1


base = getenv('HOME')
!path = expand_path('+'+base+'/SOC/Level1/idl/startup/')+':'+$
        !path
	
.run run_extract_events
run_extract_events


exit
