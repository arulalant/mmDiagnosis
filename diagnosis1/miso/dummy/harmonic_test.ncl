load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl" 
   
   system ("rm  hclim_ncl.nc")
   diri    = "./"                             ; input directory   
   fili    = "precip_2000.nc"                         ; input file       
   f       = addfile (diri+fili , "r")                          
;***********************************************************
; Read time and create required yyyyddd                    
;***********************************************************
   time    = f->time                          ; time:units = "hours since 1-1-1 00:00:0.0"                               
   TIME    = cd_calendar(time, 0)          ; type float 
   year    = toint( TIME(:,0) )
   month   = toint( TIME(:,1) )
   day     = toint( TIME(:,2) ) 
   ddd     = day_of_year(year, month, day) 
   yyyyddd = year*1000 + ddd                                  ; needed for input
;***********************************************************
; Read data: short2flt                                     
;*********************************************************** 
   precip_data     =   f->precip     ; convert to float 
;***********************************************************
; Compute raw daily climatology  
;***********************************************************
   hClmDay    = clmDayTLL(precip_data, yyyyddd)     ; daily climatology at each grid point                                      
;***********************************************************
; Compute smoothed daily climatology using 2 harmonics  
;***********************************************************
   hClmDay_sm = smthClmDayTLL(hClmDay, 3)  
   printVarSummary(hClmDay_sm)
  
   
    filo="hclim_2000_ncl.nc"
        fo =addfile(filo,"c")  ;open output file
      ;  fo@title= "Roms MLD Monthly Climatology at each Grid Point"
      ;  SST_MON_CLIM = new((/12,241,361/),float)
      ;;  SST_MON_CLIM!0 = "TIME"
      ;  SST_MON_CLIM!1="LAT"
      ;  SST_MON_CLIM!2="LON"
        fo->precip=hClmDay_sm

