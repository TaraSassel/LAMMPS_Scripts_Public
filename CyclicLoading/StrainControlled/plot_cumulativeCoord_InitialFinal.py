# Commulative Distribution Tara 04/02/2022

#===============================================================================
# Importing libraries
import re
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


#===============================================================================
# Define Plot Fontsizes
TF = 25     # Title Font Size
LGF = 16    # Legend Font Size
LBF = 18    # Label Font Size
TS = 18     # Tick Size
ms1 = 5     # markersize
LW = 2     # linewidth

#===============================================================================
# Define Path
path = r'E:\StrainControlledCyclic\300kPa\Strain1'

# Get steps to dumpfile 100
os.chdir(path + r'\template')

file_name = "continue_cyclic.in"

with open(path + "\\template\\" + file_name) as f:
        for line in f:
            # Capturing Walltime
            if 'interval_dump equal' in line:
                cyclic_steps = re.findall(r'\d+', line)
                cyclic_steps = int(cyclic_steps[0])
                cyclic_steps = cyclic_steps*4
                print(cyclic_steps)
dump_steps100 = cyclic_steps * 100

#===============================================================================
# Function
def get_cumulative2(dump_file):
    df = pd.read_csv(dump_file, skiprows = 9, delimiter = ' ', header = None,names = ["ID", "coord", "x", "y", "z", "radius", "NaN"])
    df = df.sort_values(by=['coord'])
    natoms = np.max(df['ID'])
    maxcoord = np.max(df['coord'])
    coords = np.arange(0,maxcoord+1,1)
    coordn = 0
    count = 0

    cumulative = np.zeros(maxcoord+1,)
    while coordn <= maxcoord:
        count = count + ((df.coord == coordn).sum()/natoms)*100
        cumulative[coordn] = count
        coordn += 1

    cumulativeD = np.array([coords,cumulative])

    return cumulativeD

#===============================================================================
# Call Function
# At cycle 1
os.chdir(path + r'\run1\connectivity')
dump0 = r'dump0.connectivity'
cumulativeD0 = get_cumulative2(dump0)

# At cycle 100
os.chdir(path + r'\run100\connectivity')
dump100 = rf'dump{dump_steps100}.connectivity'
cumulativeD100 = get_cumulative2(dump100)


# #===============================================================================
# Create Figure
plt.figure(figsize=(7, 7))

plt.plot(cumulativeD0[0,:],cumulativeD0[1,:], color = "black", lw = 3, label = "Cycle 1")
plt.plot(cumulativeD100[0,:],cumulativeD100[1,:], color = "maroon", lw = 3, ls = ':', label = "Cycle 100")

plt.xticks(np.arange(0,15,1))
plt.yticks(np.arange(0,101,10))
plt.xlabel(r'Coordination Number ($\bar{C}_N$)', fontsize = LBF)
plt.ylabel('Cumulative Distribution [%]', fontsize = LBF)
plt.legend(loc = 'center right', fontsize = LGF)
ax = plt.gca()
ax.tick_params(axis='both', labelsize= TS)
plt.grid()
plt.tight_layout()
plt.show()
