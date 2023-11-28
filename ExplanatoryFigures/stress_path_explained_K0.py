# Author: Tara Sassel 
# Date: 03/04/2023

# This script creates the figure that provides an overview for the stress path

import os 
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 

# ==================================================================================
# Define path to merged_data
path = r'E:\K0StrainControlledCyclic\Dry_K0_FC0p25to0p25_8m\Strain1\merged_data'

# Define Plot Fontsizes
LGF = 14   # Legend Font Size
LBF = 18    # Label Font Size
TS = 16     # Tick Size
lw1 = 3

# ==================================================================================
# Loading Data 
os.chdir(path)
stress_data = pd.read_csv('stress_data.csv')

step_interval = stress_data.step_s[1]-stress_data.step_s[0]
quarter_cycle_steps = int(5567103/(step_interval))
time_step = 5.242309e-09
quarter_cycle_time = time_step/5567103
print(quarter_cycle_time)

# ==================================================================================
# Figure 
n1 = 0
n2 = 12
plt.figure(figsize = (7,7))
plt.plot(stress_data.step_s[quarter_cycle_steps*n1:quarter_cycle_steps*n2], 
         stress_data.stress_xx[quarter_cycle_steps*n1:quarter_cycle_steps*n2]/1000, 
         color = 'black', 
         lw = lw1,
         label = r"$\sigma'_{xx}$")

plt.plot(stress_data.step_s[quarter_cycle_steps*n1:quarter_cycle_steps*n2], 
         stress_data.stress_yy[quarter_cycle_steps*n1:quarter_cycle_steps*n2]/1000,
         color = 'navy',
         lw = lw1,
         label = r"$\sigma'_{yy}$")

plt.plot(stress_data.step_s[quarter_cycle_steps*n1:quarter_cycle_steps*n2], 
         stress_data.stress_zz[quarter_cycle_steps*n1:quarter_cycle_steps*n2]/1000, 
         color = 'darkgreen',
         lw = lw1,
         label = r"$\sigma'_{zz}$")

c1 = 'lightsteelblue'
plt.text(
    -4e6,
    208,
    ha = 'center',
    va = 'center',
    s = r'208 $\Rightarrow$',
    bbox=dict(facecolor=c1, edgecolor=c1, boxstyle='round,pad =0')
)

plt.text(
    -4e6,
    160,
    ha = 'center',
    va = 'center',
    s = r'160 $\Rightarrow$',
    bbox=dict(facecolor=c1, edgecolor=c1, boxstyle='round,pad =0')
)

# ==================================================================================
# Ajust figure
ax = plt.gca()
#labels = np.arange(0, quarter_cycle_time*13, quarter_cycle_time*4)
ax.set_xticks(np.arange(0,5567103*13, 5567103))
ax.tick_params(axis='x', rotation=90)

#ax.set_xticklabels([])
#ax.set_xlabels([])

plt.legend(loc = 'lower left', fontsize = LGF)          


# Remove spines
#ax.yaxis.set_ticks_position('left')
#ax.xaxis.set_ticks_position('bottom')

plt.xlabel("Time step (N)", fontsize = LBF)
plt.ylabel("Stress [kPa]", fontsize = LBF)
plt.xlim(0,5567103*12)
plt.ylim(100,350)

ax.yaxis.set_label_coords(-.1, .5)

plt.grid()
plt.tick_params(axis='both', which='major', labelsize=TS)
plt.tight_layout()

plt.show()

