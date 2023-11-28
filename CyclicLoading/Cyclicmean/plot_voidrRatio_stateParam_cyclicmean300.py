"""
Author: Tara Sassel
Date: 24/10/2022

Collecting State Parameter at specific cycle numbers
"""
# Imporing Libraries
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ==============================================================================
# Defining Path
path_300_15 = r'F:\CyclicLoading\Cyclicmean\TX300_FC0p25to0p25_amp15\merged_data'
path_300_20 = r'F:\CyclicLoading\Cyclicmean\TX300_FC0p25to0p25_amp20\merged_data'
path_300_30 = r'F:\CyclicLoading\Cyclicmean\TX300_FC0p25to0p25_amp30\merged_data'
path_300_60 = r'F:\CyclicLoading\Cyclicmean\TX300_FC0p25to0p25_amp60\merged_data'
path_300_90 = r'F:\CyclicLoading\Cyclicmean\TX300_FC0p25to0p25_amp90\merged_data'

path_list = [path_300_15, path_300_20, path_300_30, path_300_60, path_300_90]

# Defining Colors
color_list = ['#f0f9e8', '#bae4bc', '#7bccc4', '#43a2ca', '#0868ac']

# Defining Labels
label_list = [
    'ampl = 15kPa',
    'ampl = 30kPa',
    'ampl = 30kPa',
    'ampl = 60kPa',
    'ampl = 90kPa']

# Define Plot Fontsizes
TF = 24     # Text font
LGF = 12   # Legend Font Size
LBF = 15    # Label Font Size
TS = 12     # Tick Size
lw1 = 2     # Line Width
ms1 = 10    # Marker Size

# ==============================================================================
# Figure Critical State
plt.figure(1, figsize = (10,10))

# Data points from Huang et al. (2014)
vr1 = 0.588
s1 = -0.0414
vr2 = 0.606
s2 = -0.0245
vr3 = 0.646
s3 = 0.0171

state_params = [s1,s2,s3]
voids = [vr1, vr2, vr3]

# Best fit line
a, b = np.polyfit(voids,state_params, 1)
x = np.arange(0.58,0.68,0.01)
plt.plot(
    x,
    a*x+b,
    color = 'k',
    label = f'$\psi = {a:.2f}*e+{b:.2f}$',
    zorder = 3)

# Huangs data points
plt.plot(
    voids,
    state_params,
    color = 'red',
    ls = '',
    marker = 'o',
    ms = 10,
    label = f'Huange et al. (2014)',
    zorder = 2)

# Labels
plt.xlabel('Void Ratio (e)', fontsize = LBF)
plt.ylabel('State Parameter $(\psi)$', fontsize = LBF)

# ==============================================================================
# Calculating cycle length
time_step = 5.242309e-09
period = 0.25
cycle_length = int(period/(time_step))

cycle_numbers = [0,1,2,3,4,5,10,20,30,40,50]
wanted_cycles = [0,1,2,3,4,5,10,20,30,40,50]
wanted_steps = [cycle*cycle_length for cycle in wanted_cycles]

# ==============================================================================
for p, path in enumerate(path_list):
    print(path)
    os.chdir(path)
    void_data = pd.read_csv('void_data.csv')
    step_v, void_ratio = void_data.to_numpy().T

    # Collecting voids ratio at start of cycle for wanted_cycles
    print(len(wanted_steps))
    index_list = []
    for step in wanted_steps:
        print(step)
        index_list.append(np.argmax(step_v >= step))
    wanted_void_ratio = void_ratio[index_list]
    wanted_state_param = a*wanted_void_ratio+b
    # ==========================================================================
    # Figure 1 State Parameter vs void ratio
    plt.figure(1, figsize = (10,10))
    plt.plot(
        wanted_void_ratio,
        wanted_state_param,
        color = color_list[p],
        ls = '', ms = 7,
        marker = 's', mec = 'k',
        label = label_list[p],
        zorder = 1)

    # Figure 2 void ratio vs cycle number
    plt.figure(2, figsize = (10,10))
    plt.plot(
        wanted_cycles,
        wanted_void_ratio,
        ls = '',
        marker = 's',
        color = color_list[p],
        mec = 'k',
        ms = ms1,
        label = label_list[p])

    # Figure 3 State Parameter vs cycle number
    plt.figure(3, figsize = (10,10))
    plt.plot(
        wanted_cycles,
        wanted_state_param,
        ls = '',
        marker = 's',
        color = color_list[p],
        mec = 'k',
        ms = ms1,
        label = label_list[p])

# ==============================================================================
# Fine tuning figures
plt.figure(3, figsize = (10,10))
plt.xlim(0)
plt.legend(loc = 'lower left', fontsize = LGF)
plt.xlabel('Cycle Number (N)', fontsize = LBF)
plt.ylabel('State Parameter ($\psi$)', fontsize = LBF)
plt.gca().tick_params(which='major', labelsize=TS)
plt.grid(ls=':', lw=1, c='gray')

plt.figure(2, figsize = (10,10))
plt.xlim(0)
plt.legend(loc = 'lower left', fontsize = LGF)
plt.xlabel('Cycle Number (N)', fontsize = LBF)
plt.ylabel('Void Ratio ($e$)', fontsize = LBF)
plt.gca().tick_params(which='major', labelsize=TS)
plt.grid(ls=':', lw=1, c='gray')

plt.figure(1, figsize = (10,10))
plt.legend(loc = 'upper left', fontsize = LGF)
plt.gca().tick_params(which='major', labelsize=TS)

plt.show()
