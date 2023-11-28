"""
Author: Tara Sassel
Date: 14/12/2022
This strain plots the stress strain loops for the strain controlled cyclic data 
"""

# Imports 
import os 
import numpy as np
import pandas as pd
import seaborn as sns 
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
import matplotlib.ticker as ticker
import matplotlib.colors

from cyclicStrain import get_strain_info
from basicFunctions.get_strain import get_strain

# =================================================================================================
strainInfo = get_strain_info("E") # Drive Number example: 'E'
N = 101             # Number of cycles

# Fontisze
LBF = 18    # Label Fontsize
TS = 16     # Ticksize
CBF = 18    # Colorbar Font

# Define wanted dataset 
which_iso_stress = 300             # 100, 200 or 300
which_strain_amplitude = 1       # 0.1, 0.5 or 1
which_friction_coefficient = 0.25   # 0.1, 0.15 or 0.25

# =================================================================================================
# change directory to selected data set
wanted_data = strainInfo[
    (strainInfo.iso_stress == which_iso_stress) &\
    (strainInfo.strain_amplitude == which_strain_amplitude) &\
    (strainInfo.friction_coefficient == which_friction_coefficient)]

path_list = list(wanted_data.path)
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
fig = plt.figure(figsize = (10,5))

custom_cmap = matplotlib.colors.LinearSegmentedColormap.from_list("custom", ["#d9f3ff","#4c72b9", "#002a78"])
color_list = custom_cmap(np.linspace(0, 1, N))

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

plt.plot(cycle_number_list[0:101],G[0:101], c = "black", lw = 2)

# Labels
plt.ylabel(r"Cyclic stiffness ($G_{cyc}$) [$\frac{kPa}{mm}$]", fontsize = LBF)
plt.xlabel('Cycle number (N)', fontsize = LBF)
plt.xlim(0,100)
plt.tick_params(axis='both', which='major', labelsize=TS)

# Grid and minor ticks

plt.grid(which = 'minor', color = 'gray', ls = '--')
plt.grid(which = 'major', color = 'dimgray', ls = '-')
plt.tight_layout()
plt.show()