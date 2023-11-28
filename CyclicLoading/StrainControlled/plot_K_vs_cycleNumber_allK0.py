"""
Author: Tara Sassel
Date: 12/01/2023
This strain plots the stress strain loops for the K0 strain controlled cyclic data 
"""

# Imports 
import re 
import os 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import matplotlib.patches as mpatches

# Fontisze
LBF = 16    # Label Fontsize
TS = 14     # Ticksize
LGF = 12    # Legend Font 
lw1 = 2     # Line Width 
TxtS = 14   # Text size
TF = 14     # Legend title font

# =================================================================================================
stresses = [100,200,300]
strains = ['0p1','0p5','1']

color_list = ['lightgreen','lightsteelblue','mediumpurple','lightcoral']
ls_list = [':','--','-']
depth_list = [2,4,6,8]

for i, depth in enumerate(depth_list): 
    for j, strain in enumerate(strains): 
        path = rf'E:\K0StrainControlledCyclic\Dry_K0_FC0p25to0p25_{depth}m\Strain{strain}'

        N = 101

        # Get cyclic turns 
        os.chdir(path + r'\template')
        for line in open('continue_cyclic.in'):
            match = re.search('cyclicturns equal (\d+)', line)
            if match:
                cyclicturns = int(match.group(1))
                print(cyclicturns)


        # Load Data
        os.chdir(path + r'\merged_data')
        stress_data = pd.read_csv('stress_data.csv')

        # Adapt Data
        cycle_steps_max = np.arange(cyclicturns,cyclicturns*2*N, cyclicturns*2)
        cycle_steps_max = [round(val, -4) for val in cycle_steps_max]

        stress_xx_max = stress_data.stress_xx[stress_data['step_s'].isin(cycle_steps_max)].to_numpy()/1000
        stress_yy_max = stress_data.stress_zz[stress_data['step_s'].isin(cycle_steps_max)].to_numpy()/1000
        stress_zz_max = stress_data.stress_zz[stress_data['step_s'].isin(cycle_steps_max)].to_numpy()/1000
        ratio_max = stress_zz_max/stress_xx_max

        cycle_steps_min = np.arange(0+10000,cyclicturns*2*N+1, cyclicturns*2)
        cycle_steps_min = [round(val, -4) for val in cycle_steps_min]

        stress_xx_min = stress_data.stress_xx[stress_data['step_s'].isin(cycle_steps_min)].to_numpy()/1000
        stress_yy_min = stress_data.stress_zz[stress_data['step_s'].isin(cycle_steps_min)].to_numpy()/1000
        stress_zz_min = stress_data.stress_zz[stress_data['step_s'].isin(cycle_steps_min)].to_numpy()/1000
        ratio_min = stress_zz_min/stress_xx_min
        # =================================================================================================
        # Figure
        plt.figure(1, figsize=(12,7))
        plt.plot(np.arange(0,len(ratio_max),1), ratio_max, c = color_list[i], ls = ls_list[j], lw = 2, marker = '^', markevery = 5, mec = 'black')
        plt.plot(np.arange(0,len(ratio_min),1), ratio_min, c = color_list[i], ls = ls_list[j], lw = 2, marker = 'v', markevery = 5, mec = 'black')

ax = plt.gca()

plt.hlines(y = 1, xmin = -5, xmax = 105, ls = '--', color = 'black', lw =2)
plt.text(99,1.03, 'Isotropic line', horizontalalignment='right', fontsize = TxtS)
plt.xlim(-5, 105)
plt.ylim(0.25,2.25)

# Labels
plt.ylabel(r"Stress ratio $(\frac{\sigma'_{zz}}{\sigma'_{xx}})$", fontsize = LBF)
plt.xlabel('Cycle number (N)', fontsize = LBF)

plt.tick_params(axis='both', which='major', labelsize=TS)

plt.xlim(0,100)

# Legend
basecolor = 'gray'

# lg1:
line1 = mlines.Line2D([], [], color=basecolor, ls = ':', label='0.1%', lw = lw1)
line2 = mlines.Line2D([], [], color=basecolor, ls = '--', label='0.5%', lw = lw1)
line3 = mlines.Line2D([], [], color=basecolor, ls = '-', label='1%', lw = lw1)
lg1 = ax.legend(handles=[line1, line2, line3], fontsize = LGF, title = "$\epsilon_{zz}^{ampl}$:", title_fontsize=TF, loc='lower left', bbox_to_anchor=(1, 0.01))

# lg2:
patch1 = mpatches.Patch(color = color_list[0], label = '52 kPa')
patch2 = mpatches.Patch(color = color_list[1], label = '104 kPa')
patch3 = mpatches.Patch(color = color_list[2], label = '156 kPa')
patch4 = mpatches.Patch(color = color_list[3], label = '208 kPa')

lg2 = ax.legend(handles=[patch1, patch2, patch3, patch4], fontsize = LGF, title = "$\sigma'^0_{xx}$:", loc='upper left', bbox_to_anchor=(1, 1))

# lg3:
marker1 = mlines.Line2D([], [], color=basecolor, ls = ' ', marker = 'v', mec = 'black', label='Starting position')
marker2 = mlines.Line2D([], [], color=basecolor, ls = ' ', marker = '^', mec = 'black', label='Peak position')
lg3 = ax.legend(handles=[marker1, marker2], fontsize = LGF, loc='upper left')

ax.add_artist(lg1)
ax.add_artist(lg2)

plt.grid(which = 'minor', color = 'gray', ls = '--')
plt.grid(which = 'major', color = 'dimgray', ls = '-')

plt.subplots_adjust(right=0.85)
plt.show()