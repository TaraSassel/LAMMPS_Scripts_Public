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
LBF = 16    # Label Font Size
TS = 14     # Tick Size
lw1 = 2     # Line Width

# ==============================================================================
path0 = r'F:\PhD_Data_Back_Up\LAMMPS\Random_Packing\Istotropic Compression\Toyoura15k\NoFix_ISOCOMP300_Density2650_FC0p25\merged_data'

os.chdir(path0)
stress_data = pd.read_csv('stress_data.csv')
void_data = pd.read_csv('void_data.csv')

# Convert to numpy
np_stress_data = {}
col_names = stress_data.columns
for i, name in enumerate(col_names):
    np_stress_data[f"{name}"] = stress_data.iloc[:,i].to_numpy().T

    # Calculate q p
q0 = ((((np_stress_data['stress_xx']-np_stress_data['stress_yy'])**2 \
            +(np_stress_data['stress_yy']-np_stress_data['stress_zz'])**2 \
            +(np_stress_data['stress_zz'] - np_stress_data['stress_xx'])**2)/2) \
            +3*(np_stress_data['stress_xy']**2 + np_stress_data['stress_xz']**2 + np_stress_data['stress_yz']**2))**0.5

p0 = (np_stress_data['stress_xx'] + np_stress_data['stress_yy'] \
    + np_stress_data['stress_zz'])/3


# ==============================================================================
path = r'E:\StrainControlledCyclic\300kPa\Strain1\merged_data' # Path to merged_data

os.chdir(path)
stress_data = pd.read_csv('stress_data.csv')
void_data = pd.read_csv('void_data.csv')

# Convert to numpy
np_stress_data = {}
col_names = stress_data.columns
for i, name in enumerate(col_names):
    np_stress_data[f"{name}"] = stress_data.iloc[:,i].to_numpy().T

    # Calculate q p
q = ((((np_stress_data['stress_xx']-np_stress_data['stress_yy'])**2 \
            +(np_stress_data['stress_yy']-np_stress_data['stress_zz'])**2 \
            +(np_stress_data['stress_zz'] - np_stress_data['stress_xx'])**2)/2) \
            +3*(np_stress_data['stress_xy']**2 + np_stress_data['stress_xz']**2 + np_stress_data['stress_yz']**2))**0.5

p = (np_stress_data['stress_xx'] + np_stress_data['stress_yy'] \
    + np_stress_data['stress_zz'])/3
# ==============================================================================
step_interval = stress_data.step_s[1]-stress_data.step_s[0]
quarter_cycle_steps = int(5568485/(step_interval))
time_step = 5.24231e-09
quarter_cycle_time = time_step/5568485
# ==============================================================================

# Figure
plt.plot(p0/1000,q0/1000, color = 'darkgreen', lw = lw1, label = 'Isotropic consolidation')
plt.plot(p/1000,q/1000, color = 'navy', lw = lw1, label = 'Strain controlled cyclic loading')
plt.plot(p[0:quarter_cycle_steps*4]/1000,q[0:quarter_cycle_steps*4]/1000, color = 'maroon', lw = lw1, label = 'Cycle 1')

# Adjusting Figure
plt.ylim(-200,)
plt.xlim(0,450)
plt.yticks([-200,-100,0,100,200,300], ["","", 0, "", "",""])
plt.xticks([0,50,100,150,200,250,300,350,400,450], [0,"", "", "","", "","$p'_0$" , "", "",""])

plt.xlabel("Mean effective stress (p') [kPa]", fontsize = LBF)
plt.ylabel("Deviatoric Stress (q) [kPa]", fontsize = LBF)


plt.legend(loc = 'upper left', fontsize = LGF)
plt.vlines(x = 300, ymin = -200, ymax = 0, color ='black', ls = '--')
plt.gca().tick_params(axis='both', which='major', labelsize=TS)
plt.gca().spines['right'].set_visible(False)
plt.gca().spines['top'].set_visible(False)

plt.tight_layout()
plt.show()
