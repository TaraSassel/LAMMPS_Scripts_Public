# Author:   Tara Sassel
# Date:     27/03/23

# This scriptintends to reproduce a figure using my DEM data by Al Tarhouni and Hawlader (2023)
# Where you have the stress ratio tau_zx/sigma_z vs the axial strain (shear stress --> ratio tau_zx)

# Imports 
import os 
import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt 
from matplotlib.pyplot import cm

from cyclicStrainK0 import get_K0_info
from basicFunctions.get_strain import get_strain

# =================================================================================================
# Fontisze
LBF = 16    # Label Fontsize
TS = 12     # Ticksize
CBF = 14    # Colorbar Font

strainInfo = get_K0_info('E') # Drive Number example: 'E'
N = 101             # Number of cycles

# Define wanted dataset 
which_depth = 8               # 2, 4, 6 or 8m
which_strain_amplitude = 1      # 0.1, 0.5 or 1
which_friction_coefficient = 0.25  # 0.1, 0.15 or 0.25

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


stress_yy = stress_data.stress_yy.to_numpy().T
stress_zz = stress_data.stress_zz.to_numpy().T

# =================================================================================================
# Figure
fig = plt.figure(figsize = (7,7))
color_list = cm.bone(np.linspace(0, 1, N))

cycle_number_list = list(stress_data['cycle_number'].unique())
for i, number in enumerate(cycle_number_list):
    if number < N:
        print(number)
        cycle_data = stress_data[stress_data['cycle_number'] == number]
        plt.plot(cycle_data['stress_yy']/cycle_data['stress_zz'],cycle_data['strain_z'], c = color_list[i])

# Colorbar
sm = plt.cm.ScalarMappable(cmap=cm.bone, norm=plt.Normalize(vmin=0, vmax=N))
cb = plt.colorbar(sm)
cb.ax.tick_params(labelsize=TS)
cb.set_label('Cycle Number (N)', fontsize = CBF)

# Labels
plt.xlabel(r'$\frac{\sigma_y}{\sigma_z}$', fontsize = LBF)
plt.ylabel(r'$\epsilon_z$ [%]', fontsize = LBF)
plt.tick_params(axis='both', which='major', labelsize=TS)

plt.show()

