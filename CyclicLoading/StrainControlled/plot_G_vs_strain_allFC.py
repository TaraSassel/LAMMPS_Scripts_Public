"""
Author: Tara Sassel
Date: 14/12/2022
This strain plots the stress strain loops for the strain controlled cyclic data 
"""

# Imports 
import os 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import matplotlib.patches as mpatches
import matplotlib.image as image
from PIL import Image

from matplotlib.offsetbox import (OffsetImage, AnnotationBbox)

from cyclicStrain import get_strain_info
from basicFunctions.get_strain import get_strain

# =================================================================================================
strainInfo = get_strain_info("E") # Drive Number example: 'E'
N = 101             # Number of cycles

# Fontisze
LBF = 16    # Label Fontsize
TS = 14     # Ticksize
LGF = 14    # Legend Font 
lw1 = 2     # Line Width 
TF = 14     # Legend title font


# Define wanted dataset 
which_iso_stress = 300            
amplitudes = [0.1, 0.5, 1]       
FCs = [0.15, 0.25]   # 0.1, 0.15 or 0.25
color_list = ['black','indianred']
ls_list = [':','--','-']
fig = plt.figure(figsize = (10,5))

for k, which_friction_coefficient in enumerate(FCs):
    for j, which_strain_amplitude in enumerate(amplitudes): 

        # =================================================================================================
        # change directory to selected data set
        wanted_data = strainInfo[
            (strainInfo.iso_stress == which_iso_stress) &\
            (strainInfo.strain_amplitude == which_strain_amplitude) &\
            (strainInfo.friction_coefficient == which_friction_coefficient)]

        path_list = list(wanted_data.path)
        print(path_list[0])
        cyclic_turns = list(wanted_data.cyclic_turns)
        os.chdir(path_list[0] + r'/merged_data')

        # Load Data
        stress_data = pd.read_csv('stress_data.csv')

        # Adapt Data
        stress_data['strain_z'] = get_strain(stress_data['length_z'])/100*1000 # converting back from % to mm 
        stress_data['cycle_number'] = stress_data.step_s/(cyclic_turns[0]*2)
        stress_data['cycle_number'] = stress_data['cycle_number'].round()

        # =================================================================================================
        # Figure
        fig = plt.figure(1, figsize = (10,5))

        cycle_number_list = list(stress_data['cycle_number'].unique())
        G = np.zeros((len(cycle_number_list),))
        for i, number in enumerate(cycle_number_list):
            if number < N:
                print(number)
                cycle_data = stress_data[stress_data['cycle_number'] == number]
                min_strain = min(cycle_data['strain_z'])
                min_stress = min(cycle_data['stress_zz'])/1000
                max_strain = max(cycle_data['strain_z'])
                max_stress = max(cycle_data['stress_zz'])/1000
                G[i] = ((max_stress-min_stress)/(max_strain-min_strain))

        plt.plot(cycle_number_list[0:101],G[0:101], c = color_list[k], ls = ls_list[j], lw = lw1, marker = 'o', mec = 'black', markevery = 5)
        

ax = plt.gca()

# Labels
plt.ylabel(r"Secant stiffness ($G_{sec}$) [$\frac{kPa}{mm}$]", fontsize = LBF)
plt.xlabel('Cycle number (N)', fontsize = LBF)
plt.xlim(0,100)
plt.tick_params(axis='both', which='major', labelsize=TS)

# Grid and minor ticks

plt.grid(which = 'minor', color = 'gray', ls = '--')
plt.grid(which = 'major', color = 'dimgray', ls = '-')

plt.ylim(1,)


# Legend
basecolor = 'gray'

# lg1:
line1 = mlines.Line2D([], [], color=basecolor, ls = ':', label='0.1%', lw = lw1, marker = 'o', mec = 'black')
line2 = mlines.Line2D([], [], color=basecolor, ls = '--', label='0.5%', lw = lw1, marker = 'o', mec = 'black')
line3 = mlines.Line2D([], [], color=basecolor, ls = '-', label='1%', lw = lw1, marker = 'o', mec = 'black')
lg1 = ax.legend(handles=[line1, line2, line3], fontsize = LGF, title = "$\epsilon_{zz}^{ampl}$:", title_fontsize=TF, loc='lower left', bbox_to_anchor=(1, 0.01))

# lg2:
patch1 = mpatches.Patch(color = 'black', label = '0.15')
patch2 = mpatches.Patch(color = 'indianred', label = '0.25')


lg2 = ax.legend(handles=[patch1, patch2], loc='upper left', bbox_to_anchor=(1, 1), fontsize = LGF, title = "$\mu_{prep}$:", title_fontsize=TF)

ax.add_artist(lg1)

plt.tick_params(axis = 'both', which = 'major', labelsize = TS)
plt.grid(which = 'minor', color = 'gray', ls = '--')
plt.grid(which = 'major', color = 'dimgray', ls = '-')
plt.tight_layout()
plt.show()