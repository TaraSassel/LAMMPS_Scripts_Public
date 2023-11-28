
"""
Author: Tara Sassel
Date: 24/10/2022

Script to define mechanical coordination number for cylcicmean 300
"""
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D

from basicFunctions.MechanicalCoordinationNumber import get_mechCoord

# ==============================================================================
# Defining Path
drive = "E" # for example "E"
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
    'ampl = 15kPa',
    'amp = 20kPa',
    'ampl = 30kPa',
    'ampl = 60kPa',
    'ampl = 90kPa']

# Definig Plot Fontsizes
TF = 24     # Text font
LGF = 12   # Legend Font Size
LBF = 15    # Label Font Size
TS = 12     # Tick Size
lw1 = 2     # Line Width

# ==============================================================================
plt.figure( figsize = (7,7)) # Initiating Figure

for p, path in enumerate(path_list):
    os.chdir(path)

    # Mechanical Coordination Number
    mech_coord = get_mechCoord(
        path + r'\SortedData\2_NeutralPos\connectivity',
        ['id','diameter','coord'])

    # Plotting
    plt.plot(
        np.arange(0,50,1),
        mech_coord.mechanical_coord[:50],
        c = color_list[p],
        lw = lw1,
        label = label_list[p],
        marker = 'o',
        mec = 'k')

plt.legend(loc = 'upper left', fontsize = LGF)
plt.xlabel('Cycle number (N)', fontsize = LBF)
plt.ylabel(r'Mean mechanical coordination number ($\bar C*_N$)', fontsize = LBF)
plt.gca().tick_params(axis='both', which='major', labelsize=TS)
plt.tight_layout()
plt.grid()
plt.show()
