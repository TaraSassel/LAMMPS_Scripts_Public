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


# Creating Lists
path_list = []
FC_list = ["0p10","0p11","0p12","0p13","0p14","0p15","0p16","0p17","0p18","0p19","0p20"]
label_list = []
color_list = []
lw1 = 2

palette = sns.color_palette("flare", len(FC_list)-1).as_hex()
color_list = color_list + palette
color_list.append('navy')

plt.figure(figsize = (7,7))

for friction_coefficent in FC_list:
    path_C = rf'E:\Monotonic_Undrained\300kPa_FC\FC{friction_coefficent}\merged_data'
    path_list.append(path_C)

    os.chdir(path_C)
    void_data = pd.read_csv('void_data.csv')
    void0 = void_data.void_ratio[0]

    label_list.append("$e$ = {:.3f}".format(void0))

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

    if j < 2:
        idx = np.argmax(p>400000)
    else:
        idx = len(p)
    plt.plot(p[0:idx]/1000,q[0:idx]/1000, color = color_list[j], label = label_list[j], lw = lw1)

# Adjusting Figure
plt.ylim(0,300)
plt.xlim(0,400)
plt.xlabel("Mean effective stress (p') [kPa]", fontsize = LBF)
plt.ylabel("Deviatoric stress (q) [kPa]", fontsize = LBF)
plt.legend(loc = 'upper left')
plt.gca().tick_params(axis='both', which='major', labelsize=TS)
plt.gca().spines['right'].set_visible(False)
plt.gca().spines['top'].set_visible(False)
plt.tight_layout()

#plt.savefig(r'C:\Users\shrab\Google Drive\PhD\My Writing\Paper_CyclicMean\Monotonic_Undrained_FC.png')
#plt.savefig(r'C:\Users\shrab\Google Drive\PhD\My Writing\Paper_CyclicMean\Monotonic_Undrained_FC.eps', format='eps')
plt.show()
