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
path = r'F:\CyclicLoading\Cyclicmean_Undrained\TX300_FC0p1to0p25_amp15_Capability_MaxRate20\merged_data' # Path to merged_data

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
index_n = len(stress_data) #3700
fig, ax = plt.subplots(2,3, figsize = (15,8))

# q-p
ax[0,0].plot(p[0:index_n]/1000, q[0:index_n]/1000, color = 'navy', lw = 2)

ax[0,0].set_ylim(0,)
ax[0,0].set_xlim(0,)
ax[0,0].set_xlabel("Mean effective stress (p') [kPa]", fontsize = LBF)
ax[0,0].set_ylabel("Deviatoric stress (q) [kPa]", fontsize = LBF)

# q/p - strain_z
ax[1,0].plot(strain_z[0:index_n], q[0:index_n]/p[0:index_n], color = 'navy', lw = 2)

ax[1,0].set_ylim(0,)
ax[1,0].set_xlim(0,)
ax[1,0].set_xlabel("Axial strain ($\epsilon_{zz}$) [%]", fontsize = LBF)
ax[1,0].set_ylabel(r"$\frac{q}{p'}$", fontsize = LBF)


# stress - strain_z
ax[0,1].plot(strain_z[0:index_n], np_stress_data['stress_xx'][0:index_n]/1000, lw = 2, color = 'deepskyblue', label = "$\sigma'_{xx}$")
ax[0,1].plot(strain_z[0:index_n], np_stress_data['stress_yy'][0:index_n]/1000, lw = 2, color = 'cornflowerblue', label = "$\sigma'_{yy}$")
ax[0,1].plot(strain_z[0:index_n], np_stress_data['stress_zz'][0:index_n]/1000, lw = 2, color = 'navy', label = "$\sigma'_{zz}$")

ax[0,1].legend(loc = 'lower right', fontsize = LGF)
ax[0,1].set_xlabel("Axial strain ($\epsilon_{zz}$) [%]", fontsize = LBF)
ax[0,1].set_ylabel("Stress [kPa]", fontsize = LBF)

# stress - step number
ax[1,1].plot(np_stress_data['step_s'][0:index_n], np_stress_data['stress_xx'][0:index_n]/1000, lw = 2, color = 'deepskyblue', label = "$\sigma'_{xx}$")
ax[1,1].plot(np_stress_data['step_s'][0:index_n], np_stress_data['stress_yy'][0:index_n]/1000, lw = 2, color = 'cornflowerblue', label = "$\sigma'_{yy}$")
ax[1,1].plot(np_stress_data['step_s'][0:index_n], np_stress_data['stress_zz'][0:index_n]/1000, lw = 2, color = 'navy', label = "$\sigma'_{zz}$")

ax[1,1].legend(loc = 'lower right', fontsize = LGF)
ax[1,1].set_xlabel("Step number ($N$)", fontsize = LBF)
ax[1,1].set_ylabel("Stress [kPa]", fontsize = LBF)

# Volume - step number
ax[0,2].plot(np_stress_data['step_s'][0:index_n], vol[0:index_n]/1000, lw = 2, color = 'navy')

ax[0,2].set_xlabel("Step number (N)", fontsize = LBF)
ax[0,2].set_ylabel("Volume [$cm^3$]", fontsize = LBF)

# Wall Velocity - step number
ax[1,2].plot(np_stress_data['step_s'][1:index_n], velocity_x[0:index_n], lw = 2, color = 'deepskyblue', label = "x-direction")
ax[1,2].plot(np_stress_data['step_s'][1:index_n], velocity_y[0:index_n], lw = 2, color = 'cornflowerblue', label = "y-direction")
ax[1,2].plot(np_stress_data['step_s'][1:index_n], velocity_z[0:index_n], lw = 2, color = 'navy', label = "z-direction")

ax[1,2].legend(loc = 'upper right', fontsize = LGF)
ax[1,2].set_xlabel("Step number (N)", fontsize = LBF)
ax[1,2].set_ylabel(r"Wall velocity [$\frac{m}{s}$]", fontsize = LBF)

plt.subplots_adjust(left=0.1,
                    bottom=0.1,
                    right=0.9,
                    top=0.9,
                    wspace=0.4,
                    hspace=0.4)
fig.tight_layout()
plt.show()
