# Author: Tara Sassel 
# Date: 03/04/2023

# This script creates the figure that provides an overview for the stress path

import os 
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 

# ==================================================================================
# Define path to merged_data
path = r'E:\StrainControlledCyclic\300kPa\Strain1\merged_data'

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
quarter_cycle_steps = int(5568485/(step_interval))
time_step = 5.24231e-09
quarter_cycle_time = time_step/5568485
print(quarter_cycle_time)

# ==================================================================================
# Figure 
n1 = 0
n2 = 12
plt.figure(figsize = (7,7))
plt.plot(stress_data.step_s[quarter_cycle_steps*n1:quarter_cycle_steps*n2], 
         stress_data.length_x[quarter_cycle_steps*n1:quarter_cycle_steps*n2]*1000, 
         color = 'black', 
         lw = lw1,
         label = r"x-direction",
         marker = 'x',
         markevery = quarter_cycle_steps,
         ms = 9)

plt.plot(stress_data.step_s[quarter_cycle_steps*n1:quarter_cycle_steps*n2], 
         stress_data.length_y[quarter_cycle_steps*n1:quarter_cycle_steps*n2]*1000,
         color = 'navy',
         lw = lw1,
         label = r"y-direction")

plt.plot(stress_data.step_s[quarter_cycle_steps*n1:quarter_cycle_steps*n2], 
         stress_data.length_z[quarter_cycle_steps*n1:quarter_cycle_steps*n2]*1000, 
         color = 'darkgreen',
         lw = lw1,
         label = r"z-direction")

# ==================================================================================
# Ajust figure
ax = plt.gca()
ax.set_xticks(np.arange(0,5567103*13, 5567103))
ax.tick_params(axis='x', rotation=90)

plt.legend(loc = 'upper right', fontsize = LGF)          

plt.xlabel("Time step (N)", fontsize = LBF)
plt.ylabel("Wall position [mm]", fontsize = LBF)
plt.xlim(0,5567103*12)

ax.yaxis.set_label_coords(-.11, .5)

plt.grid()
plt.tick_params(axis='both', which='major', labelsize=TS)
plt.tight_layout()
plt.show()

