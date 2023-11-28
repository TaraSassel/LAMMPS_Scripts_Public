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
LBF = 18    # Label Fontsize
TS = 16     # Ticksize
LGF = 16    # Legend Font 
TF = 18     # Title Font 
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
        stress_data = pd.read_csv('stress_data.csv')

        # Adapt Data
        stress_data['strain_z'] = get_strain(stress_data['length_z'])/100*1000 # converting back from % to mm 
        stress_data['cycle_number'] = stress_data.step_s/(cyclic_turns[0]*2)
        stress_data['cycle_number'] = stress_data['cycle_number'].round()

        # =================================================================================================
        # Figure
        fig = plt.figure(1, figsize = (15,5))

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

        plt.plot(cycle_number_list[0:101],G[0:101], c = color_list[k], ls = ls_list[k], lw = lw1)
        k += 1 

ax = plt.gca()
# import image
sub_fig = image.imread(r'C:\Users\taras\My Drive\PhD\My Writing\Figures_For_Thesis\Gcyc.png')
imagebox = OffsetImage(sub_fig, zoom=0.05)
ab = AnnotationBbox(imagebox, (50, 240))
ax.add_artist(ab)

# Labels
plt.ylabel(r"Cyclic stiffness ($G_{cyc}$) [$\frac{kPa}{mm}$]", fontsize = LBF)
plt.xlabel('Cycle number (N)', fontsize = LBF)
plt.xlim(0,100)
plt.tick_params(axis='both', which='major', labelsize=TS)

# Grid and minor ticks

plt.grid(which = 'minor', color = 'gray', ls = '--')
plt.grid(which = 'major', color = 'dimgray', ls = '-')

plt.ylim(0,300)

# Legend
basecolor = 'gray'

# lg1:
line1 = mlines.Line2D([], [], color=basecolor, ls = ':', label='0.1%', lw = lw1)
line2 = mlines.Line2D([], [], color=basecolor, ls = '--', label='0.5%', lw = lw1)
line3 = mlines.Line2D([], [], color=basecolor, ls = '-', label='1%', lw = lw1)
lg1 = ax.legend(handles=[line1, line2, line3], loc = 'upper left', fontsize = LGF, title = "$\epsilon_{zz}^{ampl}$:", title_fontsize=TF)

# lg2:
patch1 = mpatches.Patch(color = 'darkgreen', label = '100 kPa')
patch2 = mpatches.Patch(color = 'navy', label = '200 kPa')
patch3 = mpatches.Patch(color = 'maroon', label = '300 kPa')

lg2 = ax.legend(handles=[patch1, patch2, patch3], loc = 'upper right', fontsize = LGF, title = "$\sigma'_0$:", title_fontsize=TF)

ax.add_artist(lg1)

plt.tight_layout()
plt.show()