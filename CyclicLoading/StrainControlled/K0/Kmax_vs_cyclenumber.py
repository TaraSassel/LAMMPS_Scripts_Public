# Author:   Tara Sassel
# Date:     27/03/23

# Kmax vs cycle number

# Imports 
import os 
import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt 
import matplotlib.lines as mlines
import matplotlib.patches as mpatches

from cyclicStrainK0 import get_K0_info
from basicFunctions.get_strain import get_strain

# =================================================================================================
# Fontisze
LBF = 16    # Label Fontsize
TS = 14     # Ticksize
LGF = 14    # Legend Font
lw1 = 2     # Line width 
TF = 16     # Legend title font

strainInfo = get_K0_info('E') # Drive Number example: 'E'
N = 101             # Number of cycles
color_list = ['lightgreen', 'lightsteelblue','mediumpurple', 'lightcoral']

depths = [2, 4, 6, 8]
amplitudes = [0.1, 0.5, 1] 

# Initiating figure 
fig = plt.figure(figsize = (12,7))

# Looping trough data 
for which_depth in depths: 
    for which_strain_amplitude in amplitudes:
        which_friction_coefficient = 0.25  # 0.1, 0.15 or 0.25
        
        c = color_list[int(which_depth/2-1)]

        if which_strain_amplitude == 0.1:
            ls1 = ':'
        if which_strain_amplitude == 0.5:
            ls1 = '--'
        if which_strain_amplitude == 1:
            ls1 = '-'

        

        # =================================================================================================
        # change directory to selected data set
        wanted_data = strainInfo[
            (strainInfo.depth == which_depth) &\
            (strainInfo.strain_amplitude == which_strain_amplitude) &\
            (strainInfo.friction_coefficient == which_friction_coefficient)]

        path_list = list(wanted_data.path)
        cyclic_turns = list(wanted_data.cyclic_turns)

        print(path_list[0])
        os.chdir(path_list[0] + r'/merged_data')

        # Load Data
        stress_data = pd.read_csv('stress_data.csv')

        # Adapt Data
        stress_data['strain_z'] = get_strain(stress_data['length_z'])
        stress_data['cycle_number'] = stress_data.step_s/(cyclic_turns[0]*2)
        stress_data['cycle_number'] = stress_data['cycle_number'].round()

        
        cycle_number_list = list(stress_data['cycle_number'].unique())
        Kmax = np.zeros(len(cycle_number_list, ))
        for i, number in enumerate(cycle_number_list):
            if number < N:
                print(number)
                cycle_data = stress_data[stress_data['cycle_number'] == number]
                stress_ratio = cycle_data.stress_yy.to_numpy()/cycle_data.stress_zz.to_numpy()
                Kmax[i] = np.max(stress_ratio)

        # Figure
        plt.plot(cycle_number_list, Kmax, color = c, ls = ls1, lw = lw1)

# =================================================================================================
ax = plt.gca()

# Limits
plt.xlim(0,100)
plt.ylim(0.8,1.8)

# Labels
plt.xlabel(r'Cycle number (N)', fontsize = LBF)
plt.ylabel(r'$K_{max}$', fontsize = LBF)
plt.tick_params(axis='both', which='major', labelsize=TS)

# Legend
basecolor = 'gray'

# lg1:
line1 = mlines.Line2D([], [], color=basecolor, ls = ':', label='0.1%', lw = lw1)
line2 = mlines.Line2D([], [], color=basecolor, ls = '--', label='0.5%', lw = lw1)
line3 = mlines.Line2D([], [], color=basecolor, ls = '-', label='1%', lw = lw1)
lg1 = ax.legend(handles=[line1, line2, line3], loc = 'lower right', fontsize = LGF, title = "$\epsilon_{zz}^{ampl}$:", title_fontsize=TF)

# lg2:
patch1 = mpatches.Patch(color = 'lightgreen', label = '2 m')
patch2 = mpatches.Patch(color = 'lightsteelblue', label = '4 m')
patch3 = mpatches.Patch(color = 'mediumpurple', label = '6 m')
patch4 = mpatches.Patch(color = 'lightcoral', label = '8 m')

lg2 = ax.legend(handles=[patch1, patch2, patch3, patch4], loc = 'upper center', fontsize = LGF, title = "Depth:", ncol = 4, title_fontsize=TF)

ax.add_artist(lg1)

plt.show()

