# Author: Tara Sassel 
# Date: 29/02/23

# This script is to plot the number of contacts against cycle number 

# Imports
import re
import os
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
import matplotlib.lines as mlines
import matplotlib.patches as mpatches

from basicFunctions.get_mechCoord import get_mechCoord
from basicFunctions.get_strainInfo import get_strain_info

# =================================================================================================
strainInfo = get_strain_info('E')   # Drive Number example: 'E'
N = 102                             # Number of cycles
pos = 'Starting_Position'             # Select Name for folder # Position_Loaded, Position_Unoaded

# Fontisze
LBF = 16    # Label Fontsize
TS = 16     # Ticksize
LGF = 12    # Legend font
TF = 14     # Legend title font
lw1 = 2     # Line width 

# Define wanted dataset 
stresses = [100, 200, 300]             
amplitudes = [0.1, 0.5, 1]       
which_friction_coefficient = 0.25   # 0.1, 0.15 or 0.25
color_list = ['darkgreen','darkgreen','darkgreen', 'navy','navy','navy','maroon','maroon','maroon']
ls_list = [':', '--', '-']*3

fig = plt.figure(figsize = (12,7))
k = 0 # To enumerate trough colors and line
for which_iso_stress in stresses:
    for which_strain_amplitude in amplitudes: 
        # change directory to selected data set
        wanted_data = strainInfo[
            (strainInfo.iso_stress == which_iso_stress) &\
            (strainInfo.strain_amplitude == which_strain_amplitude) &\
            (strainInfo.friction_coefficient == which_friction_coefficient)]

        path_list = list(wanted_data.path)
        path = path_list[0]
        print(path)

        # Get cyclic turns 
        os.chdir(path + r'\merged_data')
        
        ft_df = pd.read_csv("deviatoricFabric.csv")


        plt.plot(ft_df.cycle, ft_df.ftd, c = color_list[k], ls = ls_list[k], lw = lw1)
        k += 1

# Figure labeling 
ax = plt.gca()

#Limits
plt.xlim(0,)
plt.ylim(0,)

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

lg2 = ax.legend(handles=[patch1, patch2, patch3], loc = 'upper left', fontsize = LGF, title = "$\sigma'_0$:", title_fontsize=TF)

ax.add_artist(lg1)

plt.ylabel(r"Deviatoric fabric tensor ($\Phi_d$)", fontsize = LBF)
plt.xlabel('Cycle number (N)', fontsize = LBF)
plt.tick_params(axis='both', which='major', labelsize=TS)
plt.grid(which = 'major', color = 'dimgray', ls = '-')
plt.xlim(0,100)
plt.show()


