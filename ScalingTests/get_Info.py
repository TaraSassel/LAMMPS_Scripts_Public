# Get Scaling Test Info
# Tara Sassel 27/10/2021

import os
import fnmatch
import datetime
import numpy as np
import time
import re   # regular expression operations
from glob import glob

path = r'E:\Molecules\ScalingTestMolecules\22k_Sample' # Path to main directory 
os.chdir(path)

# function to convert walltime to seconds
def time_to_sec(t):
   h, m, s = map(int, t.split(':'))
   return h * 3600 + m * 60 + s
dirlist = []
for (dirpath, dirnames, filenames) in os.walk(path):
    for dir in dirnames:
        if fnmatch.fnmatch(dir,"*Core*"):
            dirlist = np.append(dirlist,dir)
print(dirlist)

for i in range(len(dirlist)):
    os.chdir(path+'\\'+dirlist[i])
    print(path+'\\'+dirlist[i])
    # Names of Files
    for (dirpath, dirnames, filenames) in os.walk(path+'\\'+dirlist[i]):
        for file in filenames:
            if fnmatch.fnmatch(file,"*.sh.o*"):
                file_name = file
                print(file_name)

    # Finding Info
    with open(file_name,'r') as f:
        for line in f:
            # Capturing Walltime
            if 'Total wall time:' in line:
                walltime = line.partition('Total wall time:')[2] # This partitions after : so the second entry is my time
                walltime = time_to_sec(walltime)

            # Capturing NCPUs
            if 'Loop time' in line:
                NCPUs = [float(s) for s in re.findall(r'-?\d+\.?\d*', line)][1] # I know the second value is the NCPUs

            # Capturing NCPUs
            if 'Per MPI rank memory allocation' in line:
                Memory = [float(s) for s in re.findall(r'-?\d+\.?\d*', line)][2] # Used Memory

            # Caturing Nlocal
            if 'Nlocal:' in line:
                Nlocal = [float(s) for s in re.findall(r'-?\d+\.?\d*', line)][0] # I know the first entry is the avarage

            # Capturing Nghost
            if 'Nghost:' in line:
                Nghost = [float(s) for s in re.findall(r'-?\d+\.?\d*', line)][0] # I know the first entry is the avarage

            # Capturing Neighs
            if 'Neighs:' in line:
                Neighs = [float(s) for s in re.findall(r'-?\d+\.?\d*', line)][0] # I know the first entry is the avarage

            # Capturing FullNghs
            if 'FullNghs:' in line:
                FullNghs = [float(s) for s in re.findall(r'-?\d+\.?\d*', line)][0] # I know the first entry is the avarage

            # Capturing Pair time info
            if 'Pair    |' in line:
                Pair_t = [float(s) for s in re.findall(r'-?\d+\.?\d*', line)][1] # avarage
                Pair_p = [float(s) for s in re.findall(r'-?\d+\.?\d*', line)][4] # percentage
            # Capturing Neigh time info
            if 'Neigh   |' in line:
                Neigh_t = [float(s) for s in re.findall(r'-?\d+\.?\d*', line)][1] # avarage
                Neigh_p = [float(s) for s in re.findall(r'-?\d+\.?\d*', line)][4] # percentage
            # Capturing Comm time info
            if 'Comm    |' in line:
                Comm_t = [float(s) for s in re.findall(r'-?\d+\.?\d*', line)][1] # avarage
                Comm_p = [float(s) for s in re.findall(r'-?\d+\.?\d*', line)][4] # percentage
            # Capturing Output time info
            if 'Output  |' in line:
                Output_t = [float(s) for s in re.findall(r'-?\d+\.?\d*', line)][1] # avarage
                Output_p = [float(s) for s in re.findall(r'-?\d+\.?\d*', line)][4] # percentage

            # Capturing Modify time info
            if 'Modify  |' in line:
                Modify_t = [float(s) for s in re.findall(r'-?\d+\.?\d*', line)][1] # avarage
                Modify_p = [float(s) for s in re.findall(r'-?\d+\.?\d*', line)][4] # percentage
            # Capturing Other time info
            if 'Other   |' in line:
                Other_t = [float(s) for s in re.findall(r'-?\d+\.?\d*', line)][0] # avarage
                Other_p = [float(s) for s in re.findall(r'-?\d+\.?\d*', line)][1] # percentage

    f.close()

    # Creating Output
    os.chdir("..")

    info_file = 'ScalingTestInfo.txt'
    dirName = 'ScalingTestInfo'

    if i == 0:
        # Creating new directory
        try :
            os.mkdir(dirName)
        except FileExistsError:
            print("Directory " ,dirName,  " already exists")

        os.chdir(path + "\\ScalingTestInfo")

        with open(info_file, 'w') as f:
            f.write('NCPUs Walltime Memory Nlocal Nghost Neighs FullNghs Pair_time Pair_per Neigh_time Neigh_per Comm_time Comm_per Output_time Output_per Modify_time Modify_per Other_time Other_per\n')
        f.close()

    os.chdir(path + "\\ScalingTestInfo")
    with open(info_file, 'a') as f:
        f.write('%i %i %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f\n' % (NCPUs, walltime, Memory, Nlocal, Nghost, Neighs, FullNghs, Pair_t, Pair_p, Neigh_t, Neigh_p, Comm_t, Comm_p, Output_t, Output_p, Modify_t, Modify_p, Other_t, Other_p))
