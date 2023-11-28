"""
Author: Tara Sassel
Date: 12/01/2023

Wall movement during K0 
"""
# =================================================================================================
# Imports
import os 
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt

from cyclicStrainK0 import get_K0_info

# =================================================================================================
strainInfo =  get_K0_info(None) # Drive Number example: 'E'

# Fontisze
LGF = 12    # Legend Fontsize
LBF = 16    # Label Fontsize
TS = 12     # Ticksize
CBF = 14    # Colorbar Font

# Define wanted dataset 
which_depth = None                 # 2, 4, 6 or 8m
which_strain_amplitude = None      # 0.1, 0.5 or 1
which_friction_coefficient = None  # 0.1, 0.15 or 0.25

# =================================================================================================
# Get Data 
wanted_data = strainInfo[
    (strainInfo.depth == which_depth) &\
    (strainInfo.strain_amplitude == which_strain_amplitude) &\
    (strainInfo.friction_coefficient == which_friction_coefficient)]

path_list = list(wanted_data.path)
cyclic_turns = list(wanted_data.cyclic_turns)

os.chdir(path_list[0] + r'/merged_data')

# Load Data
stress_data = pd.read_csv('stress_data.csv')

# =================================================================================================
step  = stress_data.step_s.to_numpy().T
length_x = stress_data.length_x.to_numpy().T/1000
length_y = stress_data.length_y.to_numpy().T/1000
length_z = stress_data.length_z.to_numpy().T/1000

# FIGURE 
fig = plt.figure(figsize = (7,7))

plt.plot(step, length_x, color = 'black', lw = 2, label = "$length_{x}$")
plt.plot(step, length_y, color = 'red', lw = 2, label = "$length_{y}$")
plt.plot(step, length_z, color = 'blue', lw = 2, ls = ':', label = "$length_{z}$")

# Legend
plt.legend(loc = 'lower left', fontsize = LGF)

# Labels
plt.ylabel('Wall displacement [m]', fontsize = LBF)
plt.xlabel('Step number', fontsize = LBF)
plt.tick_params(axis='both', which='major', labelsize=TS)

# Grid and minor ticks
plt.grid(which = 'minor', color = 'gray', ls = '--')
plt.grid(which = 'major', color = 'dimgray', ls = '-')

plt.show()