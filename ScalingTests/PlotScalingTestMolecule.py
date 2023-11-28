# Plot Scaling Test Info
# has to be run after get_Info
import os
import fnmatch
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import matplotlib.patches as mpatches

path1 = r'E:\Molecules\ScalingTestMolecules\6k_Sample'
path2 = r'E:\Molecules\ScalingTestMolecules\22k_Sample'
path3 = r'E:\Molecules\ScalingTestMolecules\22k_Sample_Cyclic'
path4 = r'E:\Molecules\ScalingTestMolecules\6k_Sample_Cyclic_AR1p1'

lw1 = 2
LBF = 14
TS = 12    # Tick Size
LGF = 12    # Legend Font Size

def get_data(path):
    os.chdir(path + "\\ScalingTestInfo")

    for (dirpath, dirnames, filenames) in os.walk(path + "\\ScalingTestInfo"):
        for file in filenames:
            if fnmatch.fnmatch(file,"*.txt*"):
                file_name = file
                print(file_name)

    df = pd.read_csv(file_name,delimiter = ' ')
    df = df.sort_values(by=['NCPUs'])
    return df

df1 = get_data(path1)
df2 = get_data(path2)
df3 = get_data(path3)
df4 = get_data(path4)

# =================================================================================================
# Meomory Figure 

plt.figure(1,figsize=(7, 7) )
ax1 = plt.gca()
ax1.plot(df1['NCPUs'],df1['Memory'], lw=lw1,c ='darkgreen', ls = '-', label = '6k Clumps ISO')
ax1.plot(df2['NCPUs'],df2['Memory'], lw=lw1,c ='royalblue', ls = '-',  label = '22k Clumps ISO')
ax1.plot(df3['NCPUs'],df3['Memory'], lw=lw1,c ='indianred', ls = '-',  label = '22k Clumps Cyclic AR1.4')
ax1.plot(df4['NCPUs'],df4['Memory'], lw=lw1,c ='darkorange', ls = '-',  label = '6k Clumps Cyclic AR1.1')

ax1.legend(loc= 'upper right', fontsize = LGF)

ax1.set_xlabel('Number of CPUs (NCPUs)',fontsize = LBF)
ax1.set_ylabel('Max memory [GB]',fontsize = LBF)

ax1.set_ylim(0,)

ax1.set_xticks([12,24,48,96,128,256,512])
ax1.set_xlim([1,512])
ax1.grid(which='major', axis='both', ls = '--')
plt.tick_params(axis='both', which='major', labelsize=TS)
plt.tight_layout()
# =================================================================================================
# Walltime Figure

plt.figure(2,figsize=(7, 7) )
ax1 = plt.gca()
ax1.plot(df1['NCPUs'],df1['Walltime']/60, lw=lw1,c ='darkgreen', ls = '-', label = '6k Clumps ISO')
ax1.plot(df2['NCPUs'],df2['Walltime']/60, lw=lw1,c ='royalblue', ls = '-',  label = '22k Clumps ISO')
ax1.plot(df3['NCPUs'],df3['Walltime']/60, lw=lw1,c ='indianred', ls = '-',  label = '22k Clumps Cyclic AR 1.4')
ax1.plot(df4['NCPUs'],df4['Walltime']/60, lw=lw1,c ='darkorange', ls = '-',  label = '6k Clumps Cyclic AR1.1')


ax1.legend(loc= 'upper right', fontsize = LGF)

ax1.set_xlabel('Number of CPUs (NCPUs)',fontsize = LBF)
ax1.set_ylabel('Walltime [min]',fontsize = LBF)

ax1.set_ylim(0,)

ax1.set_xticks([12,24,48,96,128,256,512])
ax1.set_xlim([1,512])
ax1.grid(which='major', axis='both', ls = '--')
plt.tick_params(axis='both', which='major', labelsize=TS)
plt.tight_layout()

# =================================================================================================
# Particle Number Figure

plt.figure(3,figsize=(7, 7))
ax1 = plt.gca()
ax1.plot(df1['NCPUs'],df1['Nlocal']/60, lw=lw1,c ='darkgreen', ls = '-',  label = '6k Clumps Local')
ax1.plot(df1['NCPUs'],df1['Nghost']/60, lw=lw1,c ='darkgreen', ls = ':',  label = '6k Clumps Ghost')
ax1.plot(df2['NCPUs'],df2['Nlocal']/60, lw=lw1,c ='royalblue', ls = '-',  label = '22k Clumps Local')
ax1.plot(df2['NCPUs'],df2['Nghost']/60, lw=lw1,c ='royalblue', ls = ':',  label = '22k Clumps Ghost')
ax1.plot(df3['NCPUs'],df3['Nlocal']/60, lw=lw1,c ='indianred', ls = '--',  label = '22k Clumps Cyclic Local')
ax1.plot(df3['NCPUs'],df3['Nghost']/60, lw=lw1,c ='indianred', ls = ':',  label = '22k Clumps Cyclic Ghost')
ax1.plot(df4['NCPUs'],df4['Nlocal']/60, lw=lw1,c ='darkorange', ls = '--',  label = '6k Clumps Cyclic AR1.1 Local')
ax1.plot(df4['NCPUs'],df4['Nghost']/60, lw=lw1,c ='darkorange', ls = ':',  label = '6k Clumps Cyclic AR1.1 Ghost')

ax1.set_xlabel('Number of CPUs (NCPUs)',fontsize = LBF)
ax1.set_ylabel('Number of Particles',fontsize = LBF)


# Creating Legends
lines1 = mlines.Line2D([], [], color='gray', ls = '-', lw = lw1, label='Local')
lines2 = mlines.Line2D([], [], color='gray', ls = ':', lw = lw1, label='Ghost')

first_legend = ax1.legend(handles=[lines1,lines2],loc='upper right', fontsize = LGF)

_6k_patch = mpatches.Patch(color='darkgreen', label='6k Clump Sample ISO')
_22k_patch = mpatches.Patch(color='royalblue', label='22k Clump Sample ISO')
_22k_cyc_patch = mpatches.Patch(color='indianred', label='22k Clump Sample Cyclic AR 1.4')
_6k_cyc_patch = mpatches.Patch(color='darkorange', label='6k Clump Sample Cyclic AR 1.1')


second_legend = ax1.legend(handles=[_6k_patch,_22k_patch, _22k_cyc_patch, _6k_cyc_patch],loc='upper center', fontsize = LGF)
plt.gca().add_artist(first_legend)

ax1.set_ylim(0,)
#
ax1.set_xticks([12,24,48,96,128,256,512])
ax1.set_xlim([1,512])
ax1.grid(which='major', axis='both', ls = '--')


# =================================================================================================

plt.show()
