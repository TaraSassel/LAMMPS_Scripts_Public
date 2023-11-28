"""
Author: Tara Sassel
Date: 27/10/2022
This script was created to get the void ratio at 35% to compare my value with
Huang et al. (2014) and see if I have a comparable critical state line
"""
# Import Libraries
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from basicFunctions.get_strain import get_strain

# Define directory
path = None # Path to merged_data
os.chdir(path)

# Define Plot Fontsizes
TF = 24     # Text font
LGF = 12   # Legend Font Size
LBF = 15    # Label Font Size
TS = 12     # Tick Size
lw1 = 2     # Line Width

# Load Data
void_data = pd.read_csv('void_data.csv')
stress_data = pd.read_csv('stress_data.csv')

void_ratio = void_data.void_ratio.to_numpy().T
zlength = stress_data.length_z.to_numpy().T
zstrain = get_strain(zlength)

# Getting point at 35% strain
index35 = np.argmax(zstrain >= 35)
void_ratio35 = void_ratio[index35]
zstrain35 = zstrain[index35]
print(f'The void ratio at 35% axial strain is {void_ratio35:.3}')

# Figure
plt.plot(zstrain, void_ratio, lw = lw1, color = 'black')
plt.plot(zstrain35, void_ratio35, ls = '', marker = 'o', color = 'red')

plt.xlabel('Axial Strain $\epsilon_{zz}$ [%]', fontsize = LBF)
plt.ylabel('Void Ratio (e)', fontsize = LBF)
plt.xlim(0,)
plt.gca().tick_params(which = 'major', labelsize = TS)
plt.grid()
plt.tight_layout()
plt.show()
