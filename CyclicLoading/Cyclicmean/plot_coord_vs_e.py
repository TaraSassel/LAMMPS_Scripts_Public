"""
Author: Tara Sassel
Date: 18/01/2023

This script shows both the coordination number against the void ratio
"""

# Importing 
import os 
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)

from basicFunctions.MechanicalCoordinationNumber import get_mechCoord

# ==============================================================================
# Defining Path
drive = 'E'
path_300_15 = rf'{drive}:\CyclicLoading\Cyclicmean\TX300_FC0p25to0p25_amp15\merged_data'
path_300_20 = rf'{drive}:\CyclicLoading\Cyclicmean\TX300_FC0p25to0p25_amp20\merged_data'
path_300_30 = rf'{drive}:\CyclicLoading\Cyclicmean\TX300_FC0p25to0p25_amp30\merged_data'
path_300_60 = rf'{drive}:\CyclicLoading\Cyclicmean\TX300_FC0p25to0p25_amp60\merged_data'
path_300_90 = rf'{drive}:\CyclicLoading\Cyclicmean\TX300_FC0p25to0p25_amp90\merged_data'

path_list = [path_300_15, path_300_20, path_300_30, path_300_60, path_300_90]

# Defining Colors
color_list = ['#f0f9e8', '#bae4bc', '#7bccc4', '#43a2ca', '#0868ac']

# Defining Labels
label_list = [
    '$q^{ampl}$ = 15kPa',
    '$q^{ampl}$ = 20kPa',
    '$q^{ampl}$ = 30kPa',
    '$q^{ampl}$ = 60kPa',
    '$q^{ampl}$ = 90kPa']

# Definig Plot Fontsizes
TF = 24     # Text font
LGF = 10   # Legend Font Size
LBF = 15    # Label Font Size
TS = 12     # Tick Size
lw1 = 2     # Line Width

# ==============================================================================
# COORDINATION NUMBER STARTING POS
# Calculating cycle length
time_step = 5.242309e-09
period = 0.25
cycle_length = int(period/(time_step))

index_length = int(cycle_length*51/10000)

plt.figure( figsize = (7,7)) # Initiating Figure
for i, path in enumerate(path_list):
    os.chdir(path)
    # loading data
    coord_data = pd.read_csv('coord_data.csv')
    void_data = pd.read_csv('void_data.csv')

    # joining data on step
    coord_data = coord_data.rename(columns={"step_c":"step"})
    void_data = void_data.rename(columns={"step_v":"step"})

    all_data  = pd.merge(coord_data, void_data, on ='step')
    all_data = all_data.dropna()

    coord_number = all_data.coord_number.to_numpy()
    void_ratio = all_data.void_ratio.to_numpy()

    plt.plot(
        void_ratio[:index_length],
        coord_number[:index_length], 
        c = color_list[i], 
        ls = '-',
        lw = lw1, 
        label = label_list[i],
        zorder=(len(path_list)+1)-i)

# Adjusting axis 
ax = plt.gca()

# Legend 
custom_lines1 = [Line2D([0], [0], c = color_list[0], lw=4, label = label_list[0]),
                Line2D([0], [0], c = color_list[1], lw=4, label = label_list[1]),
                Line2D([0], [0], c = color_list[2], lw=4, label = label_list[2]),
                Line2D([0], [0], c = color_list[3], lw=4, label = label_list[3]),
                Line2D([0], [0], c = color_list[4], lw=4, label = label_list[4])]
lg1 = ax.legend(handles=custom_lines1 , loc='upper right', fontsize = LGF)

# Labels 
plt.xlabel('Void ratio ($e$)', fontsize = LBF)
plt.ylabel(r'Coordination number $(\bar C_N)$', fontsize = LBF)

ax.tick_params(axis='both', which='major', labelsize=TS)
plt.tight_layout()

plt.grid(which = 'major', color = 'gray')
plt.grid(which = 'minor', color = 'gray', ls = '--')
plt.show()


