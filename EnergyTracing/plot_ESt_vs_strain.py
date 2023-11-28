# Energy Balance by Tara Sassel 19.06.2020

# Importing Libraries
import re 
import os
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt

from basicFunctions.get_strain import get_strain

# Define Plot Fontsizes
TF = 20     # Title Font Size
LGF = 20    # Legend Font Size
LBF = 15    # Label Font Size
TS = 12     # Tick Size
lw1 = 2     # Line Width 

# Change Directory
path  = r'E:\StrainControlledCyclic\300kPa\Strain1' # My Desktop Dir

# Get cyclic turns 
os.chdir(path + r'\template')
for line in open('continue_cyclic.in'):
    match = re.search('cyclicturns equal (\d+)', line)
    if match:
        cyclicturns = int(match.group(1))
        print(cyclicturns)

# Energies
os.chdir(path + r'\merged_data')
energy_data = pd.read_csv('energy_data.csv')

step_en1 = energy_data.step_e.to_numpy().T
tkE1 = energy_data.tkE.to_numpy().T
rkE1 = energy_data.rkE.to_numpy().T
kE1 = energy_data.kE.to_numpy().T 
friE1 = energy_data.friE.to_numpy().T
volE1 = energy_data.volE.to_numpy().T
distE1 = energy_data.distE.to_numpy().T 
boundE1 = energy_data.boundE.to_numpy().T
normE1 = energy_data.normE.to_numpy().T 
shearE1 = energy_data.shearE.to_numpy().T 
strainE1 = energy_data.strainE.to_numpy().T 
locdampE1 = energy_data.locdampE.to_numpy().T 
viscodampE1 = energy_data.viscodampE.to_numpy().T
dampE1 = energy_data.dampE.to_numpy().T

# Calculation for Boundary Work ------------------------------------------------

E_sn0 = normE1[0]       # Initial total normal strain eregry
E_st0 = shearE1[0]      # Initial total tangental strain energy
E_kt0 = tkE1[0]         # Initial transitional kinetric energy
E_kr0 = rkE1[0]         # Initial rotational kinetic energy

print('initial boundary energy')
print(boundE1[0])
print('initial frictional energy')
print(friE1[0])

W1 = boundE1[:]  # Total boundary work
W2 = volE1 + distE1

E_f = friE1[:]          # Frictional Energy
E_sn = normE1[:]        # Total normal strain eregry
E_st = shearE1[:]       # Total tangental strain energy
E_kt = tkE1[:]          # Transitional kinetric energy
E_kr = rkE1[:]          # Rotational kinetic energy

dE1 = E_sn0 + E_st0 + E_kt0 + E_kr0 + W1 - E_f - E_sn - E_st - E_kt - E_kr    # Error in Energy Balance
dE2 = E_sn0 + E_st0 + E_kt0 + E_kr0 + W2 - E_f - E_sn - E_st - E_kt - E_kr    # Error in Energy Balance
W1_error = 100*dE1/W1
W2_error = 100*dE2/W2

# Calculation For Axial Strain -------------------------------------------------

stress_data = pd.read_csv('stress_data.csv')

step_s = stress_data.step_s.to_numpy().T

# Calculate Volumetric Strain 
length_x = stress_data.length_x.to_numpy().T
length_y = stress_data.length_y.to_numpy().T
length_z = stress_data.length_z.to_numpy().T

xstrain = get_strain(length_x)
ystrain = get_strain(length_y)
zstrain = get_strain(length_z)

# Isoloate cycle_length ---------------------------------------------------
time_step = 5.242309e-09
period = 0.25
timeinterval = (step_s[2]-step_s[1])
cycle_length = round((cyclicturns*2)/timeinterval)

def get_int(cycle_number: int)-> int:
    cri = cycle_length*cycle_number     # cycle range initial
    crf = cycle_length*(cycle_number+1) # cycle range final
    return cri, crf 

cri1, crf1 = get_int(0)
cri10, crf10 = get_int(9)
cri50, crf50 = get_int(49)
cri100, crf100 = get_int(99)

E = shearE1 # Which Energy 

# Figure 
fig = plt.figure(1, figsize = (7,7), constrained_layout=True)

plt.plot(zstrain[0:crf100], E[0:crf100],zorder = 1,c = 'silver')

plt.plot(zstrain[cri1:crf1], E[cri1:crf1],'#c0f6bb', lw = lw1)
plt.plot(zstrain[cri10:crf10], E[cri10:crf10],'#6ceb60', lw = lw1)
plt.plot(zstrain[cri50:crf50], E[cri50:crf50],'#209f14', lw = lw1)
plt.plot(zstrain[cri100:crf100], E[cri100:crf100],'#0e4409', lw = lw1)

plt.text(0.95, np.max(E[cri1:crf1]), 'Cycle 1', ha = 'center', va = 'center', bbox=dict(boxstyle="square", fc='#c0f6bb', alpha=0.7), size = 10)
plt.text(0.95, np.max(E[cri10:crf10]), 'Cycle 10', ha = 'center', va = 'center', bbox=dict(boxstyle="square", fc='#6ceb60', alpha=0.7), size = 10)
plt.text(0.95, np.max(E[cri50:crf50]), 'Cycle 50', ha = 'center', va = 'center', bbox=dict(boxstyle="square", fc='#209f14', alpha=0.7), size = 10)
plt.text(0.95, np.max(E[cri100:crf100]), 'Cycle 100', ha = 'center', va = 'center', bbox=dict(boxstyle="square", fc='#0e4409', alpha=0.7), size = 10)

# 0p1 --> 0.09
# 0p5 --> 0.49
# 1p0 --> 0.95


plt.xlabel(r'Axial strain ($\varepsilon_{zz}$) [%]', fontsize = LBF)
plt.ylabel('Tangential strain energy ($E_{st}$) [J]', fontsize = LBF)
plt.tick_params(axis='both', which='major', labelsize=TS)

plt.grid()
plt.tight_layout()
plt.show()

