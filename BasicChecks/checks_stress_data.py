"""
Author: Tara Sassel
Date: 31/10/2022

Script generates six figures:
    - Deviatoric Stress vs Mean effective stress
    - q/p vs Axial Strain
    - Stress vs Axial Strain
    - Stress vs Step Number
    - Volume vs Step Number
    - Wall Velocity vs Step Number
"""
# Importing
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from basicFunctions.get_strain import get_strain

# =============================================================================
# Define Path
path = r'E:\CyclicLoading\Cyclicmean_OneWay\TX270_FC0p25to0p25_amp30\merged_data' # Path to merged_data

# Time Step
time_step = 5.242309e-09 # s required to calculate wall velocity

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
stress_data = pd.read_csv('stress_data.csv')

# Convert to numpy
np_stress_data = {}
col_names = stress_data.columns
for i, name in enumerate(col_names):
    np_stress_data[f"{name}"] = stress_data.iloc[:,i].to_numpy().T

# Calculate q p
q = (np_stress_data['stress_zz'] - np_stress_data['stress_xx'])
p = (np_stress_data['stress_xx'] + np_stress_data['stress_yy'] + np_stress_data['stress_zz'])/3

# get strain
strain_z = get_strain(np_stress_data['length_z'])

# Volume in cm^3
vol = (np_stress_data['length_x']*np_stress_data['length_y']*np_stress_data['length_z'])*1000000

# Wall velocity
velocity_x = np.zeros(len(stress_data)-1,)
velocity_y = np.zeros(len(stress_data)-1,)
velocity_z = np.zeros(len(stress_data)-1,)

for i in range(len(stress_data)-1):
    velocity_x[i] = np.abs((np_stress_data['length_x'][i+1]-np_stress_data['length_x'][i])/time_step)
    velocity_y[i] = np.abs((np_stress_data['length_y'][i+1]-np_stress_data['length_y'][i])/time_step)
    velocity_z[i] = np.abs((np_stress_data['length_z'][i+1]-np_stress_data['length_z'][i])/time_step)
# =============================================================================
# FIGURE
# q-p
index_n = len(stress_data) #3700
plt.figure(1)
plt.plot(p[0:index_n]/1000, q[0:index_n]/1000, color = 'navy', lw = 2)

plt.ylim(0,)
plt.xlim(0,)
plt.xlabel("Mean effective stress (p') [kPa]", fontsize = LBF)
plt.ylabel("Deviatoric stress (q) [kPa]", fontsize = LBF)
plt.tight_layout()

# q/p - strain_z
plt.figure(2)
plt.plot(strain_z[0:index_n], q[0:index_n]/p[0:index_n], color = 'navy', lw = 2)

plt.ylim(0,)
plt.xlim(0,)
plt.xlabel("Axial strain ($\epsilon_{zz}$) [%]", fontsize = LBF)
plt.ylabel(r"$\frac{q}{p'}$", fontsize = LBF)
plt.tight_layout()

# stress - strain_z
plt.figure(3)
plt.plot(strain_z[0:index_n], np_stress_data['stress_xx'][0:index_n]/1000, lw = 2, color = 'deepskyblue', label = "$\sigma'_{xx}$")
plt.plot(strain_z[0:index_n], np_stress_data['stress_yy'][0:index_n]/1000, lw = 2, color = 'cornflowerblue', label = "$\sigma'_{yy}$")
plt.plot(strain_z[0:index_n], np_stress_data['stress_zz'][0:index_n]/1000, lw = 2, color = 'navy', label = "$\sigma'_{zz}$")

plt.legend(loc = 'lower right', fontsize = LGF)
plt.xlabel("Axial strain ($\epsilon_{zz}$) [%]", fontsize = LBF)
plt.ylabel("Stress [kPa]", fontsize = LBF)
plt.tight_layout()

# stress - step number
plt.figure(4)
plt.plot(np_stress_data['step_s'][0:index_n], np_stress_data['stress_xx'][0:index_n]/1000, lw = 2, color = 'deepskyblue', label = "$\sigma'_{xx}$")
plt.plot(np_stress_data['step_s'][0:index_n], np_stress_data['stress_yy'][0:index_n]/1000, lw = 2, color = 'cornflowerblue', label = "$\sigma'_{yy}$")
plt.plot(np_stress_data['step_s'][0:index_n], np_stress_data['stress_zz'][0:index_n]/1000, lw = 2, color = 'navy', label = "$\sigma'_{zz}$")

plt.legend(loc = 'lower right', fontsize = LGF)
plt.xlabel("Step number ($N$)", fontsize = LBF)
plt.ylabel("Stress [kPa]", fontsize = LBF)
plt.tight_layout()

# Volume - step number
plt.figure(5)
plt.plot(np_stress_data['step_s'][0:index_n], vol[0:index_n]/1000, lw = 2, color = 'navy')

plt.xlabel("Step number (N)", fontsize = LBF)
plt.ylabel("Volume [$cm^3$]", fontsize = LBF)
plt.tight_layout()

# Wall Velocity - step number
plt.figure(6)
plt.plot(np_stress_data['step_s'][1:index_n], velocity_x[0:index_n], lw = 2, color = 'deepskyblue', label = "x-direction")
plt.plot(np_stress_data['step_s'][1:index_n], velocity_y[0:index_n], lw = 2, color = 'cornflowerblue', label = "y-direction")
plt.plot(np_stress_data['step_s'][1:index_n], velocity_z[0:index_n], lw = 2, color = 'navy', label = "z-direction")

plt.legend(loc = 'upper right', fontsize = LGF)
plt.xlabel("Step number (N)", fontsize = LBF)
plt.ylabel(r"Wall velocity [$\frac{m}{s}$]", fontsize = LBF)
plt.tight_layout()

plt.show()
