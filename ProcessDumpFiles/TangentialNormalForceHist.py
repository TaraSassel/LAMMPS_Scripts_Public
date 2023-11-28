"""
Author: Tara Sassel
Date: 15/11/2022

Histogram of ratio Tangential/Normal Force
"""

import os
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


# FIGURE
# Define Plot Fontsizes
TF = 24     # Text font
LGF = 12   # Legend Font Size
LBF = 15    # Label Font Size
TS = 12     # Tick Size
lw1 = 3

path_300 = r'F:\Monotonic_Undrained\Initial_300\run1'
path_300_90_C1 = r'F:\Monotonic_Undrained\300kPa_90\Cycle1\run1'
path_300_90_C5 = r'F:\Monotonic_Undrained\300kPa_90\Cycle5\run1'
path_300_90_C10 =r'F:\Monotonic_Undrained\300kPa_90\Cycle10\run1'
path_300_90_C50 =r'F:\Monotonic_Undrained\300kPa_90\Cycle50\run1'

paths = [path_300,path_300_90_C1,path_300_90_C5,path_300_90_C10,path_300_90_C50]
dump_file_number = 0
label_list = ['Isotropic','Cycle 1', 'Cycle 5', 'Cycle 10', 'Cycle 50']
hue_order  = ['Cycle 50', 'Cycle 10', 'Cycle 5','Cycle 1','Isotropic']

# ==============================================================================
def get_ratioRSF_NF(path: str, dump_file_number: int) -> np.array:
    """
    Calcualting resultant shear force / normal force
    """

    # Loading dump file
    folder = r'\contact'
    os.chdir(path + folder)
    contact_data = pd.read_csv(
        "dump0.contact",
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
    rsf = np.sqrt(tfx**2+tfy**2+tfz**2)
    CFC = rsf/NF

    return CFC

# ==============================================================================
all_data = pd.DataFrame()
for p, path in enumerate(paths):
    print(path)
    CFC = get_ratioRSF_NF(path,dump_file_number)
    labels = label_list[p]
    temp = pd.DataFrame(data = {'Ratio':CFC,'Cycle Number':labels})

    all_data = all_data.append(temp)

all_data = all_data.reset_index()
print('Creating histogram')
g1 = sns.histplot(data = all_data, x = 'Ratio', hue = 'Cycle Number',  alpha = 0.4, hue_order = hue_order)
plt.xlabel(r'$\dfrac{Resultant\ shear\ force} {Normal\ force}$')
plt.ylabel(r'Number of contacts')

plt.tight_layout()
plt.show()
