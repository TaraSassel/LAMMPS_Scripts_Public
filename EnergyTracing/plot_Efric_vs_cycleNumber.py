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
me1 = 23    # Marker spacing
me2 = 30    # Marker spacing
mz1 = 3     # Marker size
mz2 = 4     # Marker size

# Change Directory
path  = r'E:\StrainControlledCyclic\300kPa\Strain1' # My Desktop Dir

####### Define Function---------------------------------------------------------
def energy_plot(col1):
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
    
    plt.figure(1, figsize = (5,5))
    plt.plot(E[required_ints],'black',zorder = 1)

# Plot -------------------------------------------------------------------------

energy_plot('black')

plt.xlabel('Cycle number (N)', fontsize = LBF)
plt.ylabel('Frictional energy ($E_{fric}$) [J]', fontsize = LBF)
plt.tick_params(axis='both', which='major', labelsize=TS)

plt.xlim(0,100)

plt.grid()
plt.tight_layout()

plt.show()
