# Created by Tara Sassel 11/03/21

# Importing Libraries
import numpy as np
import sys
import os
import matplotlib.pyplot as plt
import fnmatch
from PIL import Image
from matplotlib.patches import ConnectionPatch
from scipy.signal import find_peaks

#===============================================================================
# Define Plot Fontsizes
TF = 25     # Title Font Size
LGF = 18 #19    # Legend Font Size
LBF = 23 #23    # Label Font Size
TS = 16 #17     # Tick Size
AS = 16     # Annotation Size
width_in_inches = 10
height_in_inches = 7

# Change Directory
path  = r'F:\PhD_Data_Back_Up\LAMMPS\CyclicLoading\ConstantP\TX200_FC0p25to0p25_amp20\Merged' # My Desktop Dir
os.chdir(path)

#===============================================================================

# Names of Files
for (dirpath, dirnames, filenames) in os.walk(path):
    for file in filenames:
        if file.endswith(".txt"):
            if fnmatch.fnmatch(file,"*stress*"):
                stress_file = file
                print(stress_file)

# Mean Stresses
print('Processing Stresses')
step_s, stress_xx, stress_yy, stress_zz, stress_xy, stress_xz, stress_yz, length_x, length_y, length_z = np.loadtxt(stress_file).T
step_s0 = step_s[0]
step_s = step_s - step_s0
p_mean = (stress_xx + stress_yy + stress_zz)/3

# Figure 1 ---------------------------------------------------------------------
f1, ax = plt.subplots(1,figsize=(width_in_inches, height_in_inches))

# fig, ax = plt.subplots()
line1 = plt.plot(step_s,stress_xx/1000, color = 'navy',marker = 'x',markevery = 1000,markersize = 10,linewidth = 5)
line2 = plt.plot(step_s,stress_yy/1000, color = 'lightsteelblue',linestyle = '--')
line3 = plt.plot(step_s,stress_zz/1000, color = 'royalblue',linewidth = 3)

line4 = plt.plot(step_s,p_mean/1000, color = 'indianred', linewidth= 3)

# plt.title('Triaxial Cyclic Loading \n Stress vs Step Number', fontsize = TF)
plt.xlabel('Step number', fontsize = LBF)
# ax.xaxis.set_minor_locator(AutoMinorLocator(5))
plt.xlim(0,0.956*10e7)
#plt.xlabel('zstrain [%]', fontsize = LBF)
plt.ylabel('Stress [kPa]', fontsize = LBF)

plt.legend([r"$\sigma'_{xx}$",r"$\sigma'_{yy}$",r"$\sigma'_{zz}$",r"$p'_{mean}$"],loc='upper right', fontsize = LGF)
#plt.legend([r'$\sigma_{xx}$',r'$\sigma_{yy}$',r'$\sigma_{zz}$',r"$p'$"],loc='center left', bbox_to_anchor=(1, 0.5), fontsize = LGF)
plt.tick_params(axis='both', which='major', labelsize=TS)

# Annotations
# Amplitude Annotation
find1, properties = find_peaks(stress_zz,distance=10e2)
print(find1)
x_point = step_s[find1[0]]
con1 = ConnectionPatch(xyA=(x_point, 200), xyB=(x_point, 220), coordsA="data", coordsB="data",arrowstyle="<|-|>",linewidth = 3)
ax.annotate("Amplitude",xy=(x_point+10e5, 210),xytext=(x_point+10e5, 210), textcoords='data',fontsize = AS, rotation = 90, va = 'center')
ax.add_artist(con1)
t = ax.xaxis.get_offset_text()
t.set_size(20)
# Period Annotation
find1, properties = find_peaks(stress_zz,distance=10e2)
print(find1)
# x_point1 = step_s[find1[0]]
# x_point2 = step_s[find1[2]]
# x_pointA = step_s[find1[1]]

# OR
x_point1 = step_s[find1[0]]
x_point2 = step_s[find1[3]]
x_pointA = step_s[find1[3]]/2

# OR
# x_point1 = step_s[find1[0]]
# x_point2 = step_s[find1[0]]+ (step_s[find1[1]]-step_s[find1[0]])/3
# x_pointA = step_s[find1[0]]+ (step_s[find1[1]]-step_s[find1[0]])/50

con1 = ConnectionPatch(xyA=(x_point1, 220), xyB=(x_point2, 220), coordsA="data", coordsB="data",arrowstyle="<|-|>",linewidth = 3,zorder=10)
ax.annotate("Period",xy=(x_pointA, 217),xytext=(x_pointA, 217), textcoords='data',fontsize = AS)
ax.add_artist(con1)

plt.grid()

plt.tight_layout()


# Show  ---------------------------------------------------------------------
plt.show()

