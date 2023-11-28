"""
Author: Tara Sassel
Date: 12/01/2023
This strain plots the stress strain loops for the K0 strain controlled cyclic data 
"""

# Imports 
import os 
import numpy as np
import pandas as pd
import seaborn as sns 
import matplotlib.colors
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
import matplotlib.ticker as ticker

from cyclicStrainK0 import get_K0_info
from basicFunctions.get_strain import get_strain

# =================================================================================================
strainInfo =  get_K0_info('E') # Drive Number example: 'E'
N = 101             # Number of cycles

# Fontisze
LBF = 16    # Label Fontsize
TS = 12     # Ticksize
CBF = 14    # Colorbar Font

# Define wanted dataset 
which_depth = 4             # 100, 200 or 300
which_strain_amplitude = 1       # 0.1, 0.5 or 1
which_friction_coefficient = 0.25   # 0.1, 0.15 or 0.25

# =================================================================================================
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

# Adapt Data
stress_data['strain_z'] = get_strain(stress_data['length_z'])
stress_data['cycle_number'] = stress_data.step_s/(cyclic_turns[0]*2)
stress_data['cycle_number'] = stress_data['cycle_number'].round()

# =================================================================================================
# Figure
fig = plt.figure(figsize = (7,7))

custom_cmap = matplotlib.colors.LinearSegmentedColormap.from_list("custom", ["#E9E9E9","#000000"])
color_list = custom_cmap(np.linspace(0, 1, N))

plt.hlines(y = 1, xmin = -0.1, xmax = 1.1, ls = '--', color = 'black')

cycle_number_list = list(stress_data['cycle_number'].unique())
for i, number in enumerate(cycle_number_list):
    if number < N:
        print(number)
        cycle_data = stress_data[stress_data['cycle_number'] == number]
        stress_ratio = cycle_data.stress_yy.to_numpy()/cycle_data.stress_zz.to_numpy()
        s_xx = cycle_data.stress_xx.to_numpy()
        s_yy = cycle_data.stress_yy.to_numpy()
        s_zz = cycle_data.stress_zz.to_numpy()
        
        plt.plot(cycle_data['strain_z'],s_zz/s_xx, c = color_list[i])

ax = plt.gca()

ymin = 0.25
ymax = 2.25
yint = ymax-ymin
plt.xlim(-0.1, 1.1)
plt.ylim(ymin, ymax)

def get_loc(pwanted)->float:
     "To get positions for annotations"
     ytag = (pwanted-ymin)/yint
     return ytag

# arrow towards active
ax.annotate('', xy=(-0.12, get_loc(1)), xycoords='axes fraction', xytext=(-0.12, get_loc(0.41)), 
            arrowprops=dict(arrowstyle="<-", color='indianred'))

plt.text(-0.14, get_loc(0.5), 'Towards active', horizontalalignment='center',
     verticalalignment='bottom', rotation = 'vertical', transform=ax.transAxes, c = 'indianred')

# arrow towards passive
ax.annotate('', xy=(-0.12, get_loc(1)), xycoords='axes fraction', xytext=(-0.12, get_loc(2.186)), 
            arrowprops=dict(arrowstyle="<-", color='forestgreen'))

plt.text(-0.14, get_loc(2.1), 'Towards passive', horizontalalignment='center',
     verticalalignment='top', rotation = 'vertical', transform=ax.transAxes, c = 'forestgreen')

# isotropic label 
plt.text(-0.3, get_loc(1), 'Isotropic', horizontalalignment='left',
     verticalalignment='center', rotation = 'horizontal', transform=ax.transAxes, c = 'black')


# Colorbar
sm = plt.cm.ScalarMappable(cmap=custom_cmap, norm=plt.Normalize(vmin=0, vmax=N))
cb = plt.colorbar(sm)
cb.ax.tick_params(labelsize=TS)
cb.set_label('Cycle Number (N)', fontsize = CBF)

# Labels
plt.ylabel(r"Stress ratio $(\frac{\sigma'_{zz}}{\sigma'_{xx}})$", fontsize = LBF)
plt.xlabel('Strain [%]', fontsize = LBF)
#ax.yaxis.labelpad = 20
ax.yaxis.set_label_coords(-.2, .6)
plt.tick_params(axis='both', which='major', labelsize=TS)

# Grid and minor ticks
#plt.gca().yaxis.set_minor_locator(ticker.MultipleLocator(10))
#plt.gca().yaxis.set_major_locator(ticker.MultipleLocator(50))
plt.grid(which = 'minor', color = 'gray', ls = '--')
plt.grid(which = 'major', color = 'dimgray', ls = '-')
plt.tight_layout()
plt.show()