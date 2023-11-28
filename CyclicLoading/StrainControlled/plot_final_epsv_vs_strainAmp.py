"""
Author: Tara Sassel 
Date: 20/02/2023

This script is to recreate Figure 7 by Kang et al. (2016)
using my strain controlled DEM data
Strain-Controlled Cyclic Simple Shear Tests on Sand with
Radial Strain Measurements

"""
# IMPORTS 
import os 
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt 
from matplotlib.lines import Line2D

from cyclicStrain import get_strain_info

drive_letter = "E"
strainInfo =  get_strain_info("E")

wanted_strainInfo = strainInfo[strainInfo.friction_coefficient == 0.25]

# Define Fonts
LBF = 14
LGF = 12
TS = 12

# Function v strain: 
def get_eps_v(stress_data: pd.DataFrame) -> np.array:
    """
    This function calculates the volumetric strain 
    in %. The input is the merged stress data as *.csv
    """
    length_x = stress_data.length_x.to_numpy().T
    length_y = stress_data.length_y.to_numpy().T
    length_z = stress_data.length_z.to_numpy().T

    eps_x =  (length_x[0]-length_x)/length_x[0]
    eps_y =  (length_y[0]-length_y )/length_y[0]
    eps_z =  (length_z[0]-length_z)/length_z[0]

    eps_v = (eps_x + eps_y + eps_z)*100

    return eps_v
    
 
eps_v15 = []
eps_v50 = []
eps_v100 = []
amps = []
for i, path in enumerate(wanted_strainInfo.path):
    os.chdir(path + r"\merged_data")
    stress_data = pd.read_csv("stress_data.csv")

    # Calculate volumetric strain 
    eps_v = get_eps_v(stress_data)
    print(eps_v)

    # Check step number to get specific cycle numbers 
    step_number = stress_data.step_s.to_numpy().T
    cyclic_turns = wanted_strainInfo.cyclic_turns[i]
    amps.append( wanted_strainInfo.strain_amplitude[i])

    cycle15 = 10
    steps_at_cycle15 = cyclic_turns + cyclic_turns*2*cycle15
    idx15 = np.argmax(step_number >= steps_at_cycle15)
    eps_v15.append(eps_v[idx15])

    cycle50 = 50
    steps_at_cycle50 = cyclic_turns + cyclic_turns*2*cycle50
    idx50 = np.argmax(step_number >= steps_at_cycle50)
    eps_v50.append(eps_v[idx50])

    cycle100 = 80 # Change when all data 
    steps_at_cycle100 = cyclic_turns + cyclic_turns*2*cycle100
    idx100 = np.argmax(step_number >= steps_at_cycle100)
    eps_v100.append(eps_v[idx100])

# Figure 
plt.figure(figsize=(7,7))
plt.plot(amps[0:3], eps_v15[0:3], marker = "o", color = 'forestgreen', mec = 'black', ls = ':')
plt.plot(amps[3:6], eps_v15[3:6], marker = "o", color = 'royalblue', mec = 'black', ls = ':')
plt.plot(amps[6:9], eps_v15[6:9], marker = "o", color = 'indianred', mec = 'black', ls = ':')

plt.plot(amps[0:3], eps_v50[0:3], marker = "s", color = 'forestgreen', mec = 'black', ls = '--')
plt.plot(amps[3:6], eps_v50[3:6], marker = "s", color = 'royalblue', mec = 'black', ls = '--')
plt.plot(amps[6:9], eps_v50[6:9], marker = "s", color = 'indianred', mec = 'black', ls = '--')

plt.plot(amps[0:3], eps_v100[0:3], marker = "^", color = 'forestgreen', mec = 'black')
plt.plot(amps[3:6], eps_v100[3:6], marker = "^", color = 'royalblue', mec = 'black')
plt.plot(amps[6:9], eps_v100[6:9], marker = "^", color = 'indianred', mec = 'black')

plt.xlabel("Cyclic strain amplitude ($\epsilon^{ampl}$) [%]", fontsize = LBF)
plt.ylabel("Volumetric strain ($\epsilon_v$) [%]", fontsize = LBF)
plt.gca().tick_params(which = 'major', labelsize = TS)
plt.grid(ls = '--', lw = 1, color = 'gray')

custom_lines1 = [Line2D([0], [0], color='gray',marker = 'o', mec = 'k', ms = 5, ls = ':'),
                Line2D([0], [0], color='gray',marker = 's', mec = 'k', ms = 5, ls = '--'),
                Line2D([0], [0], color='gray',marker = '^', mec = 'k', ms = 5)]

custom_lines2 = [Line2D([0], [0], color='forestgreen',lw = 7),
                Line2D([0], [0], color='royalblue',lw = 7),
                Line2D([0], [0], color='indianred',lw = 7)]

lg1 = plt.legend(custom_lines1, ['Cycle 10', 'Cycle 50', 'Cycle 80'], loc = 'lower right', fontsize = LGF)
lg2 = plt.legend(custom_lines2, ["$p'^{av} = 100kPa$", "$p'^{av} = 200kPa$", "$p'^{av} = 300kPa$"], loc = 'upper left', fontsize = LGF)
plt.gca().add_artist(lg1)

plt.show()