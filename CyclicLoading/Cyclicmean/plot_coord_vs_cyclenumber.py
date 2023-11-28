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

from basicFunctions.get_cyclicmean_data import get_cyclicmean_data
# ==============================================================================
# DEFINE DATASET
path = None
position = 0 
which_data = 'pav300_V2'
drive = 'E'
labellist = [
    '$q^{ampl}$ = 15kPa', 
    '$q^{ampl}$ = 20kPa', 
    '$q^{ampl}$ = 30kPa', 
    '$q^{ampl}$ = 60kPa', 
    '$q^{ampl}$ = 90kPa'
    ]
# ==============================================================================
# Define Plot Fontsizes
TF = 24     # Text font
LGF = 12   # Legend Font Size
LBF = 15    # Label Font Size
TS = 12     # Tick Size
lw1 = 2     # Line Width
# ==============================================================================

pathlist, colorlist = get_cyclicmean_data(which_data, drive)

# Calculating cycle length
time_step = 5.242309e-09
period = 0.25
cycle_length = int(period/(time_step))

plt.figure(figsize = (7,7))
for i, path in enumerate(pathlist):
    print(path)
    os.chdir(path)
    coord_data = pd.read_csv('coord_data.csv')
    step = coord_data.step_c.to_numpy()
    coord_number = coord_data.coord_number.to_numpy()

    plt.plot(step, coord_number, c = colorlist[i], label = labellist[i])

ax = plt.gca()
plt.xlim(0,50*cycle_length)
ax.set_xticks(np.arange(0,51*cycle_length,10*cycle_length))
ax.set_xticklabels(np.arange(0,51,10))
ax.xaxis.set_minor_locator(AutoMinorLocator(10))
plt.grid(which = 'major', color = 'gray')
plt.grid(which = 'minor', color = 'gray', ls = '--')
ax.tick_params(which = 'major', labelsize = TS)

plt.xlabel('Cycle Number', fontsize = LBF)
plt.ylabel('Coordination Number ($Z$)', fontsize = LBF)
plt.legend(loc = 'upper left', fontsize = LGF)
plt.show()
