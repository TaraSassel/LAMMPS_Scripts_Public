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
LGF = 12   # Legend Font Size
LBF = 15    # Label Font Size
TS = 12     # Tick Size
lw1 = 3

cycle_numbers = [1,2,3,4,5,10,20,30,40,50]

path_300 = r'E:\Monotonic_Undrained\Initial_300\run1'
paths = [path_300]
label_list = ['Isotropic']
for number in cycle_numbers:
    paths.append(rf'E:\Monotonic_Undrained\300kPa_90\Cycle{number}\run1')
    label_list.append(f'Cycle {number}')

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
for p, path in enumerate(paths):
    print(path)
    CFC = get_ratioRSF_NF(path,dump_file_number)
    labels = label_list[p]
    temp = pd.DataFrame(data = {'Ratio':CFC,'Cycle Number':labels})

    # Conting contacts that are within 1% of sliding
    count_sliding = (len(temp[temp.Ratio > (0.25*99/100)]))
    sliding_count.append(count_sliding)

all_data = pd.DataFrame(data = {"Cycle Number": label_list, "Within 1% of sliding": sliding_count})

colors = [
    "#00e798",
    "#6edbfa",
    "#66c8e9",
    "#5eb5d8",
    "#57a2c6",
    "#5090b4",
    "#497ea1",
    "#416d8f",
    "#3a5c7c",
    "#324c6a",
    "#2a3d58",
    "#2a3558"
    ]
#6eeafa blue c0 #00e798 green

plt.figure(figsize = (7,7))

sns.set_palette(sns.color_palette(colors))
sns.barplot(data = all_data, x = 'Cycle Number', y = "Within 1% of sliding")
plt.xticks(rotation = 90)
plt.xlabel('Cycle Number', fontsize = LBF)
plt.ylabel('Contacts within 1% of sliding', fontsize = LBF)
plt.tick_params(which = 'both', labelsize = TS)
plt.tight_layout()
plt.grid(axis='y')
plt.ylim(0,13000)
plt.show()
