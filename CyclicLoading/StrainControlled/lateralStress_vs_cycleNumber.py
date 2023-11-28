"""
Author: Tara Sassel
Date: 11/01/2023

Increase in lateral stresses with cycle number

"""
# =================================================================================================
# Import 
import os
import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

from cyclicStrain import get_strain_info

# =================================================================================================
strainInfo = get_strain_info('E') # Drive Number example: 'E'

# Fontisze
LBF = 16    # Label Fontsize
TS = 12     # Ticksize
CBF = 14    # Colorbar Font
LGF = 8    # Legend Font 

# Customize for wanted data 
wanted_data = strainInfo[strainInfo.friction_coefficient == 0.25]

# Define label list 
label_list = [
    "$p'_0$ = 100kPa \n $\epsilon_{zz}$ = 0.1", 
    "$p'_0$ = 100kPa \n $\epsilon_{zz}$ = 0.5", 
    "$p'_0$ = 100kPa \n $\epsilon_{zz}$ = 1.0",
    "$p'_0$ = 200kPa \n $\epsilon_{zz}$ = 0.1", 
    "$p'_0$ = 200kPa \n $\epsilon_{zz}$ = 0.5", 
    "$p'_0$ = 200kPa \n $\epsilon_{zz}$ = 1.0",        
    "$p'_0$ = 300kPa \n $\epsilon_{zz}$ = 0.1", 
    "$p'_0$ = 300kPa \n $\epsilon_{zz}$ = 0.5", 
    "$p'_0$ = 300kPa \n $\epsilon_{zz}$ = 1.0"
    ]

    
ls_list = ['-','-','-','--','--', '--', ':', ':', ':']
# =================================================================================================
paths = list(wanted_data.path)
cyclic_turns = list(wanted_data.cyclic_turns)
colors = list(wanted_data.colors)

plt.figure(figsize = (10,7))

# loop trough watnted data 
for i, path in enumerate(paths):
    # change path
    os.chdir(path + r'/merged_data')

    # Load Data
    stress_data = pd.read_csv('stress_data.csv')

    step = stress_data.step_s.to_numpy().T
    stress_zz = stress_data.stress_zz.to_numpy().T

    cycle_numbers = np.uint(np.arange(0,101))
    cyclic_turn = cyclic_turns[i]
    stress = np.zeros(101,)
    for cycle in cycle_numbers:
        wanted_step = cyclic_turn + cycle*cyclic_turn*2
        index = np.argmax(step > wanted_step)
        stress[cycle] = stress_zz[index]/1000

    plt.plot(cycle_numbers, stress, color = colors[i], label = label_list[i])

# Legend
plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.25), fontsize = LGF, ncol = 3)

# Limits
plt.xlim(0,100)

# Labels
plt.ylabel('Maximum lateral stress ($\sigma_h^{max}$) [kPa]', fontsize = LBF)
plt.xlabel('Cycle number (N)', fontsize = LBF)
plt.tick_params(axis='both', which='major', labelsize=TS)

# Grid and minor ticks
plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(10))
plt.gca().xaxis.set_minor_locator(ticker.MultipleLocator(1))
plt.grid(which = 'minor', color = 'gray', ls = '--')
plt.grid(which = 'major', color = 'dimgray', ls = '-')

# Show figure
plt.tight_layout()
plt.show()