"""
    Author: Tara Sassel
    Date: 20/10/2022

    This script calculates the parameter "a" in accordance with Yimsiri and Soga
    For all cyclic loading simulations
"""

# Import Libraries
import re
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from basicFunctions.get_fabric_tensor import get_fabric_tensor_cn
from basicFunctions.yimsiriSoga import  get_a_yimsiri_soga

# ==============================================================================
# FIGURE
# Define Plot Fontsizes
TF = 24     # Text font
LGF = 15   # Legend Font Size
LBF = 18    # Label Font Size
TS = 14     # Tick Size
lw1 = 3

pos_list = ['0_StartingPos', '1_LoadedPos', '2_NeutralPos', '3_UnloadedPos']
pos_folder = pos_list[3]
print(pos_folder)

# Defining Path
drive = "E"
path_300_15 = rf'{drive}:\CyclicLoading\Cyclicmean\TX300_FC0p25to0p25_amp15\merged_data\SortedData\{pos_folder}\contact'
path_300_20 = rf'{drive}:\CyclicLoading\Cyclicmean\TX300_FC0p25to0p25_amp20\merged_data\SortedData\{pos_folder}\contact'
path_300_30 = rf'{drive}:\CyclicLoading\Cyclicmean\TX300_FC0p25to0p25_amp30\merged_data\SortedData\{pos_folder}\contact'
path_300_60 = rf'{drive}:\CyclicLoading\Cyclicmean\TX300_FC0p25to0p25_amp60\merged_data\SortedData\{pos_folder}\contact'
path_300_90 = rf'{drive}:\CyclicLoading\Cyclicmean\TX300_FC0p25to0p25_amp90\merged_data\SortedData\{pos_folder}\contact'

path_list = [path_300_15, path_300_20, path_300_30, path_300_60, path_300_90]
label_list = ['ampl = 15kPa', 'ampl = 20kPa', 'ampl = 30kPa', 'ampl = 60kPa', 'ampl = 90kPa']
color_list = ['#f0f9e8', '#bae4bc', '#7bccc4', '#43a2ca', '#0868ac']
# ==============================================================================
for p, path in enumerate(path_list):
    print(path)
    os.chdir(path)

    # Getting Contact Dump Files
    contact_files = os.listdir()
    try:
        contact_files.remove("fabric_tensor.csv")
    except:
        pass

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

    yimsiri_soga_a_value['a_mean'] = a
    yimsiri_soga_a_value['a1'] = a1
    yimsiri_soga_a_value['a2'] = a2
    yimsiri_soga_a_value['a3'] = a3

    # FIGURE =======================================================================
    plt.figure(1, figsize = (10,7))
    cycle_n = np.arange(0,len(yimsiri_soga_a_value.a_mean),1)
    plt.plot(cycle_n, yimsiri_soga_a_value.a_mean, color = color_list[p], lw = 3, label=label_list[p], marker = 'o', mec = 'black',mfc=color_list[p])

#plt.ylim(-0.08, 0.04)
plt.legend(loc = 'lower right', fontsize = LGF)
plt.xlabel('Cycle number (N)', fontsize = LBF)
plt.ylabel('Degree of anisotropy (a)', fontsize = LBF)
plt.gca().tick_params(which='major', labelsize=TS)
plt.xlim(0,50)
plt.grid()
plt.show()
