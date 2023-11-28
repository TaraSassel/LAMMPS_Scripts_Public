"""
Author: Tara Sassel
Date: 06/02/2023

Script for stress strain loops for cyclic mean data
"""
# Imports
import os 
import fnmatch
import numpy as np 
import pandas as pd 
import seaborn as sns 
import matplotlib.pyplot as plt 
from matplotlib import cm

from basicFunctions.get_strain import get_strain
from basicFunctions.get_qp import get_qp

# =============================================================================
N = 51
Nruns = 4

# Fonts 
TF = 12      # Title Font 
TS = 12     # Tick Size
LBF = 14    # Label Font 
LGF = 16    # Legend Font
lw1 = 2     # Line Width 


# Path 
path = None
os.chdir(path + r'\merged_data')

# Process Data 
stress_data = pd.read_csv('stress_data.csv')
stress_zz = stress_data.stress_zz.to_numpy().T
zstrain = get_strain(stress_data.length_z.to_numpy().T)
q, p = get_qp(stress_data)

# Create Figure 
plt.figure(figsize = (8,8))
plt.plot(zstrain[1:15000],stress_zz[1:15000]/1000, color = 'navy', lw = lw1 )
plt.xlabel("Strain [%]", fontsize = LBF)
plt.ylabel("Stress [kPa]", fontsize = LBF)

runs = np.arange(1,Nruns)
for run in runs:
    os.chdir(path + rf'\run{run}')
    for (dirpath, dirnames, filenames) in os.walk(path + rf'\run{run}'): 
        for file in filenames:
            if file.endswith(".txt"):
                if fnmatch.fnmatch(file,"*stress*"):
                    stress_file = file
    stress_names = [
        'step_s',
        'stress_xx',
        'stress_yy',
        'stress_zz',
        'stress_xy',
        'stress_xz',
        'stress_yz',
        'length_x',
        'length_y',
        'length_z'
        ]

    stress_data_run = pd.read_csv(stress_file, index_col=None, delimiter = ' ', skiprows = 1, names = stress_names)    
    
    delta =  stress_data_run.length_z[0] - stress_data.length_z[0]
    if run == 1:
        strain0 =delta*100/stress_data.length_z[0]
        print(strain0)
    strain =delta*100/stress_data.length_z[0]
    delta_strain = strain0 - strain

    if run == 1:
        plt.plot(delta_strain,stress_data_run.stress_zz[1]/1000, color = 'red', marker = 'o', alpha = 0.5) 
    else: 
        plt.plot(delta_strain,stress_data_run.stress_zz[0]/1000, color = 'red', marker = 'o', alpha = 0.5) 
plt.show()

