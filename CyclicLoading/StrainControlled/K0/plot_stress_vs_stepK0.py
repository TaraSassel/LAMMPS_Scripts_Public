"""
Author: Tara Sassel
Date: 12/01/2023

Stressevolution during K0 
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
which_depth = None                  # 2, 4, 6 or 8m
which_strain_amplitude = None       # 0.1, 0.5 or 1
which_friction_coefficient = None   # 0.1, 0.15 or 0.25

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
stress_xx = stress_data.stress_xx.to_numpy().T/1000
stress_yy = stress_data.stress_yy.to_numpy().T/1000
stress_zz = stress_data.stress_zz.to_numpy().T/1000

# FIGURE 
fig = plt.figure(figsize = (7,7))

plt.plot(step, stress_xx, color = 'black', lw = 2, label = "$\sigma'_{xx}$")
plt.plot(step, stress_yy, color = 'red', lw = 2, label = "$\sigma'_{yy}$")
plt.plot(step, stress_zz, color = 'blue', lw = 2, ls = ':', label = "$\sigma'_{zz}$")

# Legend
plt.legend(loc = 'upper left', fontsize = LGF)

# Labels
plt.ylabel('Stress [kPa]', fontsize = LBF)
plt.xlabel('Step number', fontsize = LBF)
plt.tick_params(axis='both', which='major', labelsize=TS)

# Grid and minor ticks
plt.grid(which = 'minor', color = 'gray', ls = '--')
plt.grid(which = 'major', color = 'dimgray', ls = '-')

plt.show()