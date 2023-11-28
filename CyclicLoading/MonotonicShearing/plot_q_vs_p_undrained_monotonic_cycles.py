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

# Define Plot Fontsizes
TF = 24     # Text font
LGF = 12   # Legend Font Size
LBF = 15    # Label Font Size
TS = 12     # Tick Size
lw1 = 2     # Line Width

path_initial = r'E:\Monotonic_Undrained\Initial_300\merged_data'

# Creating Lists
path_list = [path_initial]
cycle_list = [1,2,3,4,5,10,20,30,40,50]
label_list = ['Initial']
color_list = ['forestgreen']
lw_list = [2,1,1,1,1,1,1,1,1,1,2]

palette = sns.color_palette("crest", len(cycle_list)-1).as_hex()
color_list = color_list + palette
color_list.append('navy')

for cycle in cycle_list:
    path_C = rf'E:\Monotonic_Undrained\300kPa_15\Cycle{cycle}\merged_data'
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

    plt.plot(p/1000,q/1000, color = color_list[j], label = label_list[j], lw = lw_list[j])

# Adjusting Figure
plt.ylim(0,120)
plt.xlim(0,325)
plt.xlabel("Mean effective stress (p') [kPa]", fontsize = LBF)
plt.ylabel("Deviatoric stress (q) [kPa]", fontsize = LBF)
plt.legend(loc = 'upper left', fontsize = LGF)
plt.gca().tick_params(axis='both', which='major', labelsize=TS)
plt.gca().spines['right'].set_visible(False)
plt.gca().spines['top'].set_visible(False)
plt.tight_layout()

plt.show()
