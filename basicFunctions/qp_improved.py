import os
import fnmatch
import numpy as np
import pandas as pd

# Function to get q p
def get_qp(path):    # Input path, timestep, prominence, color, number of cycles, timestep
    # Change Directory
    os.chdir(path)
    # Names of Files
    for (dirpath, dirnames, filenames) in os.walk(path):
        for file in filenames:
            if file.endswith(".txt"):
                if fnmatch.fnmatch(file,"*stress*"):
                    stress_file = file
                    print(stress_file)

    # Mean Shear Stress
    print('Processing Stresses')
    df = pd.read_csv(stress_file,delimiter = ' ', header = None, index_col = None)
    step_s, stress_xx, stress_yy, stress_zz, stress_xy, stress_xz, stress_yz, length_x, length_y, length_z = df.to_numpy().T
    step_s = step_s - step_s[0]

    q = np.zeros(len(stress_xx))
    p = np.zeros(len(stress_xx))

    i = 0

    while i <= float(len(stress_xx)-1):

        q[i] = (stress_zz[i] - stress_xx[i])
        #q[i] = np.sqrt(0.5*((stress_xx[i]-stress_yy[i])**2+(stress_yy[i]-stress_zz[i])**2+(stress_xx[i]-stress_zz[i])**2+3*(stress_xy[i]**2+stress_yz[i]**2+stress_xz[i]**2)))
        p[i] = (stress_xx[i] + stress_yy[i] + stress_zz[i])/3
        i = i + 1


    delta_xx = np.zeros(len(stress_xx))
    delta_yy = np.zeros(len(stress_xx))
    delta_zz = np.zeros(len(stress_xx))

    for i in range(len(step_s)):

        delta_xx[i] =  length_x[0] - length_x[i]
        delta_yy[i] =  length_y[0] - length_y[i]
        delta_zz[i] =  length_z[0] - length_z[i]

    xstrain =delta_xx/length_x[0]
    ystrain =delta_yy/length_y[0]
    zstrain =delta_zz/length_z[0]

    # Tan Stiffness
    tanstiffness = np.zeros(len(stress_xx))
    j = 0
    while j < len(stress_xx):
        tanstiffness[i] =(q[i]-q[i-1])/(zstrain[i]-zstrain[i-1])
        j = j + 1

    return xstrain, ystrain, zstrain, q, p, tanstiffness, step_s, stress_xx, stress_yy, stress_zz, stress_xy, stress_xz, stress_yz, length_x, length_y, length_z
