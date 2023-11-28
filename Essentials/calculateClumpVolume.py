# Script to calculate Intertia and mass for a clump
import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd

# Importing function to caclulate mass and inertia
from basicFunctions.get_clump_Im import get_vol

# Define

clump_n =  6484 #22288 # Enter number of clumps
path = r'C:\Users\taras\My Drive\PhD\LAMMPS\Simulations\LAMMPS\Sample_Generation\A_Sample_Generation\ClumpGeneration\6kSample'

# Changing Directory
os.chdir(path)

# # Names of Files
# for (dirpath, dirnames, filenames) in os.walk(path):
#     for file in filenames:
#         if file.endswith(".lj"):
#             sample_file = file
#             print(sample_file)
sample_file = 'Clumps6484_AR1p5.lj'
# Loading file
# sphere number,clump number,dia,density,coord-x,coord-y,coord-z
df = pd.read_csv(sample_file, skiprows = 9, nrows = (clump_n)*2, delimiter = ' ', header = None)
df = df.to_numpy()
Vclump = np.zeros((clump_n,))

for i in range(clump_n):
    a = i*2
    id = df[a,0]
    x1 = df[a,4]
    y1 = df[a,5]
    z1 = df[a,6]
    d1 = df[a,2]
    x2 = df[a+1,4]
    y2 = df[a+1,5]
    z2 = df[a+1,6]
    d2 = df[a+1,2]
    coord1 = [x1,y1,z1]
    coord2 = [x2,y2,z2]
    print('id')
    print(id)
    Vclump[i] = get_vol(d1,coord1,d2,coord2)

Vtot = np.sum(Vclump)
print(Vtot)
np.savetxt('VStot.txt',[Vtot])
