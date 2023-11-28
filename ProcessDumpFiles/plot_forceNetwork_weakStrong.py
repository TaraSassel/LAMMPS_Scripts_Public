"""
Author: Tara Sassel
Date: 09/12/22

This sript creates a 3D reperesenation of the contact network 
"""
import os 
import numpy as np 
import pandas as pd 
import matplotlib as mpl
from matplotlib import cm
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
from matplotlib.lines import Line2D


# =============================================================================
dump_file_number = 0 # timestep of dumpfile
path = r'E:\StrainControlledCyclic\300kPa\Strain0p1\run1'
folder_list = ['atom', 'connectivity', 'stress', 'velocity']

alpha1 = 0.35
LBF = 14
# ==============================================================================
def get_RSF_NF(path: str, dump_file_number: int) -> np.array:
    """
    Calcualting resultant shear force / normal force
    """

    # Loading dump file
    folder = r'\contact'
    os.chdir(path + folder)
    contact_data = pd.read_csv(
        rf"dump{dump_file_number}.contact",
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
    RSF = np.sqrt(tfx**2+tfy**2+tfz**2)

    return X1, Y1, Z1, X2, Y2, Z2, NF, RSF, BV

# ==============================================================================
# Get contact force 
X1, Y1, Z1, X2, Y2, Z2, NF, RSF, BV = get_RSF_NF(path, dump_file_number)

NF_max = max(NF)
NF_min = min(NF)

NF_mean = np.mean(NF)


# Get slice
zmin = min(X1)
zmax = max(X1)
zl = zmax - zmin
maxBV = max(BV)

zrange1 = zl/2 - maxBV
zrange2 = zl/2 + maxBV

d = {"X1":X1, "Y1":Y1, "Z1":Z1, "X2":X2, "Y2":Y2, "Z2":Z2, "NF":NF }
df = pd.DataFrame(data = d)
df = df[(df.X1 > zrange1) & (df.X1 < zrange2)]
X1, Y1, Z1, X2, Y2, Z2, NF = df.to_numpy().T
print("Number of contacts in section")
print(len(NF))
# # # the histogram of the data
# n, bins, patches = plt.hist(NF, 50, density=True, facecolor='g', alpha=0.75)
# plt.show()

normalized_NF = np.zeros((len(NF),))
transparancy_value2 = np.zeros((len(NF),))
zorder_value = np.zeros((len(NF),))
lw_normalized = np.zeros((len(NF),))
counter = 0 
for i, NF_value in enumerate(NF):
    if NF_value < NF_mean:
        transparancy_value2[i] = alpha1
        normalized_NF[i] = (NF_value - NF_mean)/(NF_mean - NF_min)
        lw_normalized[i] = (NF_value - NF_mean)/(NF_mean - NF_min)+1
        zorder_value[i] = 1
    else: 
        normalized_NF[i] = (NF_value - NF_mean)/(NF_max - NF_mean)
        lw_normalized[i] = (NF_value - NF_mean)/(NF_mean - NF_min)+1
        transparancy_value2[i] = 1
        zorder_value[i] = 2
        counter += 1

# Define transparancy range
transparancy_value =  (NF - NF_min)/(NF_max - NF_min)
print("Number of strong contacts in section")
print(counter)
# map range
norm = mpl.colors.LogNorm(vmin=NF_min, vmax=NF_max)
norm = mpl.colors.Normalize(vmin=NF_min, vmax=NF_max)

# Figure 
fig, ax = plt.subplots(1, 1, figsize = (7,7))
# Hide the right and top spines
ax.spines[['right', 'top']].set_visible(False)

for i in range(len(X1)):
    if NF[i] > NF_mean:
        c1 = 'maroon'
    else:
        c1 = 'forestgreen'
    plt.plot([Y1[i], Y2[i]],[Z1[i], Z2[i]], alpha = 1, c=c1, lw = lw_normalized[i], zorder = zorder_value[i]) #transparancy_value[i]

plt.xlabel("y-axis [m]", fontsize = LBF)
plt.ylabel("z-axis [m]", fontsize = LBF)

custom_lines = [Line2D([0], [0], color="forestgreen", lw=4, alpha = alpha1),
                Line2D([0], [0], color="maroon", lw=4)]

ax.legend(custom_lines, [f'$F_N$ < {NF_mean:.3g} [N]', f'$F_N \leqq$  {NF_mean:.3g} [N]'], loc = 'lower left')               
plt.show()

