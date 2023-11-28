"""
Author: Tara Sassel
Date: 31/10/2022

Script generates two figures:
    - Void Ratio - Step Number
    - Void Ratio - Axial Strain
"""
# Importing
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from basicFunctions.get_strain import get_strain

# Define Path
path = None # Path to merged_data

# Define Plot Fontsizes
TF = 24     # Text font
LGF = 12   # Legend Font Size
LBF = 15    # Label Font Size
TS = 12     # Tick Size
lw1 = 2     # Line Width

# =============================================================================
# PROCESSING
# Load data
os.chdir(path)
void_data = pd.read_csv('void_data.csv')
stress_data = pd.read_csv('stress_data.csv')

# Convert to numpy
np_void_data = {}
col_names = void_data.columns
for i, name in enumerate(col_names):
    np_void_data[f"{name}"] = void_data.iloc[:,i].to_numpy().T

length_z = stress_data['length_z'].to_numpy().T

# Get Strain
strain_z = get_strain(length_z)

# =============================================================================
# FIGURE
index_v = len(void_data)
index_s = len(stress_data)
if index_v < index_s:
    index_n = index_v
else:
    index_n = index_s

# void ratio - step number
plt.figure(1)
plt.plot(np_void_data['step_v'][0:index_n], np_void_data['void_ratio'][0:index_n], color = 'navy', lw = 2)

plt.xlabel("Step number ($N$)", fontsize = LBF)
plt.ylabel("Void ratio ($e$)", fontsize = LBF)
plt.tight_layout()

# void ratio - axial strain
plt.figure(2)
plt.plot(strain_z[0:index_n], np_void_data['void_ratio'][0:index_n], color = 'navy', lw = 2)

plt.xlabel("Axial strain ($\epsilon_{zz}$) [%]", fontsize = LBF)
plt.ylabel("Void ratio ($e$)", fontsize = LBF)
plt.tight_layout()

plt.show()
