"""
Author: Tara Sassel
Date: 06/02/2023

Script for stress strain loops for cyclic mean data
"""
# Imports
import os 
import numpy as np 
import pandas as pd 
import seaborn as sns 
import matplotlib.pyplot as plt 
from matplotlib import cm

from basicFunctions.get_strain import get_strain
from basicFunctions.get_qp import get_qp

# =============================================================================
N = 51

# Fonts 
TF = 12      # Title Font 
TS = 12     # Tick Size
LBF = 14    # Label Font 
LGF = 16    # Legend Font
lw1 = 2     # Line Width 
CBF = 14    # Color Bar Font 

# Path 
path1 = r'E:\CyclicLoading\Cyclicmean\TX300_FC0p25to0p25_amp15\merged_data'
path2 = r'E:\CyclicLoading\Cyclicmean\TX300_FC0p25to0p25_amp30\merged_data'
path3 = r'E:\CyclicLoading\Cyclicmean\TX300_FC0p25to0p25_amp60\merged_data'
path4 = r'E:\CyclicLoading\Cyclicmean\TX300_FC0p25to0p25_amp90\merged_data'

path_list = [path1, path2, path3, path4]
a1 = [0,0,1,1]
a2 = [0,1,0,1]

title_list = [
    "$p'^{av}$ = 300kPa $q^{ampl}$ = 15kPa",
    "$p'^{av}$ = 300kPa $q^{ampl}$ = 30kPa",
    "$p'^{av}$ = 300kPa $q^{ampl}$ = 60kPa",
    "$p'^{av}$ = 300kPa $q^{ampl}$ = 90kPa"
    ]
xlabel_list = [
    'Axial strain ($\epsilon_{zz}$) [%] \n (a)',
    'Axial strain ($\epsilon_{zz}$) [%] \n (b)',
    'Axial strain ($\epsilon_{zz}$) [%] \n (c)',
    'Axial strain ($\epsilon_{zz}$) [%] \n (d)'
]

fig, ax = plt.subplots(2, 2, figsize = (14,8))
for pn, path in enumerate(path_list):
    os.chdir(path)
    stress_data = pd.read_csv('stress_data.csv')


    # Calculating cycle length
    time_step = 5.242309e-09
    period = 0.25
    cycle_length = int(period/(time_step))
    cycle_steps = cycle_length/(10000)
    wanted_interval = np.arange(0, (N+1)*cycle_steps, cycle_steps).astype(np.int64)

    stress_zz = stress_data.stress_zz.to_numpy().T
    zstrain = get_strain(stress_data.length_z.to_numpy().T)
    q, p = get_qp(stress_data)

    # Figure 

    ax[a1[pn],a2[pn]].set_prop_cycle('color',[cm.bone(j) for j in np.linspace(0, 1, N+1)]) # added 5 because I dont want to go to white # change color here gray
    
    

    for k in np.arange(0,N,1): 
        start = wanted_interval[k]
        finish = wanted_interval[k+1]

        if k == 1:
            colors = 'red'
        else:
            colors = 'green'
        indicies = np.arange(start,finish,1)
        strain = zstrain[indicies]
        stress = stress_zz[indicies]/1000


    
        ax[a1[pn],a2[pn]].plot(strain, stress, lw = lw1, zorder = 1)
        ax[a1[pn],a2[pn]].set_xlabel(xlabel_list[pn], fontsize = LBF)
        ax[a1[pn],a2[pn]].set_ylabel("Axial stress ($\sigma'_{zz}$) [kPa]", fontsize = LBF)
        ax[a1[pn],a2[pn]].set_title(title_list[pn],fontsize = TF)

        if pn == 3:
            if k == 0: 
                quater_interval = int(cycle_steps/4)
                plt.vlines(
                    x = strain[quater_interval], 
                    ymin = 300, 
                    ymax = 390, 
                    ls = '--', 
                    lw = 1, 
                    color = 'black'
                )

                plt.vlines(
                    x = strain[quater_interval*3+70], 
                    ymin = 210, 
                    ymax = 300, 
                    ls = '--', 
                    lw = 1, 
                    color = 'black'
                )
                ca = 'forestgreen' # color annotation 
                amp = strain[quater_interval] - strain[quater_interval*3+20]
                plt.arrow(strain[quater_interval*3+70], 300, amp, 0, head_width=3, head_length=0.03, linewidth=1, color=ca, length_includes_head=True)
                plt.arrow(strain[quater_interval], 300, -amp, 0, head_width=3, head_length=0.03, linewidth=1, color=ca, length_includes_head=True, zorder = 2)
                plt.text(0.2, 295, '$\epsilon_{zz}^{ampl}$', ha = 'center', va = 'top', color = ca, fontsize = 12)

left  = 0.125  # the left side of the subplots of the figure
right = 0.9    # the right side of the subplots of the figure
bottom = 0.1   # the bottom of the subplots of the figure
top = 0.9      # the top of the subplots of the figure
wspace1 = 0.5   # the amount of width reserved for blank space between subplots
hspace1 = 0.5   # the amount of height reserved for white space between subplots
plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=wspace1, hspace=hspace1)


# Colorbar
fig.subplots_adjust(right=0.8)
sm = plt.cm.ScalarMappable(cmap=cm.bone, norm=plt.Normalize(vmin=0, vmax=N))
cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
cb = fig.colorbar(sm, cax=cbar_ax)
cb.ax.tick_params(labelsize=TS)
cb.set_label('Cycle number (N)', fontsize = CBF)

#plt.tight_layout()
plt.show()

