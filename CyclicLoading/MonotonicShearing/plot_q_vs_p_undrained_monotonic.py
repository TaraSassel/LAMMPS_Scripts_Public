"""
Author: Tara
Date: 02/11/2022

This figure is to visualize monotonic undrained loading
For samples at diffrent stages of cyclic loading
"""
# Import Libraries
import os
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
# ==============================================================================
# Define Plot Fontsizes
TF = 24     # Text font
LGF = 12   # Legend Font Size
LBF = 15    # Label Font Size
TS = 12     # Tick Size
lw1 = 2     # Line Width

path = r'F:\Monotonic_Undrained\300kPa_30\Cycle4\merged_data' # Path to merged_data
# ==============================================================================

os.chdir(path)
stress_data = pd.read_csv('stress_data.csv')
void_data = pd.read_csv('void_data.csv')

# Convert to numpy
np_stress_data = {}
col_names = stress_data.columns
for i, name in enumerate(col_names):
    np_stress_data[f"{name}"] = stress_data.iloc[:,i].to_numpy().T

    # Calculate q p
q = (np_stress_data['stress_zz'] - np_stress_data['stress_xx'])
p = (np_stress_data['stress_xx'] + np_stress_data['stress_yy'] \
    + np_stress_data['stress_zz'])/3
# ==============================================================================
print("Max q: " + str(np.max(q)))
print("Max q/300: " + str(np.max((q)/300)))
print("Initial e: " + str(void_data.void_ratio[0]))
# ==============================================================================
# Figure
plt.plot(p/1000,q/1000)

# Adjusting Figure
plt.ylim(0,300)
plt.xlim(0,500)
plt.xlabel("Mean effective stress (p') [kPa]", fontsize = LBF)
plt.ylabel("Deviatoric stress (q) [kPa]", fontsize = LBF)
plt.legend(loc = 'upper left')
plt.gca().tick_params(axis='both', which='major', labelsize=TS)
plt.gca().spines['right'].set_visible(False)
plt.gca().spines['top'].set_visible(False)
plt.tight_layout()
plt.show()
