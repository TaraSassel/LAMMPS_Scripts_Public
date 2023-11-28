# Created by Tara Sassel 02/06/20

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

# Define Plot Fontsizes
TF = 20     # Title Font Size
LGF = 12    # Legend Font Size
LBF = 16    # Label Font Size
TS = 14     # Tick Size
lw1 = 2     # Line width 
energy_file = "shear_energy.txt"

####### GET DATA ---------------------------------------------------------------

path1  = r'F:\PhD_Data_Back_Up\LAMMPS\Random_Packing\TX Shear\TXShear100kPa_fromFC0p1to0p25\Merged' # My Desktop Dir
me1 = 10000    # Marker spacing
mz1 = 1     # Marker size
mk1 = 'None'
lsty1 = '-'
l1 = 'Newton on friction coefficient 0.1 to 0.25'
col1 = 'red'#only needed for plot 3

path2  = r'F:\PhD_Data_Back_Up\LAMMPS\Random_Packing\TX Shear\NewtonOff\TXShear100kPa_fromFC0p1to0p25\Merged' # My Desktop Dir
me2 = 10000    # Marker spacing
mz2 = 1     # Marker size
mk2 = 'None'
lsty2 = '--'
l2 = 'Newton off friction coefficient 0.1 to 0.25'
col2 = 'blue' #only needed for plot 3

path3  = r'F:\PhD_Data_Back_Up\LAMMPS\Random_Packing\TX Shear\TXShear100kPa_fromFC0p1to0p1\Merged' # My Desktop Dir
col3 = 'purple' #only needed for plot 3
me3 = 10000    # Marker spacing
mz3 = 1     # Marker size
mk3 = 'None'
lsty3 = '-'
l3 = 'Newton on friction coefficient 0.1 to 0.1'

path4  = r'F:\PhD_Data_Back_Up\LAMMPS\Random_Packing\TX Shear\NewtonOff\TXShear100kPa_fromFC0p1to0p1\Merged' # My Desktop Dir
col4 = 'green'  #only needed for plot 3
me4 = 10000    # Marker spacing
mz4 = 1     # Marker size
mk4 = 'None'
lsty4 = '--'
l4 = 'Newton off friction coefficient 0.1 to 0.1'

# Defining Functions -----------------------------------------------------------

def get_data(path):
    # Change Directory
    os.chdir(path)
    # Mean Shear Stress
    step_en1, tkE1, rkE1, kE1, friE1, volE1, distE1, boundE1, normE1, shearE1, strainE1, locdampE1, viscodampE1, dampE1 = np.loadtxt(energy_file).T
    return step_en1, tkE1, rkE1, kE1, friE1, volE1, distE1, boundE1, normE1, shearE1, strainE1, locdampE1, viscodampE1, dampE1

def plot1(mk,me,mz,lsty):

    line1 = plt.plot(step_en1, tkE1,'red',marker=mk,markevery=me,markersize = mz,ls = lsty)
    line2 = plt.plot(step_en1, rkE1,'lightskyblue',marker=mk,markevery=me,markersize = mz,ls = lsty)
    line3 = plt.plot(step_en1, kE1,'orange',marker=mk,markevery=me,markersize = mz,ls = lsty)
    line4 = plt.plot(step_en1, friE1,'darkblue',marker=mk,markevery=me,markersize = mz,ls = lsty)
    line5 = plt.plot(step_en1, volE1,'darkviolet',marker=mk,markevery=me,markersize = mz,ls = lsty)
    line6 = plt.plot(step_en1, distE1,'dimgrey',marker=mk,markevery=me,markersize = mz,ls = lsty)
    line7 = plt.plot(step_en1, boundE1,'saddlebrown',marker=mk,markevery=me,markersize = mz,ls = lsty)
    line8 = plt.plot(step_en1, normE1,'gold',marker=mk,markevery=me,markersize = mz,ls = lsty)
    line9 = plt.plot(step_en1, shearE1,'darkseagreen',marker=mk,markevery=me,markersize = mz,ls = lsty)
    line10 = plt.plot(step_en1, strainE1,'indianred',marker=mk,markevery=me,markersize = mz,ls = lsty)
    line11 = plt.plot(step_en1, locdampE1,'royalblue',marker=mk,markevery=me,markersize = mz,ls = lsty)
    line12 = plt.plot(step_en1, viscodampE1,'cyan',marker=mk,markevery=me,markersize = mz,ls = lsty)
    line13 = plt.plot(step_en1, dampE1,'darkblue',marker=mk,markevery=me,markersize = mz,ls = lsty)

