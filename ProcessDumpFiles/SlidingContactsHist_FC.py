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

# Define Plot Fontsizes
TF = 24     # Text font
LGF = 16   # Legend Font Size
LBF = 14    # Label Font Size
TS = 12     # Tick Size
lw1 = 3

friction_coefficients = [20,15,10]

path_25 = r'E:\Monotonic_Undrained\Initial_300\run1'
paths = [path_25]
label_list = ['$\mu = 0.25$']
for FC in friction_coefficients:
    paths.append(rf'E:\Monotonic_Undrained\300kPa_FC\FC0p{FC}\run1')
    label_list.append(f'$\mu = 0.{FC}$')

dump_file_number = 0

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
sliding_count = []
all_data = pd.DataFrame(data = {'Ratio':[],'Friction Coefficient':[]})
for p, path in enumerate(paths):
    print(path)
    CFC = get_ratioRSF_NF(path,dump_file_number)
    labels = label_list[p]
    temp = pd.DataFrame(data = {'Ratio':CFC,'Friction Coefficient':labels})

    all_data = pd.concat([all_data, temp])


  
colors = [
    "#00e798",
    "#33ff8a",
    "#33fff6",
    "#33beff"
    ]
#6eeafa blue c0 #00e798 green

plt.figure(figsize = (10,5))

sns.set_palette(sns.color_palette(colors))
sns.histplot(data = all_data, x = 'Ratio', hue = 'Friction Coefficient')
plt.xticks(rotation = 90)
plt.xlabel(r'$\frac{F_t}{F_n}$', fontsize = LBF+4)
plt.ylabel('Count', fontsize = LBF)
plt.tick_params(which = 'both', labelsize = TS)
plt.tight_layout()
plt.grid(axis='y')
plt.ylim(0,13000)
plt.show()
