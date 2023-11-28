"""
Author: Tara Sassel
Date: 28/03/2023
This strain plots the stress vs cycle number 
"""

# Imports 
import os 
import numpy as np
import pandas as pd
import seaborn as sns 
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.colors

from cyclicStrain import get_strain_info
from basicFunctions.get_strain import get_strain

# =================================================================================================
strainInfo = get_strain_info(None) # Drive Number example: 'E'
N = 101             # Number of cycles

# Fontisze
LBF = 18    # Label Fontsize
TS = 16     # Ticksize
LGF = 16    # Colorbar Font

# Define wanted dataset 
which_iso_stress = None             # 100, 200 or 300
which_strain_amplitude = None       # 0.1, 0.5 or 1
which_friction_coefficient = None   # 0.1, 0.15 or 0.25

# =================================================================================================
# change directory to selected data set
wanted_data = strainInfo[
    (strainInfo.iso_stress == which_iso_stress) &\
    (strainInfo.strain_amplitude == which_strain_amplitude) &\
    (strainInfo.friction_coefficient == which_friction_coefficient)]

path_list = list(wanted_data.path)
cyclic_turns = list(wanted_data.cyclic_turns)
print(cyclic_turns)
os.chdir(path_list[0] + r'/merged_data')

# Load Data
coord_data = pd.read_csv('coord_data.csv')

# Adapt Data
coord_data['cycle_number'] = coord_data.step_c/(cyclic_turns[0]*2)
coord_data['cycle_number'] = coord_data['cycle_number'].round()

# =================================================================================================
# Figure
fig = plt.figure(figsize = (12,5))

plt.plot(coord_data['step_c'], coord_data['coord_number'], c = 'navy',lw = 2)

plt.xlim(0,cyclic_turns[0]*2*100)

# Labels
plt.ylabel(r"Coordination number ($\bar{C}_N$)", fontsize = LBF)
plt.xlabel('Cycle Number (N)', fontsize = LBF)
plt.tick_params(axis='both', which='major', labelsize=TS)

# Grid and minor ticks
ticks_x = np.arange(0, cyclic_turns[0]*2*101,cyclic_turns[0]*2*10)
labels_x = np.arange(0,101,10)
plt.xticks(ticks_x, labels_x)


#plt.gca().yaxis.set_minor_locator(ticker.MultipleLocator(10))
#plt.gca().yaxis.set_major_locator(ticker.MultipleLocator(50))
plt.grid(which = 'minor', color = 'gray', ls = '--')
plt.grid(which = 'major', color = 'dimgray', ls = '-')
plt.show()