# Energy Balance by Tara Sassel 19.06.2020

# Importing Libraries
import re 
import os
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
import matplotlib.lines as mlines

from basicFunctions.get_strain import get_strain

# Define Plot Fontsizes
TF = 14     # Title Font Size
LGF = 12    # Legend Font Size
LBF = 14    # Label Font Size
TS = 12     # Tick Size
lw1 = 2     # Line width 

# =================================================================================================
stresses = [100,200,300]
strains = ['0p1','0p5','1']

color_list = ['darkgreen','navy', 'maroon']
ls_list = [':','--','-']
stress_list = [100,200,300]

####### Define Function---------------------------------------------------------
def energy_plot(path, col1, ls1, tag1):
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
    cycle_length = int((cyclicturns*2)/timeinterval)

   
    required_ints = np.arange(0, cycle_length*101, cycle_length)
    
    E = friE1
    
    if tag1:
        return friE1, required_ints
    else: 
        plt.figure(1, figsize = (10,5))
        plt.plot(E[required_ints],c = col1, ls = ls1, lw = 2)

# Plot -------------------------------------------------------------------------
for i, stress in enumerate(stress_list): 
    for j, strain in enumerate(strains): 
        path = rf'E:\StrainControlledCyclic\{stress}kPa\Strain{strain}'
        energy_plot(path, color_list[i], ls_list[j], False)

for j, strain in enumerate(strains):
    path = rf'E:\StrainControlledCyclic\300kPa_FC0p15\Strain{strain}'
    E, required_ints = energy_plot(path, 'black', ls_list[j], True)
    plt.figure(1, figsize = (10,5))
    plt.plot(E[required_ints],c = 'black', ls = ls_list[j], lw = 2, marker = 's', markevery = 5)

# Figure adjustments
ax = plt.gca()

plt.xlabel('Cycle number (N)', fontsize = LBF)
plt.ylabel('Frictional energy ($E_{fric}$) [J]', fontsize = LBF)
plt.tick_params(axis='both', which='major', labelsize=TS)

plt.xlim(0,100)

# Legend
basecolor = 'gray'

# lg1:
line1 = mlines.Line2D([], [], color=basecolor, ls = ':', label='0.1%', lw = lw1)
line2 = mlines.Line2D([], [], color=basecolor, ls = '--', label='0.5%', lw = lw1)
line3 = mlines.Line2D([], [], color=basecolor, ls = '-', label='1%', lw = lw1)
lg1 = ax.legend(handles=[line1, line2, line3], loc = 'center left', fontsize = LGF, title = "$\epsilon_{zz}^{ampl}$:")

# lg2:
patch1 = mlines.Line2D([], [], color = color_list[0], lw = lw1, label = r"$p'_0$ = 100 kPa $\mu = 0.25$")
patch2 = mlines.Line2D([], [], color = color_list[1], lw = lw1, label = r"$p'_0$ = 200 kPa $\mu = 0.25$")
patch3 = mlines.Line2D([], [], color = color_list[2], lw = lw1, label = r"$p'_0$ = 300 kPa $\mu = 0.25$")
patch4 = mlines.Line2D([], [], color = 'black', lw = lw1, marker ='s', label = r"$p'_0$ = 300 kPa $\mu = 0.15$")

lg2 = ax.legend(handles=[patch1, patch2, patch3, patch4], loc = 'upper left', fontsize = LGF)

ax.add_artist(lg1)

plt.grid()
plt.tight_layout()

plt.show()
