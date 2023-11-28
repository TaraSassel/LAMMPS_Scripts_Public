"""
Author: Tara Sassel 
Date: 08/02/2023

This script is to plot the contact normal distribution for cyclic mean data:
"""
# Imports 
import re 
import os 
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

from basicFunctions.get_cyclicmean_data import get_cyclicmean_data

# =======================================================================================
path_list, color_list =  get_cyclicmean_data('pav300_V2','E')
wanted_positions = ['0', '2'] # string 0, 1, 2, 3
ls_list = ['-', ':']

N = 51 # Number of cycles 

# Defining Labels
label_list = [
    '$q^{ampl}$ = 15kPa',
    '$q^{ampl}$ = 20kPa',
    '$q^{ampl}$ = 30kPa',
    '$q^{ampl}$ = 60kPa',
    '$q^{ampl}$ = 90kPa']

# Definig Plot Fontsizes
TF = 24     # Text font
LGF = 12   # Legend Font Size
LBF = 14    # Label Font Size
TS = 14     # Tick Size
lw1 = 2     # Line Width
ms1 = 5     # marker size 
# =======================================================================================

def get_RSF_NF(file: str) -> np.array:
    """
    Calcualting resultant shear force / normal force
    """

    # Loading dump file
    contact_data = pd.read_csv(file,
        skiprows = 9,
        header = None,
        delimiter = ' ',
        index_col=False)

    # Non zero contacts
    contact_data_n0 = contact_data[contact_data[3]>0]
    contact_data_n0 = contact_data_n0.to_numpy().T

    FC = 0.25 # Friction coefficent

    tfx = contact_data_n0[0,:]
    tfy = contact_data_n0[1,:]
    tfz = contact_data_n0[2,:]

    # 1. Distance between centroids (branch vector)
    X1 = contact_data_n0[6,:]
    Y1 = contact_data_n0[7,:]
    Z1 = contact_data_n0[8,:]
    R1 = contact_data_n0[9,:]

    X2 = contact_data_n0[10,:]
    Y2 = contact_data_n0[11,:]
    Z2 = contact_data_n0[12,:]
    R2 = contact_data_n0[13,:]

    n0_contacts = len(R2)

    # determining branch vector
    BV = np.sqrt(((X1-X2)**2)+((Y1-Y2)**2)+((Z1-Z2)**2)) # disk disk brach vechtor

    # Normal Force
    NF = contact_data_n0[3,:]*BV

    # Resulatnt shear force
    RSF = np.sqrt(tfx**2+tfy**2+tfz**2)

    return X1, Y1, Z1, X2, Y2, Z2, NF, RSF, BV

# =======================================================================================

plt.figure(1, figsize=(7,7))
for k, which_pos in enumerate(wanted_positions):
    for i, path in enumerate(path_list): 
        # Collecting sorted file name list 
        subfolders = [ f.name for f in os.scandir(path + r'\\SortedData') if f.is_dir() ]
        wanted_folder = [i for i in subfolders if i.startswith(which_pos)]
        path_to_contactFiles = path + r'\\SortedData' + r'\\' + wanted_folder[0] + r'\\contact'

        filenames = [ f.name for f in os.scandir(path_to_contactFiles) if f.is_file() ]
        filenumbers = [np.int64(re.findall(r'\d+', name)[0]) for name in filenames]

        d = {'file_name': filenames, 'file_number': filenumbers}
        file_name_df = pd.DataFrame(data=d)
        file_name_df = file_name_df.sort_values(by=['file_number'])
        file_name_df_N = file_name_df.head(N)# Taking N cycles 
        # =======================================================================================

        # Iterating trough files 
        os.chdir(path_to_contactFiles)

        NF_av = np.zeros((N,))
        cycle_number = np.arange(0,N, 1)

        a_values = np.zeros(len(file_name_df))

        for j, file in enumerate(file_name_df_N.file_name):
            # Get contact force 
            X1, Y1, Z1, X2, Y2, Z2, NF, RSF, BV = get_RSF_NF(file)
            NF_av[j] = np.mean(NF) # Mean normal force 

            d = {}
            contact_df = pd.DataFrame(data = d)


        # Figure
        plt.plot(cycle_number, NF_av, lw = lw1, ms = ms1, marker = 'o', mec = 'black', color = color_list[i], ls = ls_list[k])

# Figure adjustments 
ax = plt.gca()
# Legend 
custom_lines1 = [Line2D([0], [0], c = color_list[0], lw=4, label = label_list[0]),
                Line2D([0], [0], c = color_list[1], lw=4, label = label_list[1]),
                Line2D([0], [0], c = color_list[2], lw=4, label = label_list[2]),
                Line2D([0], [0], c = color_list[3], lw=4, label = label_list[3]),
                Line2D([0], [0], c = color_list[4], lw=4, label = label_list[4])]

custom_lines2 = [Line2D([0], [0], c = 'black', ls = '-', lw=2, ms = ms1, marker = 'o', mec = 'black',label = r'Position 0'),
                Line2D([0], [0], c = 'black', ls = ':', lw=2, ms = ms1, marker = 'o', mec = 'black',label = r'Position 2')]

lg1 = ax.legend(handles=custom_lines1 , loc='lower left', fontsize = LGF)
lg2 = ax.legend(handles=custom_lines2 , loc='upper right', fontsize = LGF)
ax.add_artist(lg1)

# Labels 
plt.xlabel('Cycle number (N)', fontsize = LBF)
plt.ylabel('Average contact normal force ($F_N^{av}$) [N]', fontsize = LBF)
plt.xlim(0,50)
plt.tight_layout()

plt.show()


