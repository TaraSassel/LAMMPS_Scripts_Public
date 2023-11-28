# Axial strain (X axis) vs Volumetric Strain (Y axes# Energy Balance by Tara Sassel 19.06.2020

# Importing Libraries
import numpy as np
import scipy.io as sio
import math
import sys
import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.lines import Line2D
from matplotlib import pyplot
from matplotlib.pyplot import *
import fnmatch
from PIL import Image

# Define Plot Fontsizes
TF = 20     # Title Font Size
LGF = 20    # Legend Font Size
LBF = 15    # Label Font Size
TS = 12     # Tick Size
me1 = 23    # Marker spacing
me2 = 30    # Marker spacing
mz1 = 3     # Marker size
mz2 = 4     # Marker size
width_in_inches = 10
height_in_inches = 10

# Change Directory
path  = r'F:\YieldSurface\YieldSurface_Cyclicmean\C0\Merged' # My Desktop Dir
os.chdir(path)

#===============================================================================
def get_data(path):

    os.chdir(path)
    # Names of Files
    for (dirpath, dirnames, filenames) in os.walk(path):
        for file in filenames:
            if file.endswith(".txt"):
                if fnmatch.fnmatch(file,"*stress*"):
                    stress_file = file
                    print(stress_file)
                # if fnmatch.fnmatch(file,"*energy*"):
                #     energy_file = file
                #     print(energy_file)

    # Mean Stresses
    print('Processing Stresses')
    data = pd.read_csv(stress_file, delimiter = " ")
    step_s, stress_xx, stress_yy, stress_zz, stress_xy, stress_xz, stress_yz, length_x, length_y, length_z = pd.DataFrame(data).to_numpy().T
    # step_s, stress_xx, stress_yy, stress_zz, stress_xy, stress_xz, stress_yz, length_x, length_y, length_z = np.loadtxt(stress_file).T


    # delta_xx = np.zeros(len(stress_xx))
    # delta_yy = np.zeros(len(stress_xx))
    delta_zz = np.zeros(len(stress_xx))

    for i in range(len(stress_xx)):

        # delta_xx[i] =  length_x[0] - length_x[i]
        # delta_yy[i] =  length_y[0] - length_y[i]
        delta_zz[i] =  length_z[0] - length_z[i]

    # xstrain =delta_xx*100/length_x[0]
    # ystrain =delta_yy*100/length_y[0]
    zstrain =delta_zz*100/length_z[0]

    # delta_xstrain = xstrain[0] - xstrain
    # delta_ystrain = ystrain[0] - ystrain
    delta_zstrain = zstrain[0] - zstrain
    p = (stress_xx + stress_yy + stress_zz)/3
    q = np.sqrt(0.5*((stress_xx-stress_yy)**2+(stress_yy-stress_zz)**2+(stress_xx-stress_zz)**2+3*(stress_xy**2+stress_yz**2+stress_xz**2)))
    return stress_zz, delta_zstrain, q, p
