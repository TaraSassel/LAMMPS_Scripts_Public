# Energy Balance by Tara Sassel 19.06.2020

# Importing Libraries
import numpy as np
import scipy.io as sio
import math
import sys
import os
import fnmatch
import matplotlib.pyplot as plt
from matplotlib import rc
from matplotlib.lines import Line2D
from matplotlib import pyplot
from matplotlib.pyplot import *

# Define Plot Fontsizes
# Fonts
TF = 20     # Title Font Size
LGF = 12    # Legend Font Size
LBF = 16    # Label Font Size
TS = 14     # Tick Size
lw1 = 2     # Line width 
ms1 = 10    # marker size

color_list = ['indianred','maroon','lightgreen','forestgreen']
ls_list = ['-','--','-','--']
lw_list = [4,2,4,2]

# energy_file = "shear_energy.txt"
# stress_file = "shear_mean_stress.txt"

# a = 73706
####### GET DATA ---------------------------------------------------------------
# Change Directory
count = 4 # Numbers of legends you entered (should be less then 5 else need to modify)

path1  = r'F:\PhD_Data_Back_Up\LAMMPS\Random_Packing\TX Shear\TXShear100kPa_fromFC0p1to0p1_Modified\Merged' # My Desktop Dir
col1 = 'red'
lsty1 = '-'
mk1 = None
lw1 = 3
l1 = 'Newton on friction coefficient 0.1 to 0.25'

path2  = r'F:\PhD_Data_Back_Up\LAMMPS\Random_Packing\TX Shear\NewtonOff\TXShear100kPa_fromFC0p1to0p25\Merged' # My Desktop Dir
col2 = 'blue'
lsty2 = '-'
mk2 = None
lw2 = 1
l2 = 'Newton off friction coefficient 0.1 to 0.25'

path3  = r'F:\PhD_Data_Back_Up\LAMMPS\Random_Packing\TX Shear\TXShear100kPa_fromFC0p1to0p25_Modified\Merged' # My Desktop Dir
col3 = 'purple'
lsty3 = '-'
mk3 = None
lw3 = 3
l3 = 'Newton on friction coefficient 0.1 to 0.1'

path4  = r'F:\PhD_Data_Back_Up\LAMMPS\Random_Packing\TX Shear\NewtonOff\TXShear100kPa_fromFC0p1to0p1\Merged' # My Desktop Dir
col4 = 'green'
lsty4 = '-'
mk4 = None
lw4 = 1
l4 = 'Newton off friction coefficient 0.1 to 0.1'

####### GET Filenames ----------------------------------------------------------

def plot_EB(path,col,lsty,lw):

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

    os.chdir(path)

    # Calculation for Boundary Work --------------------------------------------
    # Energies
    step_en1, tkE1, rkE1, kE1, friE1, volE1, distE1, boundE1, normE1, shearE1, strainE1, locdampE1, viscodampE1, dampE1 = np.loadtxt(energy_file).T
    print('array length:')
    print(len(step_en1))
    E_sn0 = normE1[0]       # Initial total normal strain eregry
    E_st0 = shearE1[0]      # Initial total tangental strain energy
    E_kt0 = tkE1[0]         # Initial transitional kinetric energy
    E_kr0 = rkE1[0]         # Initial rotational kinetic energy


    W1 = boundE1[:]-boundE1[0]  # Total boundary work

    W2 = volE1 + distE1
    W2 = W2 - W2[0]

    E_f = friE1[:]-friE1[0]          # Frictional Energy
    E_sn = normE1[:]        # Total normal strain eregry
    E_st = shearE1[:]       # Total tangental strain energy
    E_kt = tkE1[:]          # Transitional kinetric energy
    E_kr = rkE1[:]          # Rotational kinetic energy

    dE1 = E_sn0 + E_st0 + E_kt0 + E_kr0 + W1 - E_f - E_sn - E_st - E_kt - E_kr    # Error in Energy Balance
    dE2 = E_sn0 + E_st0 + E_kt0 + E_kr0 + W2 - E_f - E_sn - E_st - E_kt - E_kr    # Error in Energy Balance

    W1_error = np.zeros((len(W1),1))
    W2_error = np.zeros((len(W1),1))

    for j in range(len(W1)):
        if W1[j] == 0:
            W1_error[j]  = 0
        else:
            W1_error[j]  = 100*dE1[j] /W1[j]

        if W2[j]  == 0:
            W2_error[j]  = 0
        else:
            W2_error[j]  = 100*dE2[j] /W1[j]

    print('initial boundary energy')
    print(W1[0])
    print('initial frictional energy')
    print(E_f[0])

    # Calculation For Axial Strain ---------------------------------------------
    step_s, stress_xx, stress_yy, stress_zz, stress_xy, stress_xz, stress_yz, length_x, length_y, length_z = np.loadtxt(stress_file).T

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

    # Plot ---------------------------------------------------------------------
    f = plt.figure(1, figsize = (10,5))
    plt.plot(zstrain[1:], W1_error[1:],col,linestyle = lsty, linewidth=lw)
    plt.plot(zstrain[1:], W2_error[1:],col,linestyle = lsty, linewidth=lw, marker = 'x', markevery = 1000, ms = ms1)

# Start Function'---------------------------------------------------------------

plot_EB(path1,color_list[0],ls_list[0],lw_list[0])
plot_EB(path2,color_list[1],ls_list[1],lw_list[1])
plot_EB(path3,color_list[2],ls_list[2],lw_list[2])
plot_EB(path4,color_list[3],ls_list[3],lw_list[3])



# Figure Layout-----------------------------------------------------------------
label1=r'$\Delta E = E_{sn}^0 + E_{st}^0 + E_{kt}^0 + E_{kr}^0 + W^{\beta} - E_{f}^{\beta} - E_{sn}^{\beta} - E_{st}^{\beta} - E_{kt}^{\beta} - E_{kr}^{\beta}$'
label2=r'$\Delta E = E_{sn}^0 + E_{st}^0 + E_{kt}^0 + E_{kr}^0 + (W_{d}^{\beta} + W_{v}^{\beta}) - E_{f}^{\beta} - E_{sn}^{\beta} - E_{st}^{\beta} - E_{kt}^{\beta} - E_{kr}^{\beta}$'

legend_elementsa = [ Line2D([0], [0],color='black', label=label1),Line2D([0], [0],color='black', label=label2, marker = 'x', ms = ms1)]

legend_elementsb = [ 
    Line2D([0], [0],color=color_list[0], label=l1, lw = lw_list[0], ls = ls_list[0]),
    Line2D([0], [0],color=color_list[1], label=l2, lw = lw_list[1], ls = ls_list[1]),
    Line2D([0], [0],color=color_list[2], label=l3, lw = lw_list[2], ls = ls_list[2]),
    Line2D([0], [0],color=color_list[3], label=l4, lw = lw_list[3], ls = ls_list[3])]

la = legend(handles=legend_elementsa, loc='upper right', fontsize = LGF)
lb = legend(handles=legend_elementsb,loc='center right', fontsize = LGF)
plt.xlim(-0.1,5)
plt.xlabel('Axial strain [%]', fontsize = LBF)
plt.ylabel('Error in energy balance [%]', fontsize = LBF)

ax = plt.gca()
ax.get_yaxis().get_major_formatter().set_useOffset(False)
ax.tick_params(axis='both', which='major', labelsize=TS)
plt.xlim(-0.1,1.5)
gca().add_artist(la) # add l1 as a separate artist to the axes
gca().add_artist(lb) # add l1 as a separate artist to the axes
plt.grid()
plt.tight_layout()

plt.show()
