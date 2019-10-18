	FPMA Det 0
	
	- Epoch 0
	    Remove ~122 keV line	

    - Epoch 1 
        - Worked fine with new fits 

    - Epoch 2
        - Worked fine with new fits		

	- Epoch 3
        - Worked fie with new fits

    - Epoch 4
        - Early fit was bad.
        - 155 keV line was hitting lower limit. Changed this to 154 keV 

    - Epoch 5
        - Early fit was really bad
        - Freeze 120 keV width: freeze 14
        - Expand fit range for 148 keV line

    - Epoch 6
        - Removed 122 line
        - Fit worked well

    - Epoch 7
        - Removed 122 line
        - Fit worked well

	- Epoch 8
		- Standard fit
	
	- Epoch 9
		- Standard fit

	- Epoch 10

	- Epoch 11
		Couldn’t get the MCMC to behave nicely. Froze 14 (121 keV line width)
		Break energy unconstrained. newpar cont:2 124 -0.1
		Still a few line widths that are unconstrained, but leaving it be

    	- Had to go back and re-run Epoch 11


	- Epoch 12
		Allow high-energy continuum to vary.:
			thaw cont 1
		
	- Epoch 13
		Worked fine.

    - Epoch 14
        Worked fine





	FPMB Det 0


	- Epoch 0
		- Removed 122 keV line
		- Worked fine

	- Epoch 1 
		- Standard fit

	- Epoch 2 
		- Standard fit


	- Epoch 3
		- Standard Fit

	- Epoch 4
		- freeze 5 (narrow 144 keV line)		

	- Epoch 5
		- Freeze 14 (121 keV line)

	- Epoch 6
		Fine

	- Epoch 7
		Fine

	- Epoch 8
		Freeze 5
		Had to tune model fits since looks like we have worse statistics in this fit
		Note that 144 keV line isn’t being fit very well anymore in the line profile.

	- Epoch 9
		Fine

	- Epoch 10
		Removed 120 keV line
		

	- Epoch 11
		Okay

	- Epoch 12
		Not a great fit at 144 keV in the line shape.

	- Epoch 13
		Make the 121 keV line narrow and refit
		newpar 14 0.1
	

	- Epoch 14
		Works fine.
		
		
	FPMA Det 1
	
	    - Epoch 0 
	        Removed 122 keV line
	        
	        
	    - Epoch 1
	        Fine
	        
	    - Epoch 2
	        Remove 122 keV line
	        
	    - Epoch 3
	        Remove 122 keV line
	    
	    - Epoch 4
	        Base fit seems to work
	        
	    - Epoch 5:
	        Degeneracy in some of the 150 keV line energies, but other lines are fine.
	        
	    - Epoch 6:
	        OK
	        
	    - Epoch 7:
	        freeze 5
	        
	    - Epoch 8:
	        Removed 122 keV line
	        
	    - Epoch 9:
	        Normal
	    
	    - Epoch 10:
	        Freeze 8
	    
	    - Epoch 11:
	        Normal
	        
	    - Epoch 12:
	        Freeze 11
	    
	    - Epoch 13
	        Fine
	        
	    - Epoch 14:
	        Fine
	        
	FPMA Det 2
	    
	    In general, energy resolution is worse, hard to get a good measurement of the
	    line energy.
	    
	    - Epoch 0:
	        Remove 122 keV line
	        Had to expand 105 keV line energy fit range to 107 keV.
	        Hard to get the fit to match...
	    
	    - Epoch 1:
	        Lots of correlated parameters
	        
	    - Epoch 2:
	        Fits better behaved...not sure why...
	        
	    - Epoch 3:
	        thaw 105 keV width
	        thaw 2
	    
	    - Epoch 4:
	        Normal
	    
	    - Epoch 5:
	        Removed 122 keV line
	     
	     - Epoch 6:
	        Standard fit
	        
	        
	    - Epoch 7
	        Removed 122 keV line
	        thaw 2
	    
	    - Epoch 8
	        Removed 122 keV line
	    
	    - Epoch 9
	        Standard fit.
	        Some correlations, may want to burn in again...
	        
	    - Epoch 10 
	        Standard fit.
	    
	    - Epoch 11
	        thaw 2
	    
	    - Epoch 12:
	        thaw 2
	        Allow 144 keV sigma to be >1 keV 
	        
	    - Epoch 13:
	        thaw 2
	    
	    - Epoch 14:
	        Standard fit
	        
	FPMA Det 3:
	
	    - Epoch 0:
	        Remove 122 keV line
	        
	        
	    - Epoch 1:
	        Remove 122 keV line
	        Some odd contours in the nuisance parameters
	        
	    - Epoch 2:
	        Base fit
	    
	    - Epoch 3:
	        Base fit
	    
        - Epoch 4:
            Base fit
            Some odd behavior in the 150 keV range.
        
        - Epoch 5:
            Base fit
            
        - Epoch 6:
            freeze 8
        
        - Epoch 7:
            Base fit
            
            freeze 8
        
        - Epoch 8
            Base fit
        
        - Epoch 9
            Base fit
        
        - Epoch 10
            Base fit
            
        - Epoch 11
            Base fit
            
        - Epoch 12
            Base fit
        
        - Epoch 13
            Base fin
            
        - Epoch 14
            freeze 8
    
    FPMB Det 1:
        
        - Epoch 0 
            Base fit
            
        - Epoch 1
            Base fit
            
        - Epoch 2
            Base fit
        
        - Epoch 3
            Base fit
        
        - Epoch 4
            Base fit
            Significant settling over the first 120,000 steps.
            Doesn't seem to affect parameters we care about.
        
        - Epoch 5
            Base fit
            Lots of weird correlations and bad MCMC run
            freeze 14 (122 keV line width) and try chains again
            
	        Yep, works.
	        
	    - Epoch 6
	        freeze 14
	    
	    - Epoch 7
	        Base fit
	        Some additional burn in...
	        Doesn't affect parameter we care about
	    
	    - Epoch 8
        	freeze 8
        
        - Epoch 9
            Base fit
            
        - Epoch 10
            Base fit
        
        - Epoch 11
            Base fit
        
        - Epoch 12
            Base fit
            Some additional burn in
    
        - Epoch 13:
            Base fit
        
        - Epoch 14
            Base fit
        
        
        
    FPMB Det 2:
        - Epoch 0
            Remove 122 keV line
        
	    - Epoch 1
	        Base fit
	    
	    - Epoch 2
	        Base fit
	        Hard to get the 144 keV line to match.
	        Not a great fit...
	        MCMC seems to settle to a better fit
	        
	    - Epoch 3
	        Base fit
	        
	        
        - Epoch 4
            Base fit
        
        - Epoch 5
            Base fit
            Lots of evolution towards the end of the MCMC run.
        
        - Epoch 6
            freeze 14
        
        - Epoch 7
            Base fit
            
        - Epoch 8
            Base fit
            Some evolution during the fit
        
        - Epoch 9
            Base fit
            
        - Epoch 10 
            Base fit
        
        - Epoch 11
            Base fit

       
        - Epoch 12:
            thaw cont:2
            Something bad with contours....
            144 keV line is degenerate with lots of stuff...
            
            Tried removing 122 keV line, still bad
            
            Need additional burn in?
            thaw cont:2            
            freeze 11
            freeze 5
            
            Seems happier...something odd with the shape of the internal continuum here,
            though...
        
        
        - Epoch 13:
            Base fit
            
        - Epoch 14:
            Base fit
            
    FPMB Det 3:
        - Epoch 0 
            Base fit
            
        - Epoch 1
            Base fit
        
        - Epoch 2
            Base fit
        
        - Epoch 3
            Base fit
        
        - Epoch 4
            Base fit
            
        - Epoch 5
            freeze cont:3
            
            Something really wrong...
            
            try again.
            freeze cont:3
            thaw 17
            
            Some evolution in the fit statistic through the emcee run, but line centroids
            look okay
            
        - Epoch 6
            Base fit
        
        - Epoch 7
            Base fit
            
        - Epoch 8
            Base fit
        
        - Epoch 9
            
        
            
        
        
        
        