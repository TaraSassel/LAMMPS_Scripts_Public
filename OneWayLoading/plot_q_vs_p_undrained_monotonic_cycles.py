"""
Author: Tara
Date: 02/11/2022

This figure is to visualize monotonic undrained loading
For samples at diffrent stages of cyclic loading
"""
# Import Libraries
import os
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)

# Define Plot Fontsizes
TF = 24     # Text font
LGF = 8   # Legend Font Size
LBF = 15    # Label Font Size
TS = 12     # Tick Size
lw1 = 2     # Line Width

# Creating Lists
path_list = []
cycle_list = [0,1,2,3,4,5,10,20,30,40]
label_list = []
color_list = []
lw1 = 2

palette = sns.color_palette("crest", len(cycle_list)).as_hex()
color_list = color_list + palette
color_list.append('navy')

for cycle in cycle_list:
    path_C = rf'E:\CyclicLoading\Cyclicmean_OneWay\UndrainedShearing\TX390_FC0p25to0p25_amp90\Position2\Cycle{cycle}\merged_data'
    path_list.append(path_C)

    os.chdir(path_C)
    void_data = pd.read_csv('void_data.csv')
    void0 = void_data.void_ratio[0]

    label_list.append(rf"$N$ = {cycle} $\rightarrow$ $e$  = {void0:.3f}")

# Processing
for j, path in enumerate(path_list):

    os.chdir(path)
    stress_data = pd.read_csv('stress_data.csv')

    # Convert to numpy
    np_stress_data = {}
    col_names = stress_data.columns
    for i, name in enumerate(col_names):
        np_stress_data[f"{name}"] = stress_data.iloc[:,i].to_numpy().T

    # Calculate q p
    q = (np_stress_data['stress_zz'] - np_stress_data['stress_xx'])
    p = (np_stress_data['stress_xx'] + np_stress_data['stress_yy'] + np_stress_data['stress_zz'])/3

    plt.plot(p/1000,q/1000, color = color_list[j], label = label_list[j], lw = lw1)

# Adjusting Figure
plt.ylim(0,200)
plt.xlim(0,400)
plt.xlabel("Mean effective stress (p') [kPa]", fontsize = LBF)
plt.ylabel("Deviatoric stress (q) [kPa]", fontsize = LBF)
plt.legend(loc = 'upper left', fontsize = LGF)
plt.gca().yaxis.set_minor_locator(MultipleLocator(5))
plt.gca().tick_params(axis='both', which='major', labelsize=TS)
plt.tight_layout()
plt.grid()
plt.grid(which = 'minor', ls = '--')
#plt.savefig(r'C:\Users\shrab\Google Drive\PhD\My Writing\Paper_CyclicMean\Monotonic_Undrained_300_90_P2.png')
#plt.savefig(r'C:\Users\shrab\Google Drive\PhD\My Writing\Paper_CyclicMean\Monotonic_Undrained_300_90_P2.eps', format='eps')
plt.show()
