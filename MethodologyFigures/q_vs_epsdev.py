
# IMPORTS ======================================================================
# Importing libraries
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib import cm
import os


# Importing function
import sys
sys.path.insert(1, r'C:\Users\taras\My Drive\PhD\Scripts\Python_Scripts\LAMMPS_Python_Scripts\myFunctions')
sys.path.insert(1, r'C:\Users\taras\My Drive\PhD\Scripts\Python_Scripts\LAMMPS_Python_Scripts\myFunctions')
from qp import get_qp

# FONTSIZES ====================================================================
# Define Plot Fontsizes
TF = 25     # Title Font Size
LGF = 16    # Legend Font Size
LBF = 16    # Label Font Size
TS = 14     # Tick Size
LW = 2      # Line Width

# Chaning directory
path = r'D:\PhD_Data_Back_Up\LAMMPS\CyclicLoading\ConstantP\TX300_FC0p25to0p25_amp30\Merged'#r"F:\PhD_Data_Back_Up\LAMMPS\Clumps\New_CyclicLoading\TX300_FC0p25to0p25_amp60\Merged"
timestep = 5.242309e-09 #3.187880e-09
# FUNCTIONS ====================================================================
# Calling function
xstrain,ystrain, zstrain, q, p, tanstiffness, step_s, \
stress_xx, stress_yy, stress_zz, stress_xy, stress_xz, stress_yz,\
length_x, length_y, length_z = get_qp(path)
# PROCESSING ===================================================================
# Converting
xstrain = xstrain*100 # to percentage
ystrain = ystrain*100 # to percentage
zstrain = zstrain*100 # to percentage

q = q/1000; # from Pa to kPa
eps_q = (2/3)*(zstrain - 0.5*(xstrain + ystrain))
# Get number of cycles
time_step = timestep
period = 0.25
timeinterval = (step_s[2]-step_s[1])
cycle_length = np.intc(period/(time_step*timeinterval))
n = np.intc(np.floor(len(step_s)/(cycle_length)))
n = 50
# PLOTTING =====================================================================
highlight = False 
fig,ax = plt.subplots(figsize = (10,5))
ax.set_prop_cycle('color',[plt.cm.bone(i) for i in np.linspace(0, 1, n)]) # added 5 because I dont want to go to white # change color here gray
for i in range(n):
    int0 = 0+i*cycle_length
    intf = cycle_length+i*cycle_length
    plt.plot(eps_q[int0:intf], q[int0:intf],lw = LW, zorder = 1)

    if highlight:
        if i == 0:
            int0 = 0+i*cycle_length
            intf = cycle_length+i*cycle_length
            plt.plot(eps_q[int0:intf], q[int0:intf],lw = LW+1, c = 'green', zorder = 2)
        if i == 50:
            int0 = 0+i*cycle_length
            intf = cycle_length+i*cycle_length
            plt.plot(eps_q[int0:intf], q[int0:intf],lw = LW+1, c = 'red', zorder = 3)


plt.xlabel(r"Deviatoric strain ($\varepsilon_{q}$) [%]", fontsize = LBF)
plt.ylabel(r"Deviatoric stress (q) [kPa]", fontsize = LBF)
ax.tick_params(axis='both', which='major', labelsize=TS)

# Colorbar
norm = cm.colors.Normalize(vmin=1, vmax=n+5)
cb = plt.colorbar(cm.ScalarMappable(norm=norm, cmap="bone"), ax=ax, boundaries = np.arange(0,n,1)) # change color here gray
cb.ax.tick_params(labelsize=TS-5)
labels = [1]
labels = np.append(labels, np.arange(5,n+1,5))
loc = labels-1
cb.set_ticks(loc)
cb.set_ticklabels(labels)
cb.ax.tick_params(labelsize=15)
cb.ax.set_ylabel("Cycle Number (N)",fontsize = LBF)
cb.ax.minorticks_on()
plt.tight_layout()
plt.show()
