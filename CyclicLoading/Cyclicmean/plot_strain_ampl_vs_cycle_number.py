"""
Author: Tara Sassel
Date: 29/11/2022

"""
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

from basicFunctions.get_strain import get_strain
from basicFunctions.get_cyclicmean_data import get_cyclicmean_data
# ==============================================================================
# Define Plot Fontsizes
TF = 24     # Text font
LGF = 12   # Legend Font Size
LBF = 16   # Label Font Size
TS = 12     # Tick Size
lw1 = 2     # Line Width
# ==============================================================================
# Labels
label_list = [
    "$q^{ampl}$ = 15kPa",
    "$q^{ampl}$ = 20kPa",
    "$q^{ampl}$ = 30kPa",
    "$q^{ampl}$ = 60kPa",
    "$q^{ampl}$ = 90kPa"
    ]
# Cycle Length
time_step = 5.242309e-09
period = 0.25
cycle_length = int(period/(time_step))
cycle_idx_length = np.round(cycle_length/10000)
pos_idx_length = np.round(cycle_length/(10000*4))
cycle_number = np.arange(0,51,1)

# List with position indexes
l_pos_list = np.arange(pos_idx_length,cycle_idx_length*51+pos_idx_length,cycle_idx_length)
l_pos_list = l_pos_list.astype(int)

u_pos_list = np.arange(pos_idx_length*3,cycle_idx_length*51+pos_idx_length*3,cycle_idx_length)
u_pos_list = u_pos_list.astype(int)

# Loading Data
path_list, color_list = get_cyclicmean_data("pav300_V2","F")
for i, path in enumerate(path_list):
    os.chdir(path)
    stress_data = pd.read_csv("stress_data.csv")

    # Calculating strain amplitude
    length_z = stress_data.length_z.to_numpy().T
    strain_z = get_strain(length_z)
    strain_ampl = strain_z[l_pos_list] - strain_z[u_pos_list]

    # Figure
    plt.plot(
        cycle_number,
        strain_ampl,
        c = color_list[i],
        marker = 'o',
        mec = 'black',
        lw = 2,
        label = label_list[i],
        )

ax = plt.gca()
ax.set_yscale('log')
minorLocator = MultipleLocator(1)
ax.xaxis.set_minor_locator(minorLocator)
ax.tick_params(which = "major", labelsize = TS)
ax.set_xlabel("Cycle number (N)", fontsize = LBF)
ax.set_ylabel("Axial strain amplitude ($\epsilon_{zz}^{ampl}$)[%]", fontsize = LBF)
plt.legend(loc="upper right", fontsize = LGF)
plt.grid(which = 'minor', ls = '--')
plt.grid()
plt.tight_layout()
plt.show()
