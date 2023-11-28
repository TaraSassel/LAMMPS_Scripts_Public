# Created by Tara Sassel 14/07/20

# Importing Libraries
import numpy as np
import sys
import os
import matplotlib.pyplot as plt
import fnmatch
from PIL import Image

#===============================================================================
# Define Plot Fontsizes
TF = 20     # Title Font Size
LGF = 12    # Legend Font Size
LBF = 16    # Label Font Size
TS = 14     # Tick Size
lw1 = 2     # Line width 
width_in_inches = 12
height_in_inches = 9
me1 = 23    # Marker spacing

me2 = 30    # Marker spacing
mz1 = 3     # Marker size
mz2 = 4     # Marker size

#===============================================================================
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

#===============================================================================
volE1 = volE1[0] - volE1
distE1 = distE1[0] - distE1
boundE1 = boundE1[0] - boundE1

q_calc = (0.5*((stress_xx-stress_yy)**2+(stress_xx-stress_zz)**2+(stress_yy-stress_zz)**2+3*(stress_xy**2+stress_xz**2+stress_yz**2)))**(0.5)
p_calc = (stress_xx + stress_yy + stress_zz)/3

#===============================================================================
time_step = 5.24231e-09
timeinterval = (step_en1[2]-step_en1[1])
print('The timeinterval is: ' + str(timeinterval))

deltaWv = -pdash*dep*cellvol;
deltaWd = -q*deq*cellvol;
Eng_vol = np.zeros((len(deltaWv)))

i = 1
Eng_vol[0] = deltaWv[0]
while i < len(volE1):
    Eng_vol[i] = Eng_vol[i-1] + deltaWv[i]
    print(str(Eng_vol[i]) + "\t" + str(volE1[i]))
    i = i + 1
deltaWv_sim = np.zeros((len(deltaWv)))

# Figure 1 ---------------------------------------------------------------------
f1 = plt.figure(1,figsize=(width_in_inches, height_in_inches))
# fig, ax = plt.subplots()
plt.subplot(3,1,1)

line1 = plt.plot(timestep,q/1000, color = 'red',marker = '',markevery = 100,linewidth = 3)
line2 = plt.plot(step_s,q_calc/1000, color = 'black',marker = '',markevery = 100,linewidth = 2,linestyle='--')
plt.xlabel('Step number', fontsize = LBF)
plt.ylabel('Stress [kPa]', fontsize = LBF)

plt.legend([r'Simulated q','Calculated q'],loc='center left', bbox_to_anchor=(1, 0.5), fontsize = LGF)
plt.tick_params(axis='both', which='major', labelsize=TS)

plt.text(2.4e8, 5, r"$q = \sqrt{\frac{1}{2}[(\sigma'_{xx}-\sigma'_{yy})^2+(\sigma'_{xx}-\sigma'_{zz})^2+(\sigma'_{yy}-\sigma'_{zz})^2+3\times(\sigma'_{xy}^2+\sigma'_{xz}^2+\sigma'_{yz}^2)]}$", size=10,
         ha="right", va="top",
         bbox=dict(boxstyle="square",
                   facecolor='lightcoral')
         )

plt.grid()
#... Subplot
plt.subplot(3,1,2)
line3 = plt.plot(step_s,stress_xx/1000, color = 'red',marker = 'x',markevery = 300,markersize = 8,linewidth = 5)
line4 = plt.plot(step_s,stress_yy/1000, color = 'black',marker = '',markevery = 100,linewidth = 2)
line5 = plt.plot(step_s,stress_zz/1000, color = 'darkcyan',marker = '',markevery = 100,linewidth = 2)

plt.xlabel('Step number', fontsize = LBF)
plt.ylabel('Stress [kPa]', fontsize = LBF)

plt.legend([r"$\sigma'_{xx}$",r"$\sigma'_{yy}$",r"$\sigma'_{zz}$"],loc='center left', bbox_to_anchor=(1, 0.5), fontsize = LGF)
plt.tick_params(axis='both', which='major', labelsize=TS)

plt.grid()
#... Subplot
plt.subplot(3,1,3)
line6 = plt.plot(step_s,(stress_xx-stress_yy)/1000, color = 'red',marker = '',markevery = 100,linewidth = 2)
line7 = plt.plot(step_s,(stress_yy-stress_zz)/1000, color = 'darkcyan',marker = 'x',markevery = 300,markersize = 8,linewidth = 5)
line8 = plt.plot(step_s,(stress_xx-stress_zz)/1000, color = 'black',marker = '',markevery = 100,linewidth = 2)
plt.xlabel('Step number', fontsize = LBF)
plt.ylabel('Stress [kPa]', fontsize = LBF)

plt.legend([r"$\sigma'_{xx}-\sigma'_{yy}$",r"$\sigma'_{yy}-\sigma'_{zz}$",r"$\sigma'_{xx}-\sigma'_{zz}$"],loc='center left', bbox_to_anchor=(1, 0.5), fontsize = LGF)
plt.tick_params(axis='both', which='major', labelsize=TS)
plt.grid()

plt.tight_layout()

# Show  ---------------------------------------------------------------------
plt.show()

