"""
Author: Tara Sassel
Date: 02/01/2023

This script shows both the mechanical coordination number and the coordination number
This is for a specific position and can be define below
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
LBF = 18    # Label Font Size
TS = 14     # Tick Size
lw1 = 2     # Line Width

# ==============================================================================
# MEAN MECHANICAL COORDINATION NUMBER 
plt.figure( figsize = (12,7)) # Initiating Figure

for p, path in enumerate(path_list):
    os.chdir(path)

    # Mechanical Coordination Number
    mech_coord = get_mechCoord(
        path + r'\SortedData\0_StartingPos\connectivity',
        ['id','diameter','coord'])

    # Plotting
    plt.plot(
        np.arange(0,50,1),
        mech_coord.mechanical_coord[:50],
        c = color_list[p],
        lw = lw1,
        label = label_list[p],
        ls = '--',
        marker = '',
        mec = 'k')

# ==============================================================================
# COORDINATION NUMBER STARTING POS
# Calculating cycle length
time_step = 5.242309e-09
period = 0.25
cycle_length = int(period/(time_step))

for i, path in enumerate(path_list):
    os.chdir(path)
    coord_data = pd.read_csv('coord_data.csv')
    step = coord_data.step_c.to_numpy()
    coord_number = coord_data.coord_number.to_numpy()

    coord_array =  np.zeros(51,)
    coord_max =  np.zeros(51,)
    coord_min =  np.zeros(51,)
    cycle_number = np.arange(0,51,1)
    for cycle in cycle_number:
        wanted_step = np.float64(cycle) * cycle_length
        step_index = np.argmax(step>wanted_step)
        step_max = np.argmax(step>wanted_step + cycle_length*1/4)
        step_min = np.argmax(step>wanted_step + 3*cycle_length/4)
        coord_array[cycle] = coord_number[step_index]
        coord_max[cycle] = coord_number[step_max]
        coord_min[cycle] = coord_number[step_min]

        if cycle == 50:
            coordToCycle50 = coord_number[:step_index]
            stepsToCycle50 = step[0:step_index]
            stepsConvertCycles = stepsToCycle50*50/stepsToCycle50[-1]

    plt.plot(
        cycle_number, 
        coord_array, 
        c = color_list[i], 
        ls = ':',
        lw = lw1, 
        label = label_list[i])
    
    plt.plot(
        stepsConvertCycles, 
        coordToCycle50, 
        c = color_list[i], 
        ls = '-',
        lw = 1, 
        label = label_list[i])

    ax = plt.gca()
    if i == 4:
        ax.fill_between(cycle_number, coord_max+0.01, coord_min-0.01, facecolor=color_list[i], alpha=0.3)
    else : 
        ax.fill_between(cycle_number, coord_max, coord_min, facecolor=color_list[i], alpha=0.3)
# Figure adjustments 
# Legend 
custom_lines1 = [Line2D([0], [0], c = color_list[0], lw=4, label = label_list[0]),
                Line2D([0], [0], c = color_list[1], lw=4, label = label_list[1]),
                Line2D([0], [0], c = color_list[2], lw=4, label = label_list[2]),
                Line2D([0], [0], c = color_list[3], lw=4, label = label_list[3]),
                Line2D([0], [0], c = color_list[4], lw=4, label = label_list[4])]

custom_lines2 = [Line2D([0], [0], c = 'black', ls = '--', lw=2, label = r'Mechanical coordination number ($\bar C^*_N$) at position 0'),
                Line2D([0], [0], c = 'black', ls = ':', lw=2, label = r'Coordination number ($\bar C_N$) at position 0'),
                Line2D([0], [0], c = 'black', ls = '-', lw=1, label = r'Coordination number ($\bar C_N$)')]

lg1 = ax.legend(handles=custom_lines1 , loc='upper right', fontsize = LGF)
lg2 = ax.legend(handles=custom_lines2 , loc='upper left', fontsize = LGF+5)
ax.add_artist(lg1)

# Labels 
plt.xlabel('Cycle number (N)', fontsize = LBF)
plt.ylabel(r'$\bar C^*_N$ and $\bar C_N$', fontsize = LBF)
ax.tick_params(axis='both', which='major', labelsize=TS)
plt.xlim(0,50)
plt.ylim(4.2,5.4)
plt.tight_layout()
ax.xaxis.set_minor_locator(AutoMinorLocator(10))
plt.grid(which = 'major', color = 'gray')
plt.grid(which = 'minor', color = 'gray', ls = '--')
plt.show()