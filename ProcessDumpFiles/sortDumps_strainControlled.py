# Author: Tara Sassel
# Date: 29/03/2023

# Import Libraries
import re 
import os
import shutil as sh
import numpy as np


# =================================================================================================
# Define 
path = None
pos = 'Position_Loaded' # Select name for folder for example Position_Loaded, Position_Unoaded
N = 202

# Get cyclic turns 
os.chdir(path + r'\template')
for line in open('continue_cyclic.in'):
    match = re.search('interval_dump equal (\d+)', line)
    if match:
        cyclic_turns = 2*int(match.group(1))
        print(cyclic_turns)

# Change according to what you want 
wanted_files = np.arange(cyclic_turns, cyclic_turns*N, cyclic_turns*2)

# =================================================================================================
# Change directory 
os.chdir(path)

wanted_atom_files = []
wanted_connectivity_files = []
wanted_contact_files = []
wanted_stress_files = []
wanted_velocity_files = []
for i in range(len(wanted_files)):
    wanted_atom_files.append("dump" + str(wanted_files[i])+".atom")
    wanted_connectivity_files.append("dump" + str(wanted_files[i])+".connectivity")
    wanted_contact_files.append("dump" + str(wanted_files[i])+".contact")
    wanted_stress_files.append("dump" + str(wanted_files[i])+".stress")
    wanted_velocity_files.append("dump" + str(wanted_files[i])+".all_velocities")

# Finding all run directories in this directory
folder = []
for directory in os.scandir(path):
     if directory.name.startswith('run') and directory.is_dir():
         print(directory.name)
         folder.append(directory)

# Sorted Folder
dirName = 'SortedData'

try :
    os.mkdir(dirName)
except FileExistsError:
    print("Directory " ,dirName,  " already exists")
os.chdir(dirName)

# Selected Position
#Creating subfolders

try :
    os.mkdir(pos)
except FileExistsError:
    print("Directory " ,dirName,  " already exists")
os.chdir(pos)

try:
    os.mkdir('atom')
    os.mkdir('connectivity')
    os.mkdir('contact')
    os.mkdir('stress')
    os.mkdir('velocity')
    #os.mkdir('restart')

except FileExistsError:
    print("Directories already exist")
os.chdir('..')


print('Copying dump files from folder:')
for i in range(len(folder)):
    print(folder[i])
    atom_files = []
    connectivity_files = []
    contact_files = []
    stress_files = []
    velocity_files = []

    os.chdir(path + "\\" + folder[i].name)

    # Getting all file names

    # atom folder
    for atom_dump in os.scandir('atom'):
         if atom_dump.name.startswith('dump') and atom_dump.is_file():
             dones = []
             for k in range(len(wanted_files)):
                 wanted_file_name = wanted_atom_files[k]
                 if atom_dump.name.endswith(wanted_file_name):
                    atom_files.append(atom_dump)
                    print(atom_files)

    atom_files.sort(key= os.path.getmtime) # Needed if increase from dump9899 to dump10203

    # connectivity folder
    for connectivity_dump in os.scandir('connectivity'):
        if connectivity_dump.name.startswith('dump') and connectivity_dump.is_file():
            for k in range(len(wanted_files)):
                wanted_file_name = wanted_connectivity_files[k]
                if connectivity_dump.name.endswith(wanted_file_name):
                    connectivity_files.append(connectivity_dump)
    connectivity_files.sort(key= os.path.getmtime)

    # contact folder
    for contact_dump in os.scandir('contact'):
        if contact_dump.name.startswith('dump') and contact_dump.is_file():
            for k in range(len(wanted_files)):
                wanted_file_name = wanted_contact_files[k]
                if contact_dump.name.endswith(wanted_file_name):
                    contact_files.append(contact_dump)
    contact_files.sort(key= os.path.getmtime)

    # stress folder
    for stress_dump in os.scandir('stress'):
        if stress_dump.name.startswith('dump') and stress_dump.is_file():
            for k in range(len(wanted_files)):
                wanted_file_name = wanted_stress_files[k]
                if stress_dump.name.endswith(wanted_file_name):
                    stress_files.append(stress_dump)
    stress_files.sort(key= os.path.getmtime)

    # stress folder
    for velocity_dump in os.scandir('velocity'):
        if velocity_dump.name.startswith('dump') and velocity_dump.is_file():
            for k in range(len(wanted_files)):
                wanted_file_name = wanted_velocity_files[k]
                if velocity_dump.name.endswith(wanted_file_name):
                        velocity_files.append(velocity_dump)
    velocity_files.sort(key= os.path.getmtime)
    os.chdir('..')

    print('current directory')
    print(os.getcwd())
    if len(atom_files) > 0:
        for j in range(len(atom_files)):
            print("Copying file from directory " + folder[i].name)
            sh.copyfile(folder[i].name + '/atom/' + atom_files[j].name, dirName + '/'+ pos + '/atom/' + atom_files[j].name)
            sh.copyfile(folder[i].name + '/connectivity/' + connectivity_files[j].name, dirName + '/'+ pos + '/connectivity/' + connectivity_files[j].name)
            sh.copyfile(folder[i].name + '/contact/' + contact_files[j].name, dirName + '/'+ pos + '/contact/' + contact_files[j].name)
            sh.copyfile(folder[i].name + '/stress/' + stress_files[j].name, dirName + '/'+ pos + '/stress/' + stress_files[j].name)
            sh.copyfile(folder[i].name + '/velocity/' + velocity_files[j].name, dirName + '/'+ pos + '/velocity/' + velocity_files[j].name)
