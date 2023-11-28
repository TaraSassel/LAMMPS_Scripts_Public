import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D

from basicFunctions.MechanicalCoordinationNumber import get_mechCoord

amplitudes = [[5,10,20],[10,20,40],[15,30,60]]
stress_list = [100,200,300]
colorlist = ['forestgreen','royalblue','indianred']
ls_list = [':','--','-',':','--','-',':','--','-']

# Define Plot Fontsizes
TF = 20     # Title Font Size
LGF = 16    # Legend Font Size
LBF = 14    # Label Font Size
TS = 12     # Tick Size
ms1 = 5     # Maker size


fig, ax = plt.subplots(1, 2, figsize = (10,7)) # Initiating Figure

for s, stress in enumerate(stress_list):
    stress_amplitudes = amplitudes[s]
    for i, amp in enumerate(stress_amplitudes):
        # Chaning path
        path = fr'G:\PhD_Data_Back_Up\LAMMPS\CyclicLoading\ConstantP\TX{stress}_FC0p25to0p25_amp{amp}\Merged'
        os.chdir(path)

        # Mechanical Coordination Number
        mech_coord = get_mechCoord(path + r'\SortedData\0_StartingPos\connectivity', ['id','diameter','coord'])


        # Coordination number
        os.chdir(path)
        coord_data = pd.read_csv('shear_coord.txt', header = None, names = ['step_number', 'coord'], index_col = False, delimiter = " ")

        # Position File
        os.chdir(path)
        dfP = pd.read_csv('positions.txt',index_col = None, header = None, delimiter = " ")
        N0, L, N1, U = dfP.to_numpy().T
        cycle_n = np.arange(len(N0))

        # Plotting
        ax[0].plot(np.arange(0,50,1),mech_coord.mechanical_coord[:50], ls_list[i], c = colorlist[s])
        ax[1].plot(cycle_n,coord_data.coord[N0.astype(int)], ls = ls_list[i], c = colorlist[s])


for i in range(2):
    # Adjust Figure
    ax[i].set_xlim(0,50)
    ax[i].set_ylim(4,5.2)
    ax[i].tick_params(axis='both', which='major', labelsize=TS)

    # Hide the right and top spines
    ax[i].spines['right'].set_visible(False)
    ax[i].spines['top'].set_visible(False)
    # make arrows
    ax[i].plot((1), (0), ls="", marker=">", ms=10, color="k",
            transform=ax[i].get_yaxis_transform(), clip_on=False)
    ax[i].plot((0), (1), ls="", marker="^", ms=10, color="k",
            transform=ax[i].get_xaxis_transform(), clip_on=False)

# Figure Labels
ax[0].set_ylabel('Mechanical coordination number', fontsize = LBF)
ax[1].set_ylabel('Coordination number', fontsize = LBF)

ax[0].set_xlabel('Cycle Number (N) \n (a)', fontsize = LBF)
ax[1].set_xlabel('Cycle Number (N) \n (b)', fontsize = LBF)

# Legend
patch1 = mpatches.Patch(color=colorlist[2], label="p' = 300kPa")
patch2 = mpatches.Patch(color=colorlist[1], label="p' = 200kPa")
patch3 = mpatches.Patch(color=colorlist[0], label="p' = 100kPa")

patchz1 = mlines.Line2D([],[], c='gray', ls=':',lw=2, label="$\zeta = 0.05$")
patchz2 = mlines.Line2D([],[], c='gray', ls='--',lw=2, label="$\zeta = 0.1$")
patchz3 = mlines.Line2D([],[], c='gray', ls='-',lw=2, label="$\zeta = 0.2$")

la = ax[0].legend(handles=[patch1,patch2,patch3],loc='lower left',fontsize = LGF)
lb = ax[1].legend(handles=[patchz1,patchz2,patchz3],loc='upper right',fontsize = LGF)

plt.gcf().subplots_adjust(bottom=0.15)
plt.tight_layout()
plt.show()
