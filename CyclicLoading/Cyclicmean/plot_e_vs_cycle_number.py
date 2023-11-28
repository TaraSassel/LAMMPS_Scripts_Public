"""
Author: Tara Sassel
Date: 28/11/2022

In this script the volumetric strain
This was inspired by Lopez-Querol and Coop (2012)
Where the specific volume was plotted against
"""
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

from basicFunctions.get_cyclicmean_data import get_cyclicmean_data
# ==============================================================================
# Define Plot Fontsizes
TF = 24     # Text font
LGF = 12   # Legend Font Size
LBF = 20    # Label Font Size
TS = 16     # Tick Size
lw1 = 2     # Line Width
# ==============================================================================

# Path and color list
path_list, color_list = get_cyclicmean_data('all', 'E')
label_list = [
    "$p'^{av}$ = 100kPa $q^{ampl}$ = 5kPa",
    "$p'^{av}$ = 100kPa $q^{ampl}$ = 10kPa",
    "$p'^{av}$ = 100kPa $q^{ampl}$ = 20kPa",
    "$p'^{av}$ = 100kPa $q^{ampl}$ = 30kPa",
    "$p'^{av}$ = 200kPa $q^{ampl}$ = 10kPa",
    "$p'^{av}$ = 200kPa $q^{ampl}$ = 20kPa",
    "$p'^{av}$ = 200kPa $q^{ampl}$ = 40kPa",
    "$p'^{av}$ = 200kPa $q^{ampl}$ = 60kPa",
    "$p'^{av}$ = 300kPa $q^{ampl}$ = 15kPa",
    "$p'^{av}$ = 300kPa $q^{ampl}$ = 30kPa",
    "$p'^{av}$ = 300kPa $q^{ampl}$ = 60kPa",
    "$p'^{av}$ = 300kPa $q^{ampl}$ = 90kPa"]
# Calculating cycle length
time_step = 5.242309e-09
period = 0.25
cycle_length = int(period/(time_step))

plt.figure(figsize = (10,9))
for i, path in enumerate(path_list):
    os.chdir(path)
    print(path)
    print(color_list[i])
    # Loading data
    void_data = pd.read_csv("void_data.csv")
    step_number = void_data.step_v.to_numpy().T
    void_ratio = void_data.void_ratio.to_numpy().T

    if i == 0 or i == 4 or i == 8:
        plt.plot(
            step_number,
            void_ratio,
            color = color_list[i+1],
            label = label_list[i],
            lw = 2,
            ls = '--'
            )

    else: 
        plt.plot(
            step_number,
            void_ratio,
            color = color_list[i],
            label = label_list[i],
            lw = 2
            )

ax = plt.gca()

# Adjusting ticks
plt.xticks(np.arange(0,cycle_length*51,cycle_length*10), np.arange(0,51,10))
minorLocator = MultipleLocator(cycle_length)
ax.xaxis.set_minor_locator(minorLocator)

# Adjusting axis
plt.xlim(0,cycle_length*50)
# plt.ylim(0.625, )
ax.tick_params(which = 'major', labelsize = TS)

# Label
plt.xlabel("Cycle number ($N$)", fontsize = LBF)
plt.ylabel("Void ratio ($e$)", fontsize = LBF)

# Showing grid
plt.grid(which = 'minor', ls = '--')
plt.grid()


plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol = 3, fontsize = LGF)

plt.tight_layout()
plt.show()