def plot2(mk,me,mz,lsty):
    step_en = step_en1 - step_en1[0]
    line1 = plt.plot(step_en, kE1,'orange',marker=mk,markevery=me,markersize = mz+1,ls = lsty, lw = lw1)
    line2 = plt.plot(step_en, friE1,'blue',marker=mk,markevery=me,markersize = mz,ls = lsty, lw = lw1)
    line3 = plt.plot(step_en, volE1,'gold',marker=mk,markevery=me,markersize = mz,ls = lsty, lw = lw1)
    line4 = plt.plot(step_en, distE1,'black',marker=mk,markevery=me,markersize = mz,ls = lsty, lw = lw1)
    line5 = plt.plot(step_en, boundE1,'green',marker=mk,markevery=me,markersize = mz,ls = lsty, lw = lw1)
    line6 = plt.plot(step_en, strainE1,'indianred',marker=mk,markevery=me,markersize = mz,ls = lsty, lw = lw1)
    line7 = plt.plot(step_en, dampE1,'darkblue',marker=mk,markevery=me,markersize = mz,ls = lsty, lw = lw1)

def plot3(col,me):
    dv1 = distE1 + volE1
    error1 = 100*((boundE1 - dv1)/boundE1)
    plt.plot(step_en1, boundE1,col,markevery=me,marker ='x')
    plt.plot(step_en1, dv1,col,markevery=me)

def create_plot(legend_names):
    plt.legend(legend_names,loc='center left', bbox_to_anchor=(1, 0.5), fontsize = LGF)
    plt.xlabel('Step', fontsize = LBF)
    plt.ylabel('Energy', fontsize = LBF)
    plt.grid()

legend_names_modified = 'translational kinetic', 'rotational kinetic', 'kinetic', 'frictional', 'volumetric', 'distortional', 'boundary', 'normal strain', 'shear strain', 'strain', 'local damping', 'viscous damping', 'damping'
legend_names1 = 'translational_kinetic simulation 1', 'rotational_kinetic simulation 1', 'kinetic simulation 1', 'friction simulation 1', 'volumetric simulation 1', 'distortional simulation 1', 'boundary simulation 1', 'normal_strain simulation 1', 'shear_strain simulation 1', 'strain simulation 1', 'local_damping simulation 1', 'viscous_damping simulation 1', 'damping simulation 1'
legend_names2 = 'translational_kinetic simulation 2', 'rotational_kinetic simulation 2', 'kinetic simulation 2', 'friction simulation 2', 'volumetric simulation 2', 'distortional simulation 2', 'boundary simulation 2', 'normal_strain simulation 2', 'shear_strain simulation 2', 'strain simulation 2', 'local_damping simulation 2', 'viscous_damping simulation 2', 'damping simulation 2'
legend_names_all = np.append(legend_names1, legend_names2)

h = plt.figure(figsize=(10,5))

step_en1, tkE1, rkE1, kE1, friE1, volE1, distE1, boundE1, normE1, shearE1, strainE1, locdampE1, viscodampE1, dampE1 = get_data(path3)
plot2(mk3,me3,mz3,lsty3)
step_en1, tkE1, rkE1, kE1, friE1, volE1, distE1, boundE1, normE1, shearE1, strainE1, locdampE1, viscodampE1, dampE1 = get_data(path4)
plot2(mk4,me4,mz4,lsty4)


legend_elements1 = [   Line2D([0], [0],color='black',linestyle = lsty3, label=l3, lw = lw1),Line2D([0], [0],color='black',linestyle = lsty4, label=l4, lw = lw1)]

legend_elements2 = [    Line2D([0], [0],color='orange', label='Kinetic', lw = lw1),Line2D([0], [0],color='blue', label='Frictional', lw = lw1),
                        Line2D([0], [0],color='gold', label='Volumetric', lw = lw1),Line2D([0], [0],color='black', label='Distortional', lw = lw1),Line2D([0], [0],color='green', label='Boundary', lw = lw1),
                        Line2D([0], [0],color='indianred', label='Strain', lw = lw1),Line2D([0], [0],color='darkblue', label='Damping', lw = lw1)]

la = legend(handles=legend_elements1,loc='upper left', fontsize = LGF)
lb = legend(handles=legend_elements2,loc='center left', fontsize = LGF)

gca().add_artist(la) # add l1 as a separate artist to the axes
gca().add_artist(lb) # add l1 as a separate artist to the axes
plt.xlim(0,400000000)
plt.ylim(0,0.0006)
plt.xlabel('Step number [N]', fontsize = LBF)
plt.ylabel('Energy (J)', fontsize = LBF)

ax = plt.gca()
t = ax.xaxis.get_offset_text()
t.set_size(TS)

plt.grid()
plt.tight_layout()
plt.show()
