#!/usr/bin/python                                                                                                                                                                                                 

# modules
from MChem_tools import *
import numpy as np
import sys

# setup - get species
species       			= 'O3'#'CO2'
RMM_species 	= 16.*3.
try:    # chcck if a directory was given ad command line
	wd    = sys.argv[1]
except: # Otherwise use path below
#	wd    = '/work/home/ts551/data/all_model_simulations/standard_code_runs/standard_run_code_13_01_17_1_year/run'
	wd    = '<insert GEOS-Chem run direcotory path here>'

# get data as 4D array ( lon, lat, alt, time ) 
ctm_f 	      = open_ctm_bpch( wd ) 
data          = get_gc_data_np( ctm_f, species )
air_mass      = get_air_mass_np( ctm_f )  

# calc the total & mean mass of a speices - select data you want to calc & print
air_moles     = ( air_mass*1E3 ) / ( .78*28.+.22*32. )   # mass (convert to g) / RMM air
species_moles = air_moles * data                         # moles * v/v
species_mass  = species_moles * RMM_species              # convert to mass
print species_mass.shape
print np.sum( species_mass )  / 1E12                     # Convert to Tg
print np.sum( np.mean( species_mass, axis=3 ) ) / 1E12   # Convert to Tg

#  select data you want to plot - set as mean() of time, but simply remove 'mean(axis=3)' & give number to select desired timestamp
data          = data[:,:,:,:].mean( axis=3 )

# select surface layer
print data.shape
data          = data[:,:,0]
print data.shape
data          = np.transpose( data )
print data.shape

# plot surface
plt, cb       = plot_geos_alt_slice( data )
plt.show()
