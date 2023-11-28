"""
Author: Tara
Date: 02/12/2022

Script creates 2 figures
    qmax vs q
    qmax vs coordination number

qmax_vs_e_undrained_monotonic.py should be run first to created required csv files
"""
# Import Libraries
import re
import os
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from basicFunctions.MechanicalCoordinationNumber import get_mechCoord
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

# Empty pandas array to save mech_coord
mechCoord_data = pd.DataFrame(columns = ['cycle_number','mechCoord_15_P0','mechCoord_30_P0','mechCoord_60_P0','mechCoord_90_P0','mechCoord_90_P2'])
mechCoord_data['cycle_number'] = [0,1,2,3,4,5,10,20,30,40,50]

for i, amp in enumerate(ampl_list):
    os.chdir(path)
    qmax_e0_data = pd.read_csv(f'qmax_e_{amp}.csv')

    # Mechanical Coordination Number
    path2 = rf'E:\CyclicLoading\Cyclicmean\TX300_FC0p25to0p25_amp{amp}\merged_data'
    mech_coord = get_mechCoord(
        path2 + r'\SortedData\0_StartingPos\connectivity',
        ['id','diameter','coord'])

    mech_coord = mech_coord.mechanical_coord.to_numpy().T
    mech_coord_values = np.take(mech_coord, [0,1,2,3,4,5,10,20,30,40,50])
    mechCoord_data[f'mechCoord_{amp}_P0'] = mech_coord_values

    plt.figure(1, figsize = (6,8))
    plt.plot(
        mech_coord_values,
        qmax_e0_data.qmax/1000,
        color = color_list[i],
        ls = '-',
        marker = 'o',
        mec = "black",
        label = label_list[i])

    # Labeling Samples for comparison 
    if amp == 60:
        plt.plot(
                mech_coord_values[10],
                qmax_e0_data.qmax[10]/1000,    
                ms = 10, 
                markerfacecolor="None", 
                mec = 'black',
                marker = 'o') 

        plt.text(5.04, qmax_e0_data.qmax[10]/1000, "S2", ha = 'center', va = 'center', fontsize = 12)

    if amp == 90:
        plt.plot(
                mech_coord_values[1],
                qmax_e0_data.qmax[1]/1000,    
                ms = 10, 
                markerfacecolor="None", 
                mec = 'black',
                marker = 'o') 

        plt.text(4.91, qmax_e0_data.qmax[1]/1000, "S1", ha = 'center', va = 'center', fontsize = 12)
    
    if amp == 90:
        os.chdir(path)
        qmax_e0_data = pd.read_csv(f'qmax_e_90_P2.csv')
        path2 = rf'E:\CyclicLoading\Cyclicmean\TX300_FC0p25to0p25_amp90\merged_data'  
        mech_coord = get_mechCoord(
            path2 + r'\SortedData\2_NeutralPos\connectivity',
            ['id','diameter','coord'])

        mech_coord = mech_coord.mechanical_coord.to_numpy().T
        mech_coord_values = np.take(mech_coord, [0,1,2,3,4,5,10,20,30,40,50])
        mechCoord_data[f'mechCoord_{amp}_P2'] = mech_coord_values

        plt.figure(1, figsize = (6,8))
        plt.plot(
            mech_coord_values,
            qmax_e0_data.qmax/1000,
            color = "indianred",
            ls = '-',
            marker = 'o',
            mec = "black",
            label = '$q^{ampl}$ = 90kPa Position 2')     


os.chdir(path)
mechCoord_data.to_csv("mechCoord_values300.csv",index=False)

# Adding vertical lines
ymin, ymax = plt.gca().get_ylim()
plt.ylim(ymin, ymax)

plt.legend(loc = 'lower right', fontsize = LGF)
plt.xlabel(r"Mechanical coordination number ($\bar C*_N$)", fontsize = LBF)
plt.ylabel("Maximum deviatoric stress ($q^{max}$) [kPa]", fontsize = LBF)
plt.gca().tick_params(which = "both", labelsize = TS)
plt.grid()
plt.tight_layout()

plt.show()
