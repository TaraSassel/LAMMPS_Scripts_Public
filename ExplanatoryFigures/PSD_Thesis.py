"""
Author: Tara Sassel
Date: 23/01/2023

Particle size distribution from LAMMPS Sample for Thesis
"""
# Importing Libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
import os

path = r'C:\Users\taras\My Drive\PhD\LAMMPS\Simulations\LAMMPS\Sample_Generation\A_Sample_Generation'

TF = 20     # Title Font Size
LGF = 12    # Legend Font Size
LBF = 16    # Label Font Size
TS = 14     # Tick Size

os.chdir(path)
l1, l2, l3 = np.loadtxt('Grading_ToyouraSand.txt').T

percentage = np.zeros(len(l3))
for i in range(len(l3)):
    percentage[i] = sum(l3[0:i])

# LOAD DATA FROM HUANG 2014
os.chdir('DigitizeHuang2014')

# Load TS
colnames = ['vol', 'perc']
ts = pd.read_csv('TS.csv', names=colnames)

# Toyoura Sand 
toyouraSand = pd.read_csv('ToyouraSand.csv', names=colnames)

# FIGURE 
plt.figure(figsize=(10,5))
plt.plot(toyouraSand.vol,toyouraSand.perc,color = 'maroon',lw=3, ms = 10, ls = '',marker='o',mec='black',mfc='indianred', label = 'Laboratory sample grading from Huang et al. (2014)')
plt.plot(ts.vol,ts.perc,color = 'black',lw=2, label = 'DEM sample grading from Huang et al. (2014)')
plt.plot(l1,percentage,color = 'navy', lw=3, ls = '', marker='o',mec='black',mfc='mediumblue', label = 'DEM sample grading')

plt.legend(loc = 'lower right', fontsize = LGF)
plt.xlabel('Particle diameter [mm]', fontsize = LBF)
plt.ylabel('Passing by volume [%]', fontsize = LBF)
plt.tick_params(axis='both', which='major', labelsize=TS)
plt.ylim(0,105)
plt.xlim(0,0.5)

ax = plt.gca()
#ax.set_xscale("logit")

# Hide the right and top spines
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

# make arrows
ax.plot((1), (0), ls="", marker=">", ms=10, color="k",
        transform=ax.get_yaxis_transform(), clip_on=False)
ax.plot((0), (1), ls="", marker="^", ms=10, color="k",
        transform=ax.get_xaxis_transform(), clip_on=False)

#plt.grid()
plt.tight_layout()
plt.show()
