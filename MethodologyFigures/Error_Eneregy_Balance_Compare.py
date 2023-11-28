# Energy Balance by Tara Sassel 19.06.2020

# Importing Libraries
import numpy as np
import scipy.io as sio
import math
import sys
import os
import matplotlib.pyplot as plt
from matplotlib import rc
from matplotlib.lines import Line2D
from matplotlib import pyplot
from matplotlib.pyplot import *
import fnmatch
from PIL import Image

# Define Plot Fontsizes

TF = 20     # Title Font Size
LGF = 12    # Legend Font Size
LBF = 16    # Label Font Size
TS = 14     # Tick Size
me1 = 1000    # Marker spacing
me2 = 30    # Marker spacing
mz1 = 9     # Marker size
mz2 = 4     # Marker size

width_in_inches = 20
height_in_inches = 10



####### GET DATA --------------------------------------------------------------
# Change Directory
# Path of Isotropic Compression
path0 = r'F:\PhD_Data_Back_Up\LAMMPS\Random_Packing\Istotropic Compression\Toyoura150k\Capability_ISOCOMP200_Density2650_FC0p25'
os.chdir(path0)
# Names of Files
for (dirpath, dirnames, filenames) in os.walk(path0):
    for file in filenames:
        if file.endswith(".txt"):
            if fnmatch.fnmatch(file,"*energy*"):
                energy_file_iso = file
                print(energy_file_iso)
# Energies
step_en0, tkE0, rkE0, kE0, friE0, volE0, distE0, boundE0, normE0, shearE0, strainE0, locdampE0, viscodampE0, dampE0 = np.loadtxt(energy_file_iso).T

# Path of Cylcic Loading
path1  = r'F:\PhD_Data_Back_Up\LAMMPS\Random_Packing\Cyclic_Loading\150k_Sample\Capability_Large_TX200_FC0p25to0p25\Merged'
os.chdir(path1)

# Names of Files
for (dirpath, dirnames, filenames) in os.walk(path1):
    for file in filenames:
        if file.endswith(".txt"):
            if fnmatch.fnmatch(file,"*stress*"):
                stress_file = file
                print(stress_file)
            if fnmatch.fnmatch(file,"*energy*"):
                energy_file = file
                print(energy_file)

# Change Directory
path  = r'F:\PhD_Data_Back_Up\LAMMPS\Random_Packing\Cyclic_Loading\20k_Sample\Check_boundaryE\TraceStrain_20k_TX200_FC0p25to0p25_constantp\Merged' # My Desktop Dir
os.chdir(path)

# Names of Files
for (dirpath, dirnames, filenames) in os.walk(path):
    for file in filenames:
        if file.endswith(".txt"):
            if fnmatch.fnmatch(file,"*stress*"):
                stress_file = file
                print(stress_file)
            if fnmatch.fnmatch(file,"*energy*"):
                energy_file = file
                print(energy_file)

# Mean Stresses
print('Load Text Files')
cellvol, q, pdash, deq, dep, strain_rate_xx, strain_rate_yy, strain_rate_zz, timestep = np.loadtxt('LAMMPS_output.txt').T
step_s, stress_xx, stress_yy, stress_zz, stress_xy, stress_xz, stress_yz, length_x, length_y, length_z = np.loadtxt(stress_file).T
step_en1, tkE1, rkE1, kE1, friE1, volE1, distE1, boundE1, normE1, shearE1, strainE1, locdampE1, viscodampE1, dampE1 = np.loadtxt(energy_file).T

print('Text Files Loaded')
# Calculate Axial Strains
delta_xx = np.zeros(len(stress_xx))
delta_yy = np.zeros(len(stress_xx))
delta_zz = np.zeros(len(stress_xx))

for i in range(len(stress_xx)):

    delta_xx[i] =  length_x[0] - length_x[i]
    delta_yy[i] =  length_y[0] - length_y[i]
    delta_zz[i] =  length_z[0] - length_z[i]

xstrain =delta_xx*100/length_z[0]
ystrain =delta_yy*100/length_z[0]
zstrain =delta_zz*100/length_z[0]
# New Q
q_calc = (0.5*((stress_xx-stress_yy)**2+(stress_xx-stress_zz)**2+(stress_yy-stress_zz)**2+3*(stress_xy**2+stress_xz**2+stress_yz**2)))**(0.5)
q_new = (stress_zz - 0.5*(stress_xx + stress_yy))

