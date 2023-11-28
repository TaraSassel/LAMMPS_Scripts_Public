"""
Author: Tara Sassel
Date: 14/07/20

Creates figure of stress vs time step saved to selected directory
"""
# Importing Libraries
import numpy as np
import sys
import os
import matplotlib.pyplot as plt
import fnmatch
from PIL import Image

#===============================================================================
# Define Plot Fontsizes
TF = 25     # Title Font Size
LGF = 19    # Legend Font Size
LBF = 23    # Label Font Size
TS = 17     # Tick Size
width_in_inches = 20
height_in_inches = 10

# Change Directory
path  = None # path to directory with txt files
os.chdir(path)

#===============================================================================

# Names of Files
for (dirpath, dirnames, filenames) in os.walk(path):
    for file in filenames:
        if file.endswith(".txt"):
            if fnmatch.fnmatch(file,"*stress*"):
                stress_file = file
                print(stress_file)
            if fnmatch.fnmatch(file,"*void*"):
                void_file = file
                print(void_file)

# Mean Stresses
print('Processing Stresses')
step_s, stress_xx, stress_yy, stress_zz, stress_xy, stress_xz, stress_yz, length_x, length_y, length_z = np.loadtxt(stress_file).T

delta_xx = np.zeros(len(stress_xx))
delta_yy = np.zeros(len(stress_xx))
delta_zz = np.zeros(len(stress_xx))

for i in range(len(stress_xx)):

    delta_xx[i] =  length_x[0] - length_x[i]
    delta_yy[i] =  length_y[0] - length_y[i]
    delta_zz[i] =  length_z[0] - length_z[i]

xstrain =delta_xx*100/length_z[0]
ystrain =delta_yy*100/length_z[0]
zstrain =delta_zz*100/length_z[0]

delta_xstrain = xstrain[0] - xstrain
delta_ystrain = ystrain[0] - ystrain
delta_zstrain = zstrain[0] - zstrain

# Void Ratio
print('Processing Void Ratio')
step_v, void_ratio = np.loadtxt(void_file).T

# Figure 1 ---------------------------------------------------------------------
f1 = plt.figure(1,figsize=(width_in_inches, height_in_inches))

# fig, ax = plt.subplots()
line1 = plt.plot(step_s,stress_xx/1000, color = 'red',linewidth = 3)
line2 = plt.plot(step_s,stress_yy/1000, color = 'blue')
line3 = plt.plot(step_s,stress_zz/1000, color = 'green')



plt.xlabel('Step Number ($N$)', fontsize = LBF)
plt.ylabel('Stress [kPa]', fontsize = LBF)

plt.legend([r'$\sigma_{xx}$',r'$\sigma_{yy}$',r'$\sigma_{zz}$'],loc='center left', bbox_to_anchor=(1, 0.5), fontsize = LGF)
plt.tick_params(axis='both', which='major', labelsize=TS)

plt.grid()

plt.tight_layout()
plt.savefig("check_stress.png")

# Figure 2 ---------------------------------------------------------------------
f2 = plt.figure(2,figsize=(width_in_inches, height_in_inches))
line1 = plt.plot(step_v,void_ratio, color = 'black',linewidth = 3)
plt.xlabel('Step Number ($N$)', fontsize = LBF)
plt.ylabel('Void Ratio ($e$)', fontsize = LBF)
plt.tick_params(axis='both', which='major', labelsize=TS)

plt.grid()

plt.tight_layout()
plt.savefig("check_void_ratio.png")

# Show  ---------------------------------------------------------------------
#plt.show()
Image.open("check_stress.png").show()
Image.open("check_void_ratio.png").show()