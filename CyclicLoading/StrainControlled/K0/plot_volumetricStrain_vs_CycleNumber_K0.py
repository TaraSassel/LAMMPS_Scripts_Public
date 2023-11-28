"""
Author: Tara Sassel
Date: 25/01/2023

"""


# Imports 
import os 
import numpy as np
import pandas as pd
import seaborn as sns 
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import matplotlib.patches as mpatches

from cyclicStrainK0 import get_K0_info
from basicFunctions.get_strain import get_strain

# =================================================================================================
strainInfo = get_K0_info('E') # Drive Number example: 'E'
N = 101             # Number of cycles
print(strainInfo.head(12))
# Fontisze
LBF = 14    # Label Fontsize
LGF = 10    # Legend Fontsize
TS = 12     # Ticksize
CBF = 14    # Colorbar Font
lw1 = 2     # Linewidth

# Define wanted dataset 
depth_list = [2,4,6,8]
strain_list = [0.1, 0.5, 1] 
fc_list = [0.25]
color_list = ['lightgreen', 'lightsteelblue','mediumpurple', 'lightcoral']
#fc_list = [0.15, 0.25]
# =================================================================================================
for which_depth in depth_list:
    print(which_depth)
    for which_strain_amplitude in strain_list:
        print("\t" +str(which_strain_amplitude))
        for which_friction_coefficient in fc_list:
            print("\t" + "\t" + str(which_friction_coefficient))
            # change directory to selected data set
            wanted_data = strainInfo[
                (strainInfo.depth == which_depth) &\
                (strainInfo.strain_amplitude == which_strain_amplitude) &\
                (strainInfo.friction_coefficient == which_friction_coefficient)]

            path_list = list(wanted_data.path)
            cyclic_turns = list(wanted_data.cyclic_turns)

            os.chdir(path_list[0] + r'/merged_data')

            # Load Data
            stress_data = pd.read_csv('stress_data.csv')

            # Calculate Volumetric Strain 
            length_x = stress_data.length_x.to_numpy().T
            length_y = stress_data.length_y.to_numpy().T
            length_z = stress_data.length_z.to_numpy().T

            lengthx0 = wanted_data.xdim.to_numpy()[0]
            lengthy0 = wanted_data.ydim.to_numpy()[0]
            lengthz0 = wanted_data.zdim.to_numpy()[0]

            xstrain = (lengthx0 - length_x)*100/lengthx0
            ystrain = (lengthy0 - length_y)*100/lengthy0
            zstrain = (lengthz0 - length_z)*100/lengthz0

            eps_v = (xstrain + ystrain + zstrain)

            stress_data['eps_v'] = eps_v 
            step_interval = int(stress_data.step_s[1] - stress_data.step_s[0])

            # Get wanted steps to the nearest step_interval (10000)
            cyclic_turns = wanted_data.cyclic_turns.to_numpy()[0]
            cycle_length = cyclic_turns*2
            wanted_steps = np.arange(cyclic_turns, cyclic_turns + cycle_length*N,cycle_length)
            steps_df = pd.DataFrame(wanted_steps, columns=['steps'])
            wanted_steps_round = (steps_df.steps / step_interval).astype(np.int64) * step_interval
            wanted_steps_round = wanted_steps_round.to_numpy().T

            # color 
            c = color_list[int(which_depth/2-1)]
            # Line style 
            if which_strain_amplitude == 0.1:
                ls1 = ':'
            if which_strain_amplitude == 0.5:
                ls1 = '--'
            if which_strain_amplitude == 1:
                ls1 = '-'        

                # Marker 
            if which_friction_coefficient == 0.15:
                m1 = 'o'
            else:
                m1 = ' '
                
            # Get only rows with wanted steps
            wanted_stress_data = stress_data.loc[stress_data['step_s'].isin(wanted_steps_round)]
            wanted_eps_v = wanted_stress_data.eps_v.to_numpy().T

            plt.plot(wanted_eps_v, color = c, ls = ls1, lw = lw1, marker= m1, markevery = 10)

plt.xlim(0, )
plt.ylim(0, 6.5)
plt.xlabel('Cycle number (N)', fontsize = LBF)
plt.ylabel('Volumetric strain ($\epsilon_v$) [%]', fontsize = LBF)
plt.tick_params(axis='both', which='major', labelsize=TS)

ax = plt.gca()

# Hide the right and top spines
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

# make arrows
ax.plot((1), (0), ls="", marker=">", ms=10, color="k",
        transform=ax.get_yaxis_transform(), clip_on=False)
ax.plot((0), (1), ls="", marker="^", ms=10, color="k",
        transform=ax.get_xaxis_transform(), clip_on=False)

# Legend
basecolor = 'gray'

# lg1:
line1 = mlines.Line2D([], [], color=basecolor, ls = ':', label='0.1%', lw = lw1)
line2 = mlines.Line2D([], [], color=basecolor, ls = '--', label='0.5%', lw = lw1)
line3 = mlines.Line2D([], [], color=basecolor, ls = '-', label='1%', lw = lw1)
lg1 = ax.legend(handles=[line1, line2, line3], loc = 'lower right', fontsize = LGF, title = "$\epsilon_{zz}^{ampl}$:")

# lg2:
patch1 = mpatches.Patch(color = 'lightgreen', label = '2 m')
patch2 = mpatches.Patch(color = 'lightsteelblue', label = '4 m')
patch3 = mpatches.Patch(color = 'mediumpurple', label = '6 m')
patch4 = mpatches.Patch(color = 'lightcoral', label = '8 m')

lg2 = ax.legend(handles=[patch1, patch2, patch3, patch4], loc = 'upper left', fontsize = LGF, title = "Depth:")

ax.add_artist(lg1)
#ax.add_artist(lg2)

plt.tight_layout()
plt.show() 