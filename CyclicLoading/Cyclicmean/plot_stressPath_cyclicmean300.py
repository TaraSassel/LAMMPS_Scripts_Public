"""
Author: Tara Sassel
Date: 24/10/2022

Visualize stress path for cyclic mean 300kPa
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import matplotlib.gridspec as gridspec

# ==============================================================================
# Defining Path
path_300_15 = r'F:\CyclicLoading\Cyclicmean\TX300_FC0p25to0p25_amp15\merged_data'
path_300_20 = r'F:\CyclicLoading\Cyclicmean\TX300_FC0p25to0p25_amp20\merged_data'
path_300_30 = r'F:\CyclicLoading\Cyclicmean\TX300_FC0p25to0p25_amp30\merged_data'
path_300_60 = r'F:\CyclicLoading\Cyclicmean\TX300_FC0p25to0p25_amp60\merged_data'
path_300_90 = r'F:\CyclicLoading\Cyclicmean\TX300_FC0p25to0p25_amp90\merged_data'

path_list = [path_300_15, path_300_20, path_300_30, path_300_60, path_300_90]
color_list = ['#f0f9e8', '#bae4bc', '#7bccc4', '#43a2ca', '#0868ac']

# FIGURE
# Define Plot Fontsizes
TF = 24     # Text font
LGF = 12   # Legend Font Size
LBF = 15    # Label Font Size
TS = 12     # Tick Size
lw1 = 2     # Line Width

# ==============================================================================
# Calculating cycle length
time_step = 5.242309e-09
period = 0.25
cycle_length = int(period/(time_step))

# ==============================================================================
plt.figure(figsize=(10, 10)) # Initiating Figure
for i, path in enumerate(path_list):
    print(path)
    os.chdir(path)
    stress_data = pd.read_csv('stress_data.csv')

    # Plotting
    plt.plot(stress_data.step_s/cycle_length, stress_data.stress_zz/1000, color = color_list[i], lw = lw1)
    if i == 2:
        plt.plot(stress_data.step_s/cycle_length, stress_data.stress_xx/1000, color = 'black',lw = 5)
        plt.plot(stress_data.step_s/cycle_length, stress_data.stress_yy/1000, color = 'maroon', lw = 2)

# legend
custom_lines1 = [Line2D([0], [0], color=color_list[0], lw=lw1),
                Line2D([0], [0], color=color_list[1], lw=lw1),
                Line2D([0], [0], color=color_list[2], lw=lw1),
                Line2D([0], [0], color=color_list[3], lw=lw1),
                Line2D([0], [0], color=color_list[4], lw=lw1)]

custom_lines2 = [Line2D([0], [0], color='black', lw=5),
                Line2D([0], [0], color='maroon', lw=2)]

l1 = plt.legend(custom_lines1, [
        '$\sigma_1$ ampl = 15kPa',
        '$\sigma_1$ ampl = 20kPa',
        '$\sigma_1$ ampl = 30kPa',
        '$\sigma_1$ ampl = 60kPa',
        '$\sigma_1$ ampl = 90kPa'],
    loc='center left',
    bbox_to_anchor=(1, 0.5),
    fontsize = LGF)

l2 = plt.legend(custom_lines2, [
        '$\sigma_2$',
        '$\sigma_3$'],
    loc='center left',
    bbox_to_anchor=(1, 0.9),
    fontsize = LGF)

plt.gca().add_artist(l1)

# Axis
plt.xlabel('Cycle Number (N)', fontsize = LBF)
plt.ylabel('Stress [kPa]', fontsize = LBF)
plt.xlim(0,3)
plt.ylim(200,400)
plt.yticks([210, 240, 270, 280, 285, 315, 320, 330, 360, 390])
plt.gca().tick_params(which='major', labelsize=TS)
plt.grid(ls=':', lw=1, c='gray')

plt.tight_layout()
os.chdir(r'C:\Users\shrab\Google Drive\PhD\Meetings\FiguresCyclicmean')
plt.savefig('stress_path.png', bbox_inches='tight')
plt.show()
