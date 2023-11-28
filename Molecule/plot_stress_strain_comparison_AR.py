"""
Author: Tara Sassel
Date: 14/02/2023

This scripts compares the tress strain behaviour between 
samples of diffrent AR and spherical sample with FC 0f 0.25
"""
import os
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 

from basicFunctions.get_strain import get_strain

AspectRatios = ["1p1", "1p2", "1p3", "1p4"]
label_list = ["Spherical sample", "AR = 1.1", "AR = 1.2", "AR = 1.3", "AR = 1.4", "AR = 1.1 trial sample"]
color_list = ["forestgreen", "steelblue","blue", "darkcyan","navy", "indianred"]

LBF = 14    # Label Font 
LGF = 14    # Legend Font 
TS =  12    # Tick Size

plt.figure(figsize=(10,5))
# Spherical Sample
path = rf"E:\YieldSurface\YieldSurface_Cyclicmean\200C0\merged_data"
os.chdir(path)

stress_data = pd.read_csv("stress_data.csv")
zstrain = get_strain(stress_data.length_z.to_numpy())
    
plt.plot(zstrain, stress_data.stress_zz/1000, c = color_list[0], label = label_list[0], zorder = 3)

# Molecule Samples 
for j, AR in enumerate(AspectRatios):
    i = j + 1
    path = rf"E:\Molecules\ShearingMolecule\Shear_AR{AR}_FC0p25_ISO200\merged_data"
    os.chdir(path)

    stress_data = pd.read_csv("stress_data.csv")
    zstrain = get_strain(stress_data.length_z.to_numpy())
    
    plt.plot(zstrain[1:], stress_data.stress_zz[1:]/1000, c = color_list[i], label = label_list[i], zorder = 2)

# Molecule trial sample 
#path = rf"E:\Molecules\ShearingMolecule\Shear_AR1p1_FC0p25_ISO200_trail\merged_data"
#os.chdir(path)

#stress_data = pd.read_csv("stress_data.csv")
#zstrain = get_strain(stress_data.length_z.to_numpy())
    
#plt.plot(zstrain, stress_data.stress_zz/1000, c = color_list[5], label = label_list[5], zorder = 1, ls = ":")

# Labeling
plt.xlabel("Axial strain ($\epsilon_{zz}$) [%]", fontsize = LBF)
plt.ylabel("Axial stress ($\sigma'_{zz}$) [kPa]", fontsize = LBF)
plt.legend(loc = "lower right", fontsize = LGF)
plt.gca().tick_params(which = "both", labelsize = TS)

plt.xlim(0,30)
plt.ylim(200,)
plt.grid(ls = '--', color = 'gray')
#plt.tight_layout()
plt.show()