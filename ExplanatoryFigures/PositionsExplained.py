"""
Author: Tara Sassel
Date: 15/11/2022

This script is to show the diffrent positions during one loading cycle.

"""
# Imports
import os
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
matplotlib.rcParams['axes.linewidth'] = 2

path = r'E:\CyclicLoading\Cyclicmean\TX300_FC0p25to0p25_amp90\merged_data'
os.chdir(path)
stress_data = pd.read_csv('stress_data.csv')

step_interval = stress_data.step_s[1]-stress_data.step_s[0]
time_step = 5.242309e-09
period = 0.25
cycle_length = int(period/time_step)
quarter_cycle_steps = int(cycle_length/(4*step_interval))

plt.figure(figsize = (7,7))

# Stress zz
plt.plot(
    stress_data.step_s[quarter_cycle_steps*4:quarter_cycle_steps*8],
    stress_data.stress_zz[quarter_cycle_steps*4:quarter_cycle_steps*8],
    c = 'black',
    lw = 3,
    ls = '--'
)

plt.hlines(
    300000,
    stress_data.step_s[quarter_cycle_steps*3],
    stress_data.step_s[quarter_cycle_steps*8.5],
    ls = "-",
    lw = 2,
    color = 'black'
)

# Starting pos
plt.plot(
    stress_data.step_s[quarter_cycle_steps*4],
    stress_data.stress_zz[quarter_cycle_steps*4],
    c = 'cornflowerblue',
    marker = 'o',
    ms = 10,
    mec = 'black'
)

plt.text(
    stress_data.step_s[quarter_cycle_steps*4],
    285000,
    ha = 'center',
    va = 'center',
    s = 'Starting Position \n Position 0'
)

plt.plot(
    stress_data.step_s[quarter_cycle_steps*8],
    stress_data.stress_zz[quarter_cycle_steps*8],
    c = 'cornflowerblue',
    marker = 'o',
    ms = 10,
    mec = 'black'
)

# Loaded Pos
plt.plot(
    stress_data.step_s[quarter_cycle_steps*5],
    stress_data.stress_zz[quarter_cycle_steps*5],
    c = 'darkorange',
    marker = 'o',
    ms = 10,
    mec = 'black'
)

plt.text(
    stress_data.step_s[quarter_cycle_steps*5],
    400000,
    ha = 'center',
    va = 'center',
    s = 'Loaded Position \n Position 1'
)

# Neutral Pos
plt.plot(
    stress_data.step_s[quarter_cycle_steps*6],
    stress_data.stress_zz[quarter_cycle_steps*6],
    c = 'indianred',
    marker = 'o',
    ms = 10,
    mec = 'black'
)

plt.text(
    stress_data.step_s[int(quarter_cycle_steps*6.5)],
    310000,
    ha = 'center',
    va = 'center',
    s = 'Neutral Position \n Position 2'
)

# Unloaded Pos
plt.plot(
    stress_data.step_s[quarter_cycle_steps*7],
    stress_data.stress_zz[quarter_cycle_steps*7],
    c = 'forestgreen',
    marker = 'o',
    ms = 10,
    mec = 'black'
)

plt.text(
    stress_data.step_s[quarter_cycle_steps*7],
    200000,
    ha = 'center',
    va = 'center',
    s = 'Unoaded Position \n Position 3'
)

# Hline
plt.hlines(390000, stress_data.step_s[int(quarter_cycle_steps*3.4)],stress_data.step_s[int(quarter_cycle_steps*8.5)], ls = ':', color = 'black', lw = 1)
plt.hlines(210000, stress_data.step_s[int(quarter_cycle_steps*3.4)],stress_data.step_s[int(quarter_cycle_steps*8.5)], ls = ':', color = 'black', lw = 1)

plt.text(
    stress_data.step_s[int(quarter_cycle_steps*3.4)]-6000000,
    390000,
    ha = 'center',
    va = 'center',
    s = "$p'^{av} + \sigma'^{ampl}$",
    fontsize = 12
)

plt.text(
    stress_data.step_s[int(quarter_cycle_steps*3.4)]-6000000,
    210000,
    ha = 'center',
    va = 'center',
    s = "$p'^{av} - \sigma'^{ampl}$", 
    fontsize = 12
)

plt.text(
    stress_data.step_s[int(quarter_cycle_steps*3.4)]-6000000,
    300000,
    ha = 'center',
    va = 'center',
    s = "$p'^{av}$", 
    fontsize = 12
)


# Ajust figure
ax = plt.gca()
ax.set_xticks([])
ax.set_yticks([])

# Hide the right and top spines
ax.spines.right.set_visible(False)
ax.spines.top.set_visible(False)
ax.spines.bottom.set_visible(False)

# Remove spines
ax.yaxis.set_ticks_position('left')
ax.xaxis.set_ticks_position('bottom')

ax.set_xlim(stress_data.step_s[int(quarter_cycle_steps*3.4)],stress_data.step_s[int(quarter_cycle_steps*8.5)])
ax.set_ylim(170000,420000)
plt.xlabel("Step number (N)", fontsize = 15)
plt.ylabel("Axial stress ($\sigma_{zz}}$)", fontsize = 15)
ax.yaxis.set_label_coords(-.2, .5)
plt.tight_layout()

#plt.savefig(r'C:\Users\shrab\Google Drive\PhD\My Writing\Paper_CyclicMean\Positions_Explained.png')
#plt.savefig(r'C:\Users\shrab\Google Drive\PhD\My Writing\Paper_CyclicMean\Positions_Explained.eps' , format = 'eps')
plt.tight_layout()
plt.show()
