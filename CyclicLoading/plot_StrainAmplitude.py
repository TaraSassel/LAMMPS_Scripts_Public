# Get Strain Amplitude
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from matplotlib.lines import Line2D

from basicFunctions.get_strain import get_strain

# Directories
path200_10 = r'G:\PhD_Data_Back_Up\LAMMPS\CyclicLoading\ConstantP\TX300_FC0p25to0p25_amp15'
path200_20 = r'G:\PhD_Data_Back_Up\LAMMPS\CyclicLoading\ConstantP\TX300_FC0p25to0p25_amp30'
path200_40 = r'G:\PhD_Data_Back_Up\LAMMPS\CyclicLoading\ConstantP\TX300_FC0p25to0p25_amp60'
path_list = [path200_10, path200_20, path200_40]

# FONTSIZES ====================================================================
# Define Plot Fontsizes
TF = 20     # Title Font Size
LGF = 16    # Legend Font Size
LBF = 18    # Label Font Size
TS = 16     # Tick Size
LW = 2      # Line Width
# COLORS/LINESTYLES/LABELS =====================================================
label_list = ["$\sigma_1'^{ampl}=15kPa$", "$\sigma_1'^{ampl}=30kPa$", "$\sigma_1'^{ampl}=60kPa$"]
ls_list = [':','--','-']
c1 = 'indianred' # Color
c_list = ['green','blue','red']

plt.figure(1,figsize = (7,7)) # Initiating figure
for i, path in enumerate(path_list):

    os.chdir(path + r'\merged_data')
    stress_data = pd.read_csv('stress_data.csv')
    stress_data['strain_z'] = get_strain(stress_data.length_z)

    # Position File
    os.chdir(path + r'\Merged\PostProcessedData')
    positions = pd.read_csv('positions.txt',index_col = None, header = None, delimiter = " ")
    N0, Max_Peak, N1, Min_Peak = positions.to_numpy().T

    # Getining Maxima and Minima
    max_strain = stress_data.loc[list(map(int,Max_Peak))]
    min_strain = stress_data.loc[list(map(int,Min_Peak))]

    strain_amp = max_strain['strain_z'].to_numpy()-min_strain['strain_z'].to_numpy()

    plt.figure(2,figsize = (7,7)) # Initiating figure
    plt.plot(np.arange(0,50,1),max_strain['strain_z'][0:50]/100, marker = '^', c = c_list[i], ls = ls_list[i])
    plt.plot(np.arange(0,50,1),min_strain['strain_z'][0:50]/100, marker = 'v', c = c_list[i], ls = ls_list[i])
    plt.xlabel('Cycle Number (N)', fontsize = LBF)
    plt.ylabel('Axial Strain %', fontsize = LBF)

    plt.figure(1,figsize = (7,7)) # Initiating figure
    plt.plot((strain_amp/100), label = label_list[i], c = c1, ls = ls_list[i], lw = LW) # Convert from percentage and change to 10^-4 to be comparable to wichtmann

# Adjust Axis
plt.tick_params(axis='both', which='major', labelsize=TS)
plt.legend(loc = 'upper right', fontsize = LGF)
plt.xlabel('Cycle Number (N)', fontsize = LBF)
plt.ylabel('Strain Amplitude $(\epsilon^{ampl})$', fontsize = LBF)
plt.xlim(0,50)
plt.ylim(0)

plt.tight_layout()
plt.grid()

plt.figure(2,figsize = (7,7)) # Initiating figure
plt.tick_params(axis='both', which='major', labelsize=TS)
plt.legend(loc = 'upper right', fontsize = LGF)
plt.xlabel('Cycle Number (N)', fontsize = LBF)
plt.ylabel('Axial strain $(\epsilon_{zz})$', fontsize = LBF)
plt.xlim(0,50)
plt.ylim(0)

#Legend
y1_line = mlines.Line2D([],[],label= "$\zeta$ = 5%", c = 'green')
y2_line = mlines.Line2D([],[],label= "$\zeta$ = 10%", c = 'blue')
y3_line = mlines.Line2D([],[],label= "$\zeta$ = 20%", c = 'red')
la = plt.legend(handles=[y1_line,y2_line,y3_line],loc='center right',fontsize = LGF)

y1_line = mlines.Line2D([],[], marker = '^', ls=' ',label= "Maxima", c = 'black')
y2_line = mlines.Line2D([],[], marker = 'v', ls=' ',label= "Minima", c = 'black')
lb = plt.legend(handles=[y1_line,y2_line],loc='upper right',fontsize = LGF)
plt.gca().add_artist(la)

plt.tight_layout()
plt.grid()

plt.show()
