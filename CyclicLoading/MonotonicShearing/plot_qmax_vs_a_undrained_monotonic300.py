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

from basicFunctions.get_fabric_tensor import get_fabric_tensor_cn
from basicFunctions.yimsiriSoga import  get_a_yimsiri_soga
# ==============================================================================
# Define Plot Fontsizes
TF = 24     # Text font
LGF = 11   # Legend Font Size
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

# Empty pandas array to save a values
a_data = pd.DataFrame(columns = ['cycle_number','a_15_P0','a_30_P0','a_60_P0','a_90_P0','a_90_P2'])
a_data['cycle_number'] = [0,1,2,3,4,5,10,20,30,40,50]

# Yimsiri and Soga
def get_a_val(path, pos):
    """

    """
    path = path + pos + r'\contact'
    os.chdir(path)
    # Getting Contact Dump Files
    contact_files = os.listdir()

    step_number = []
    print(contact_files)
    for contact_file in contact_files:
        step_number.append(re.findall('\d+', contact_file))

    print(contact_files)
    step_number = [int(step[0]) for step in step_number] # Convert string to integer

    yimsiri_soga_a_value = pd.DataFrame(data = {'file_name':contact_files, 'step_number':step_number})
    yimsiri_soga_a_value = yimsiri_soga_a_value.sort_values(by = ['step_number'], ascending = True)

    # Initiating lists
    a = []
    a1 = []
    a2 = []
    a3 = [] 

    # Iterating trough dump files
    for contact_file in yimsiri_soga_a_value.file_name:

        # Loading contact file
        contact_data = pd.read_csv(
                contact_file,
                skiprows = 9,
                delimiter = ' ',
                index_col = False,
                header = None
            )

        # Getting Fabric Tensor
        CNfabrictensor = get_fabric_tensor_cn(contact_data)

        # Getting mean a
        a_mean, a_val1, a_val2, a_val3 = get_a_yimsiri_soga(CNfabrictensor)
        a.append(a_mean)
        a1.append(a_val1)
        a2.append(a_val2)
        a3.append(a_val3)

    return a

for i, amp in enumerate(ampl_list):
    os.chdir(path)
    qmax_e0_data = pd.read_csv(f'qmax_e_{amp}.csv')
    print(qmax_e0_data.qmax)
    path2 = rf'E:\CyclicLoading\Cyclicmean\TX300_FC0p25to0p25_amp{amp}\merged_data\SortedData'
    a = get_a_val(path2, r"\0_StartingPos")
    len(a)
    a_values = np.take(a, [0,1,2,3,4,5,10,20,30,40,50])
    a_data[f'a_{amp}_P0'] = a_values

    plt.figure(1, figsize = (6,8))
    plt.plot(
        a_values,
        qmax_e0_data.qmax/1000,
        color = color_list[i],
        ls = '-',
        marker = 'o',
        mec = "black",
        label = label_list[i])

    # Labeling Samples for comparison 
    if amp == 60:
        plt.plot(
                a_values[10],
                qmax_e0_data.qmax[10]/1000,    
                ms = 10, 
                markerfacecolor="None", 
                mec = 'black',
                marker = 'o') 

        plt.text(-0.0232, qmax_e0_data.qmax[10]/1000, "S2", ha = 'center', va = 'center', fontsize = 12)

    if amp == 90:
        plt.plot(
                a_values[1],
                qmax_e0_data.qmax[1]/1000,    
                ms = 10, 
                markerfacecolor="None", 
                mec = 'black',
                marker = 'o') 

        plt.text(-0.066, qmax_e0_data.qmax[1]/1000, "S1", ha = 'center', va = 'center', fontsize = 12)
    
    # Add pos 2
    if amp == 90:
        os.chdir(path)
        qmax_e0_data = pd.read_csv(f'qmax_e_90_P2.csv')
        path2 = rf'E:\CyclicLoading\Cyclicmean\TX300_FC0p25to0p25_amp90\merged_data\SortedData'
        a = get_a_val(path2, r"\2_NeutralPos")
        len(a)
        a_values = np.take(a, [0,1,2,3,4,5,10,20,30,40,50])
        print(a_values)
        a_data[f'a_{amp}_P2'] = a_values
        plt.figure(1, figsize = (6,8))
        plt.plot(
            a_values,
            qmax_e0_data.qmax/1000,
            color = "indianred",
            ls = '-',
            marker = 'o',
            mec = "black",
            label = '$q^{ampl}$ = 90kPa Position 2')
    

os.chdir(path)
a_data.to_csv("a_values300.csv",index=False)

# Adding vertical lines
ymin, ymax = plt.gca().get_ylim()
plt.ylim(ymin, ymax)

plt.legend(loc = 'lower right', fontsize = LGF)
plt.xlabel("Degree of anisotropy ($a$)", fontsize = LBF)
plt.ylabel("Maximum deviatoric stress ($q^{max}$) [kPa]", fontsize = LBF)
plt.gca().tick_params(which = "both", labelsize = TS)
plt.grid()
plt.tight_layout()

plt.show()
