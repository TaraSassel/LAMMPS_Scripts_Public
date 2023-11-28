"""
Author: Tara
Date: 03/11/2022
-------------------------------------------------------
Guide:
Script creates a custom dump file to visulaise in Ovito
The wanted columns should be specified in the "wanted_columns"

    id:             sphere id
    type:           type of sphere
    x:              x-coordinate
    y:              y-coordinate
    z:              z-coordinate
    radius:         sphere radius
    c_*:            coordination number
    c_*_stress[1]:  stress in the xx - direction
    c_*_stress[2]:  stress in the yy - direction
    c_*_stress[3]:  stress in the zz - direction
    c_*_stress[4]:  stress in the xy - direction
    c_*_stress[5]:  stress in the xz - direction
    c_*_stress[6]:  stress in the yz - direction
    vx:             velocity in the x-direction
    vy:             velocity in the y-direction
    vz:             velocity in the z-direction
    fx:             force on the x-direction
    fy:             force in the y-direction
    fz              force in the z-direction
"""

# Imports
import os
import fnmatch
import pandas as pd
import numpy as np

from basicFunctions.get_combinedDump import get_combinedDump

# =============================================================================
dump_file_number = 0 # timestep of dumpfile
path = r'E:\Molecules\CyclicMolecule\AR1p1_FC0p25_200_60_Trial2\run1'
folder_list = ['atom', 'connectivity', 'stress', 'velocity']
wanted_columns = ['id','x','y','z','radius','c_2']

# =============================================================================
# Getting Custom Dump data
combined_dump = get_combinedDump(path, folder_list,dump_file_number)

sxx = combined_dump['c_1_stress[1]'].to_numpy().T
syy = combined_dump['c_1_stress[2]'].to_numpy().T
szz = combined_dump['c_1_stress[3]'].to_numpy().T
sxy = combined_dump['c_1_stress[4]'].to_numpy().T
sxz = combined_dump['c_1_stress[5]'].to_numpy().T
syz = combined_dump['c_1_stress[6]'].to_numpy().T

q_values = (1/2*((sxx-syy)**2+(sxx-szz)**2+(syy-szz)**2 + 3*(sxy**2+sxz**2+syz**2)))**(1/2)

combined_dump['q'] = q_values

custom_dump = combined_dump[wanted_columns].copy()
# ------------------------------------------------------------------------------
# Creating Header Section
file_name = fnmatch.filter(os.listdir('.'), f'dump{dump_file_number}.*')
with open(file_name[0]) as myfile:
    hearder_section = [next(myfile) for x in range(8)]
hearder_section = ''.join(hearder_section)

line1 = ' '.join(wanted_columns)
line1 = "ITEM: ATOMS " + line1 + "\n"
hearder_section = hearder_section + line1

# ------------------------------------------------------------------------------
# Creating Directory to store dump files
directory_name = 'custom_dump'
os.chdir(path)
try:
    os.mkdir(directory_name)
except FileExistsError:
    print("Directory " ,directory_name,  " already exists")
os.chdir(path + '\\' + directory_name)

# ------------------------------------------------------------------------------
# Creating file containg custom data
custom_dump.to_csv("data.txt", sep=' ', index=False, header=False)

# Creating text file containg header section
try :
    os.remove("header.txt")
except FileNotFoundError:
    pass

file_object = open("header.txt","a")
file_object.seek(0)
file_object.write(hearder_section)
file_object.close()

filenames = ['header.txt', 'data.txt']
with open(f'dump{dump_file_number}.custom', 'w') as outfile:
    for fname in filenames:
        with open(fname) as infile:
            for line in infile:
                outfile.write(line)

os.remove("header.txt")
os.remove("data.txt")
