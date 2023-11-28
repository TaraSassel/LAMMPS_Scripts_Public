"""
Author: Tara Sassel
Date: 28/03/2023
This strain plots the stress vs cycle number 
"""

# Imports 
import os 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import matplotlib.patches as mpatches

from cyclicStrain import get_strain_info
from basicFunctions.get_strain import get_strain

# =================================================================================================
strainInfo = get_strain_info('E') # Drive Number example: 'E'
N = 101             # Number of cycles

print(strainInfo['strain_amplitude'])
# Fontisze
LBF = 18    # Label Fontsize
TS = 16     # Ticksize
LGF = 14    # Legend font
TF = 18    # Legend title font
lw1 = 2

# Define wanted dataset 
stresses = [100, 200, 300]             
amplitudes = [0.1, 0.5, 1]       
which_friction_coefficient = 0.25   # 0.1, 0.15 or 0.25
color_list = ['darkgreen','darkgreen','darkgreen', 'navy','navy','navy','maroon','maroon','maroon']
ls_list = [':', '--', '-']*3
fig = plt.figure(figsize = (10,7))
k = 0 
for which_iso_stress in stresses:
    for which_strain_amplitude in amplitudes: 

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
        coord_data = pd.read_csv('coord_data.csv')

        # Adapt Data
        coord_data['cycle_number'] = coord_data.step_c/(cyclic_turns[0]*2)
        coord_data['cycle_number'] = coord_data['cycle_number'].round()

        # =================================================================================================
        # Figure
    
        cycle_number_list = list(coord_data['cycle_number'].unique())
        coord_max = np.zeros(len(cycle_number_list),)
        for i, number in enumerate(cycle_number_list):
            if number < N:
                cycle_data = coord_data[coord_data['cycle_number'] == number]
                coord_max[i] = cycle_data['coord_number'].iloc[0]

        plt.plot(cycle_number_list,coord_max, c = color_list[k], ls = ls_list[k], lw = lw1)
        print(color_list[k])
        print(ls_list[k])
        k += 1

# Adjust figure 
ax = plt.gca()

# Limits
plt.xlim(0,100)
plt.ylim(4,5)

# Labels
plt.ylabel(r"Coordination number ($\bar{C}_N$)", fontsize = LBF)
plt.xlabel('Cycle number (N)', fontsize = LBF)
plt.tick_params(axis='both', which='major', labelsize=TS)


# Legend
basecolor = 'gray'

# lg1:
line1 = mlines.Line2D([], [], color=basecolor, ls = ':', label='0.1%', lw = lw1)
line2 = mlines.Line2D([], [], color=basecolor, ls = '--', label='0.5%', lw = lw1)
line3 = mlines.Line2D([], [], color=basecolor, ls = '-', label='1%', lw = lw1)
lg1 = ax.legend(handles=[line1, line2, line3], loc = 'lower right', fontsize = LGF, title = "$\epsilon_{zz}^{ampl}$:", title_fontsize=TF)

# lg2:
patch1 = mpatches.Patch(color = 'darkgreen', label = '100 kPa')
patch2 = mpatches.Patch(color = 'navy', label = '200 kPa')
patch3 = mpatches.Patch(color = 'maroon', label = '300 kPa')

lg2 = ax.legend(handles=[patch1, patch2, patch3], loc = 'upper left', fontsize = LGF, title = "$p'_0$:", title_fontsize=TF)

ax.add_artist(lg1)

plt.grid(which = 'minor', color = 'gray', ls = '--')
plt.grid(which = 'major', color = 'dimgray', ls = '-')
plt.show()