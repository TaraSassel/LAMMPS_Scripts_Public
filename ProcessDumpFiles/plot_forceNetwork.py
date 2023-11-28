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



# =============================================================================
dump_file_number = 0 # timestep of dumpfile
path = r'E:\Monotonic_Undrained\300kPa_90\Cycle50\run1'
folder_list = ['atom', 'connectivity', 'stress', 'velocity']


# ==============================================================================
def get_RSF_NF(path: str, dump_file_number: int) -> np.array:
    """
    Calcualting resultant shear force / normal force
    """

    # Loading dump file
    folder = r'\contact'
    os.chdir(path + folder)
    contact_data = pd.read_csv(
        "dump0.contact",
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

# # # the histogram of the data
# n, bins, patches = plt.hist(NF, 50, density=True, facecolor='g', alpha=0.75)
# plt.show()

NF_max = max(NF)
NF_min = min(NF)
print(NF_min)
print(NF_max)

# Define transparancy range
transparancy_value =  (NF - NF_min)/(NF_max - NF_min)

# map range
norm = mpl.colors.LogNorm(vmin=NF_min, vmax=NF_max)
norm = mpl.colors.Normalize(vmin=NF_min, vmax=NF_max)

# Figure 
fig, ax = plt.subplots(1, 1, subplot_kw={'projection': '3d'}, figsize = (10,10))
ax.set_axis_off()

for i in range(len(X1)):
    plt.plot([X1[i], X2[i]], [Y1[i], Y2[i]],zs=[Z1[i], Z2[i]], alpha = transparancy_value[i], c=cm.plasma(norm(NF[i])))

fig.colorbar(plt.cm.ScalarMappable(norm=mpl.colors.Normalize(vmin=NF_min, vmax=NF_max), cmap=cm.plasma),
             ax=ax, label="Normalized", shrink=0.5)
plt.show()

