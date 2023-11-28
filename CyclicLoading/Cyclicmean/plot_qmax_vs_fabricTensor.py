"""
Author: Tara Sassel
Date: 19/01/2023


"""

import os 
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt

# Define Plot Fontsizes
TF = 24     # Text font
LGF = 7   # Legend Font Size
LBF = 12    # Label Font Size
TS = 10     # Tick Size
lw1 = 2     # Line Width

color_list = ['#f0f9e8', '#7bccc4', '#43a2ca', '#0868ac', 'indianred']
label_list = [
    '$q^{peak}$ = 15kPa Position 0',
    '$q^{peak}$ = 30kPa Position 0',
    '$q^{peak}$ = 60kPa Position 0',
    '$q^{peak}$ = 90kPa Position 0',
    '$q^{peak}$ = 90kPa Position 2'
    ]

positions = [0,0,0,0,2]
amplitudes = [15, 30, 60, 90, 90]
cycle_list = [0,1,2,3,4,5,10,20,30,40,50]

# Calculating cycle length
time_step = 5.242309e-09
period = 0.25
cycle_length = int(period/(time_step))-1 # not sure why one less

# Loop trough amplitudes
for i, amp in enumerate(amplitudes):

    # Loading qmax
    os.chdir(r'E:\Monotonic_Undrained')

    # Staring position 
    if positions[i] == 0:
        qmax_data = pd.read_csv(rf"qmax_e_{amp}.csv")
        pos = '0_StartingPos'
        pos_step = 0 # Number of steps to position
        wanted_steps = [cycle*cycle_length + pos_step for cycle in cycle_list] 
    
    # Neutral Position 
    if positions[i] == 2:
        qmax_data = pd.read_csv(rf"qmax_e_{amp}_P2.csv")
        pos = '2_NeutralPos'
        pos_step = int(cycle_length/2)
        wanted_steps = [cycle*cycle_length + pos_step for cycle in cycle_list] 
    
    qmax = qmax_data.qmax.to_numpy().T

    # Loading fabric tensor 
    path = rf'E:\CyclicLoading\Cyclicmean\TX300_FC0p25to0p25_amp{amp}\merged_data\SortedData' + r'\\' + pos
    os.chdir(path)
    fabric_tensor = pd.read_csv("fabric_tensor.csv")
    fabric_tensor_xyz = pd.read_csv("fabric_tensor_xyz.csv")
    fabric_tensor = fabric_tensor[fabric_tensor['step_number'].isin(wanted_steps)]
    fabric_tensor['cycle_number'] = cycle_list 

    # Calculating deviatoric fabric
    ft1 =  fabric_tensor.ft1.to_numpy().T
    ft3 =  fabric_tensor.ft3.to_numpy().T

    ftq = (ft1 - ft3)
    fabric_tensor['ftq'] = ftq

    plt.plot(ftq,qmax/1000, marker = 'o', mec = 'black', c = color_list[i], label = label_list[i])


plt.legend(loc = 'upper right', fontsize = LGF)
plt.xlabel("Deviatoric fabric ($F_d = F_{1} - F_{3}$)", fontsize = LBF)
plt.ylabel("Maximum deviatoric stress ($q^{max}$) [kPa]", fontsize = LBF)
plt.gca().tick_params(which = "both", labelsize = TS)
plt.grid()
plt.tight_layout()

plt.show()
