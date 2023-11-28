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
from matplotlib.colors import ListedColormap

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


# Path 
path = r'E:\CyclicLoading\Cyclicmean_OneWay\TX330_FC0p25to0p25_amp30'    

os.chdir(path + r'/merged_data')


# Load stress data
stress_data = pd.read_csv('stress_data.csv')

# Calculating cycle length
time_step = 5.24231e-09
period = 0.25
cycle_length = int(period/(time_step))
step_interval = stress_data.step_s[1] - stress_data.step_s[0]
cycle_steps = int(cycle_length/step_interval)


# Caluclate q p 
stress_zz = stress_data.stress_zz.to_numpy().T
zstrain = get_strain(stress_data.length_z.to_numpy().T)
q, p = get_qp(stress_data)


my_cmap = ListedColormap(sns.color_palette("ch:s=.25,rot=-.25", n_colors=51))
color = my_cmap(np.linspace(0,1,51))

plt.figure(figsize = (12,5))

for i in range(51):
    k = i+1
    plt.plot(zstrain[i*cycle_steps:k*cycle_steps],stress_zz[i*cycle_steps:k*cycle_steps]/1000, lw = lw1, c = color[i])

# Colorbar
sm = plt.cm.ScalarMappable(cmap=my_cmap, norm=plt.Normalize(vmin=0, vmax=50))
cb = plt.colorbar(sm)
cb.ax.tick_params(labelsize=TS)
cb.set_label('Cycle number (N)', fontsize = 12)


plt.xlabel("Axial strain [%]", fontsize = LBF)
plt.ylabel("Axial stress ($\sigma'_{zz}$) [kPa]", fontsize = LBF)

plt.xlim(0,)
plt.show()

