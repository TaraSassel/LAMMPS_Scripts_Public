"""
Author: Tara Sassel
Date: 12/01/2023
This strain plots the stress strain loops for the K0 strain controlled cyclic data 
"""

# Imports 
import re 
import os 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# Fontisze
LBF = 16    # Label Fontsize
TS = 14     # Ticksize
LGF = 14    # Legend Font 
lw1 = 2 

# =================================================================================================

path = r'E:\StrainControlledCyclic\300kPa_FC0p15\Strain1'
N = 101

# Get cyclic turns 
os.chdir(path + r'\template')
for line in open('continue_cyclic.in'):
    match = re.search('cyclicturns equal (\d+)', line)
    if match:
        cyclicturns = int(match.group(1))
        print(cyclicturns)


# Load Data
os.chdir(path + r'\merged_data')
stress_data = pd.read_csv('stress_data.csv')

# Adapt Data
cycle_steps_max = np.arange(cyclicturns,cyclicturns*2*N, cyclicturns*2)
cycle_steps_max = [round(val, -4) for val in cycle_steps_max]

stress_xx_max = stress_data.stress_xx[stress_data['step_s'].isin(cycle_steps_max)].to_numpy()/1000
stress_yy_max = stress_data.stress_zz[stress_data['step_s'].isin(cycle_steps_max)].to_numpy()/1000
stress_zz_max = stress_data.stress_zz[stress_data['step_s'].isin(cycle_steps_max)].to_numpy()/1000
ratio_max = stress_xx_max/stress_zz_max

cycle_steps_min = np.arange(0,cyclicturns*2*N+1, cyclicturns*2)
cycle_steps_min = [round(val, -4) for val in cycle_steps_min]

stress_xx_min = stress_data.stress_xx[stress_data['step_s'].isin(cycle_steps_min)].to_numpy()/1000
stress_yy_min = stress_data.stress_zz[stress_data['step_s'].isin(cycle_steps_min)].to_numpy()/1000
stress_zz_min = stress_data.stress_zz[stress_data['step_s'].isin(cycle_steps_min)].to_numpy()/1000
ratio_min = stress_xx_min/stress_zz_min
# =================================================================================================
# Figure
plt.figure(figsize=(10,5))
plt.plot(np.arange(0,len(ratio_max),1), ratio_max, c = 'navy', lw = 2, marker = 'v', markevery = 5)
plt.plot(np.arange(0,len(ratio_min),1), ratio_min, c = 'navy', lw = 2, marker = '^', markevery = 5)

plt.hlines(y = 1, xmin = -5, xmax = 105, ls = '--', color = 'black')
plt.xlim(-5, 105)

ax = plt.gca()


# Labels
plt.ylabel(r"Stress ratio $(\frac{\sigma'_{zz}}{\sigma'_{xx}})$", fontsize = LBF)
plt.xlabel('Strain [%]', fontsize = LBF)

plt.tick_params(axis='both', which='major', labelsize=TS)

# Grid and minor ticks
#plt.gca().yaxis.set_minor_locator(ticker.MultipleLocator(10))
#plt.gca().yaxis.set_major_locator(ticker.MultipleLocator(50))
plt.grid(which = 'minor', color = 'gray', ls = '--')
plt.grid(which = 'major', color = 'dimgray', ls = '-')
plt.tight_layout()
plt.show()