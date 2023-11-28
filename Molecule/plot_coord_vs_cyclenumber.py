# Author: Tara Sassel 
# Date 30/12/22

# Script to plot the coodrination number vs the cycle number
# For a specific position 
# ==============================================================================

#  IMPORTS 
import os 
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)

# ==============================================================================
# DEFINE DATASET
path = r'E:\Molecules\CyclicMolecule\AR1p1_FC0p25_200_60_Trial128\merged_data'

# ==============================================================================
# Define Plot Fontsizes
TF = 24     # Text font
LGF = 12   # Legend Font Size
LBF = 15    # Label Font Size
TS = 12     # Tick Size
lw1 = 2     # Line Width
# ==============================================================================
print(path)
os.chdir(path)
coord_data = pd.read_csv('coord_data.csv')
step = coord_data.step_c.to_numpy()
coord_number = coord_data.coord_number.to_numpy()

# Calculating cycle length
time_step = 3.313644294808273e-09
period = 0.25
cycle_length = int(period/(time_step))

plt.figure(figsize = (7,7))
plt.plot(step, coord_number, c = 'forestgreen')

ax = plt.gca()
plt.xlim(0,5*cycle_length)
ax.set_xticks(np.arange(0,5*cycle_length,1*cycle_length))
ax.set_xticklabels(np.arange(0,5,1))
ax.xaxis.set_minor_locator(AutoMinorLocator(10))
plt.grid(which = 'major', color = 'gray')
plt.grid(which = 'minor', color = 'gray', ls = '--')
ax.tick_params(which = 'major', labelsize = TS)

plt.xlabel('Cycle Number', fontsize = LBF)
plt.ylabel('Coordination Number ($Z$)', fontsize = LBF)
plt.show()