# Calculate delta eps
delta_eps_x = np.zeros((len(q_new)-1,))
delta_eps_y = np.zeros((len(q_new)-1,))
delta_eps_z = np.zeros((len(q_new)-1,))
W_d_calc = np.zeros((len(q_new)-1,))
for i in range(len(q_new)-1):
    delta_eps_x[i] = (length_x[i+1] - length_x[i])/(0.5*(length_x[i]+length_x[i+1]))
    delta_eps_y[i] = (length_y[i+1] - length_y[i])/(0.5*(length_y[i]+length_y[i+1]))
    delta_eps_z[i] = (length_z[i+1] - length_z[i])/(0.5*(length_z[i]+length_z[i+1]))

deq =(2/3)*(delta_eps_z-0.5*(delta_eps_x+delta_eps_y))
i = 0
W_d_calc[i] =  q_new[i]*deq[i]*cellvol[i]
i = 1
while i < (len(q_new)-1):
    W_d_calc[i] = W_d_calc[i-1]- q_new[i]*deq[i]*cellvol[i]
    i = i + 1

# W1 = boundE1
# W2 = volE1 + distE1
# W3 = volE1 + W_d_calc
E_sn0 = normE1[0]       # Initial total normal strain eregry
E_st0 = shearE1[0]      # Initial total tangental strain energy
E_kt0 = tkE1[0]         # Initial transitional kinetric energy
E_kr0 = rkE1[0]         # Initial rotational kinetic energy


#
W1 = boundE1[:]-boundE1[0]  # Total boundary work
W2 = volE1 + distE1
W2 = W2 - W2[0]
W3 = volE1[1:] + W_d_calc
W3 = W3 - W3[0]

E_f = friE1[:]-friE1[0] # Frictional Energy
E_sn = normE1[:]        # Total normal strain eregry
E_st = shearE1[:]       # Total tangental strain energy
E_kt = tkE1[:]          # Transitional kinetric energy
E_kr = rkE1[:]          # Rotational kinetic energy

dE1 = E_sn0 + E_st0 + E_kt0 + E_kr0 + W1 - E_f - E_sn - E_st - E_kt - E_kr    # Error in Energy Balance using boundary energy
dE2 = E_sn0 + E_st0 + E_kt0 + E_kr0 + W2 - E_f - E_sn - E_st - E_kt - E_kr    # Error in Energy Balance using volumetric + distrorional energy
dE3 = E_sn0 + E_st0 + E_kt0 + E_kr0 + W3 - E_f[1:] - E_sn[1:] - E_st[1:] - E_kt[1:] - E_kr[1:]   # Error in Energy Balance Modified

W1_error = np.zeros((len(W1),1))
W2_error = np.zeros((len(W1),1))
W3_error = np.zeros((len(W1),1))

for j in range(len(W1)):
    if W1[j] == 0:
        W1_error[j]  = 0
    else:
        W1_error[j]  = 100*dE1[j] /W1[j]

    if W2[j]  == 0:
        W2_error[j]  = 0
    else:
        W2_error[j]  = 100*dE2[j] /W2[j]
for j in range(len(W1)-1):
    if W3[j]  == 0:
        W3_error[j]  = 0
    else:
        W3_error[j]  = 100*dE3[j] /W3[j]
# Plot -------------------------------------------------------------------------

fig, ax = plt.subplots(figsize=(10,5))
a1 = len(zstrain)
a2 = len(W1)
if a1 < a2:
    a = a1
else:
    a = a2
ax.axhline(0,color = 'black')
line2 = plt.plot(timestep[10:a], W1_error[10:a],'darkgreen',marker = "o",markevery=me1,markersize = mz1,label=r'Energy balance using $W_{bound\:simulated}$',linewidth = 4)
line2 = plt.plot(timestep[0:a], W2_error[0:a],'darkred',markevery=me1,markersize = mz1,label=r'Energy balance using $W_{vol\:simulated} + W_{dist\:simulated}$',linewidth = 2)
line3 = plt.plot(timestep[10:a], W3_error[10:a],'darkblue',marker = '>',markevery=(me1+100),markersize = mz1,label=r'Energy balance using $W_{vol\:simulated} + W_{dist\:modified}$',linewidth = 2)

plt.xlabel('Step number', fontsize = LBF)
plt.ylabel('Error in energy balance [%]', fontsize = LBF)
plt.xlim(0.8e8,2.3e8)
plt.ylim()
plt.tick_params(axis='both', which='major', labelsize=TS)
plt.grid()

ts = 5.24231e-09
cycle_range = 0.25/(ts*2)
print(cycle_range)

leg = ax.legend(fontsize = LGF,loc = 'upper right',facecolor = 'white',framealpha = 1)
t = ax.xaxis.get_offset_text()
t.set_size(TS)
plt.tight_layout()
plt.show()
