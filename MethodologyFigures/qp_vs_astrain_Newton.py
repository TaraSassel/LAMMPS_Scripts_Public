"""
Author: Tara Sassel
Date: 24/01/2023

Figure for qp vs axial strain to compare newton on to newton off
"""
# Imports
import os 
import pandas as pd 
import matplotlib.pyplot as plt

from basicFunctions.get_qp import get_qp

# Fonts
TF = 20     # Title Font Size
LGF = 12    # Legend Font Size
LBF = 16    # Label Font Size
TS = 14     # Tick Size
lw1 = 2     # Line width 


# Paths 
path_TX_FC0p1_NOn = r'F:\PhD_Data_Back_Up\LAMMPS\Random_Packing\TX Shear\TXShear100kPa_fromFC0p1to0p1\merged_data'
path_TX_FC0p1_NOff = r'F:\PhD_Data_Back_Up\LAMMPS\Random_Packing\TX Shear\NewtonOff\TXShear100kPa_fromFC0p1to0p1\merged_data'

path_TX_FC0p25_NOn = r'F:\PhD_Data_Back_Up\LAMMPS\Random_Packing\TX Shear\TXShear100kPa_fromFC0p1to0p25\merged_data'
path_TX_FC0p25_NOff = r'F:\PhD_Data_Back_Up\LAMMPS\Random_Packing\TX Shear\NewtonOff\TXShear100kPa_fromFC0p1to0p25\merged_data'

paths = [path_TX_FC0p1_NOn, path_TX_FC0p1_NOff, path_TX_FC0p25_NOn, path_TX_FC0p25_NOff]
label_list = [
    'Newton On with $\mu = 0.1$', 
    'Newton Off with $\mu = 0.1$', 
    'Newton On with $\mu = 0.25$', 
    'Newton Off with $\mu = 0.25$'
    ]
color_list = ['indianred','maroon','lightgreen','forestgreen']
ls_list = ['-','--','-','--']
lw_list = [4,2,4,2]

plt.figure(figsize = (10,5))
for i, path in enumerate(paths):
    print(path)
    os.chdir(path)
    stress_data = pd.read_csv("stress_data.csv")
    q, p = get_qp(stress_data)
    
    # strain
    length_z = stress_data.length_z.to_numpy().T
    zstrain = (length_z[0] - length_z)/length_z[0] 
    zstrain = zstrain*100 # to percentage

    # Figure
    plt.plot(zstrain, q/p, label = label_list[i], c = color_list[i], ls = ls_list[i], lw = lw_list[i])

# Annoate
plt.legend(loc = 'lower right', fontsize = LGF)
plt.xlabel('Axial strain ($\epsilon_{zz}$) [%]', fontsize = LBF)
plt.ylabel('q/p ', fontsize = LBF)
plt.xlim(0,5)
plt.ylim(0,)

ax = plt.gca()

# Hide the right and top spines
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

# make arrows
ax.plot((1), (0), ls="", marker=">", ms=10, color="k",
        transform=ax.get_yaxis_transform(), clip_on=False)
ax.plot((0), (1), ls="", marker="^", ms=10, color="k",
        transform=ax.get_xaxis_transform(), clip_on=False)

plt.tick_params(axis='both', which='major', labelsize=TS)
plt.show()