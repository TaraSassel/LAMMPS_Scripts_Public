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


# Path 
path = None     # to merged data
os.chdir(path)

# Process Data 
stress_data = pd.read_csv('stress_data.csv')
stress_zz = stress_data.stress_zz.to_numpy().T
zstrain = get_strain(stress_data.length_z.to_numpy().T)
q, p = get_qp(stress_data)

# Create Figure 
plt.figure(figsize = (8,8))
plt.plot(zstrain[1:],stress_zz[1:], color = 'navy', lw = lw1 )
plt.xlabel("Strain [%]", fontsize = LBF)
plt.ylabel("Stress [kPa]", fontsize = LBF)

plt.show()

