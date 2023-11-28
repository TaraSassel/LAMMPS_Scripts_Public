"""
Author: Tara
Date: 01/12/2022

Script creates 2 figures
    qmax vs e0
    qmax vs step_number

qmax_vs_e_undrained_monotonic.py should be run first to created required csv files
"""
# Import Libraries
import os
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
# ==============================================================================
# Define Plot Fontsizes
TF = 24     # Text font
LGF = 12   # Legend Font Size
LBF = 15    # Label Font Size
TS = 12     # Tick Size
lw1 = 2     # Line Width

path = r'E:\Monotonic_Undrained'
os.chdir(path)
# ==============================================================================
color_list = ['#f0f9e8', '#7bccc4', '#43a2ca', '#0868ac']
label_list = [
    '$q^{ampl}$ = 15kPa Position 0',
    '$q^{ampl}$ = 30kPa Position 0',
    '$q^{ampl}$ = 60kPa Position 0',
    '$q^{ampl}$ = 90kPa Position 0'
    ]
ampl_list = [15, 30, 60, 90]

for i, amp in enumerate(ampl_list):
    qmax_e0_data = pd.read_csv(f'qmax_e_{amp}.csv')

    plt.figure(1, figsize = (6,8))
    plt.plot(
        qmax_e0_data.void_ratio,
        qmax_e0_data.qmax/1000,
        color = color_list[i],
        ls = '-',
        marker = 'o',
        mec = "black",
        label = label_list[i])

    # Labeling Samples for comparison 
    if amp == 60:
        plt.plot(
                qmax_e0_data.void_ratio[10],
                qmax_e0_data.qmax[10]/1000,    
                ms = 10, 
                markerfacecolor="None", 
                mec = 'black',
                marker = 'o') 

        plt.text(0.651, qmax_e0_data.qmax[10]/1000, "S2", ha = 'center', va = 'center', fontsize = 12)

    if amp == 90:
        plt.plot(
                qmax_e0_data.void_ratio[1],
                qmax_e0_data.qmax[1]/1000,    
                ms = 10, 
                markerfacecolor="None", 
                mec = 'black',
                marker = 'o') 

        plt.text(0.651, qmax_e0_data.qmax[1]/1000, "S1", ha = 'center', va = 'center', fontsize = 12)

    plt.figure(2, figsize = (6,8))
    plt.plot(
        qmax_e0_data.cycle_number,
        qmax_e0_data.qmax/1000,
        color = color_list[i],
        ls = '-',
        marker = 'o',
        mec = "black",
        label = label_list[i])

    # Labeling Samples for comparison 
    if amp == 60:
        plt.plot(
                qmax_e0_data.cycle_number[10],
                qmax_e0_data.qmax[10]/1000,    
                ms = 10, 
                markerfacecolor="None", 
                mec = 'black',
                marker = 'o') 

        plt.text(50, 75, "S2", ha = 'center', va = 'center', fontsize = 12)

    if amp == 90:
        plt.plot(
                qmax_e0_data.cycle_number[1],
                qmax_e0_data.qmax[1]/1000,    
                ms = 10, 
                markerfacecolor="None", 
                mec = 'black',
                marker = 'o') 

        plt.text(3.5, 23.3, "S1", ha = 'center', va = 'center', fontsize = 12)


plt.figure(1, figsize = (6,8))
qmax_e0_data = pd.read_csv(f'qmax_e_90_P2.csv')
plt.plot(
    qmax_e0_data.void_ratio,
    qmax_e0_data.qmax/1000,
    color = "indianred",
    ls = '-',
    marker = 'o',
    mec = "black",
    label = '$q^{ampl}$ = 90kPa Position 2')

# Adding vertical lines
ymin, ymax = plt.gca().get_ylim()
#plt.gca().vlines(0.65686, ymin, ymax, ls = '--', lw = 2, color = 'black')
plt.gca().vlines(0.6497, ymin, ymax, ls = '--', lw = 2, color = 'black')
plt.ylim(ymin, ymax)

plt.legend(loc = 'lower left', fontsize = LGF)
plt.xlabel("Void ratio ($e$)", fontsize = LBF)
plt.ylabel("Maximum deviatoric stress ($q^{max}$) [kPa]", fontsize = LBF)
plt.gca().tick_params(which = "both", labelsize = TS)
plt.grid()
plt.tight_layout()

plt.figure(2, figsize = (6,8))
plt.plot(
    qmax_e0_data.cycle_number,
    qmax_e0_data.qmax/1000,
    color = "indianred",
    ls = '-',
    marker = 'o',
    mec = "black",
    label = '$q^{ampl}$ = 90kPa Position 2')

plt.legend(loc = 'lower right', fontsize = LGF)
plt.xlabel("Cycle number (N)", fontsize = LBF)
plt.ylabel("Maximum deviatoric stress ($q^{max}$) [kPa]", fontsize = LBF)
plt.gca().tick_params(which = "both", labelsize = TS)
plt.grid()
plt.tight_layout()

# Adding section for diffrent friction coefficient 

plt.show()
