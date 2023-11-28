# Created by Tara Sassel 20.10.22

# Importing Libraries
import shutil as sh
import numpy as np
import sys
import os
import re
import fnmatch
import math
import pandas as pd

# Spectify path and name of final folder
path  = r'F:\CyclicLoading\Cyclicmean\TX300_FC0p25to0p25_amp90' # My Laptop Dir

os.chdir(path)

cycle_positions = [0,1,2,3]
position_folder_names = ['0_StartingPos','1_LoadedPos','2_NeutralPos', '3_UnloadedPos']

# ==============================================================================
# CALCULATING DUMP FILE POSITION================================================
# ==============================================================================
# Defining cyclic positions
time_step = 5.242309e-09
period = 0.25
cycle_length = int(period/(time_step))
# Cant take int here because of unsinged and signed integer
cyclic_int = np.round_(cycle_length/4, decimals = 0)
pos0 = 4*cyclic_int*np.arange(0,100,1)
pos1 = cyclic_int + pos0
pos2 = cyclic_int*2 + pos0
pos3 = cyclic_int*3 + pos0
positions = [pos0, pos1, pos2, pos3]

# ==============================================================================
# FINDING RUN FOLDERS ==========================================================
# ==============================================================================
# Finding all run directories in this directory
folder = []
folder_n = []
def get_numbers_from_filename(filename):
    return re.search(r'\d+', filename).group(0)

for directory in os.scandir(path):
        if directory.name.startswith('run') and directory.is_dir():
            #print(directory.name)
            f = get_numbers_from_filename(directory.name)
            folder_n.append(int(f))
            folder.append(directory)
folder_n.sort()

# ==============================================================================
# CREATING SUBDIRECTORIES ======================================================
# ==============================================================================
# Creating merged subfolder
try :
    os.mkdir('merged_data')
except FileExistsError:
    print("Directory merged_data already exists")

# Create sorted subfolder
os.chdir(path + r'\merged_data')
try :
    os.mkdir('SortedData')
except FileExistsError:
    print("Directory SortedData already exists")

# Create position subfolders
for position_folder in position_folder_names:
    os.chdir(path + r'\merged_data' + r'\SortedData')
    try :
        os.mkdir(position_folder)
    except FileExistsError:
        print("Directory ", position_folder,  " already exists")

    os.chdir(path + r'\merged_data' + r'\SortedData' + r'\\' + position_folder)
    #Creating subfolders
    try:
        os.mkdir('atom')
        os.mkdir('connectivity')
        os.mkdir('contact')
        os.mkdir('stress')
        os.mkdir('velocity')
    except FileExistsError:
        print("Directorys already exists")

# ==============================================================================
# SORTING DATA =================================================================
# ==============================================================================
# Iterate trough folders
for number in folder_n:
    print('Current Folder: ' + str(number))

    # ATOM =====================================================================
    atom_file_names = []
    atom_file_number = []
    # Getting all file names
    os.chdir(path + "\\" + f"run{number}")
    for atom_dump in os.scandir('atom'):
        if atom_dump.name.startswith('dump') and atom_dump.is_file():
             atom_file_names.append(atom_dump)
             f = get_numbers_from_filename(atom_dump.name)
             atom_file_number.append(int(f))
    atom_files = pd.DataFrame(data = {'file_name': atom_file_names, 'file_number': atom_file_number})
    atom_files = atom_files.sort_values(by='file_number')

    # Copying Files
    for p, position_folder in enumerate(position_folder_names):
        file_names = atom_files[atom_files['file_number'].isin(positions[p])]
        os.chdir(path)
        for atom_file in file_names.file_name:
            sh.copyfile(rf'run{number}/atom/' + atom_file.name, r'merged_data/SortedData' + r'/' + position_folder + '/atom/' + atom_file.name)

    # CONNECTIVITY =============================================================
    connectivity_file_names = []
    connectivity_file_number = []
    # Getting all file names
    os.chdir(path + "\\" + f"run{number}")
    for connectivity_dump in os.scandir('connectivity'):
        if connectivity_dump.name.startswith('dump') and connectivity_dump.is_file():
             connectivity_file_names.append(connectivity_dump)
             f = get_numbers_from_filename(connectivity_dump.name)
             connectivity_file_number.append(int(f))
    connectivity_files = pd.DataFrame(data = {'file_name': connectivity_file_names, 'file_number': connectivity_file_number})
    connectivity_files = connectivity_files.sort_values(by='file_number')

    # Copying Files
    for p, position_folder in enumerate(position_folder_names):
        file_names = connectivity_files[connectivity_files['file_number'].isin(positions[p])]
        os.chdir(path)
        for connectivity_file in file_names.file_name:
            sh.copyfile(rf'run{number}/connectivity/' + connectivity_file.name, r'merged_data/SortedData' + r'/' + position_folder + '/connectivity/' + connectivity_file.name)

    # CONTACT ==================================================================
    contact_file_names = []
    contact_file_number = []
    # Getting all file names
    os.chdir(path + "\\" + f"run{number}")
    for contact_dump in os.scandir('contact'):
        if contact_dump.name.startswith('dump') and contact_dump.is_file():
             contact_file_names.append(contact_dump)
             f = get_numbers_from_filename(contact_dump.name)
             contact_file_number.append(int(f))
    contact_files = pd.DataFrame(data = {'file_name': contact_file_names, 'file_number': contact_file_number})
    contact_files = contact_files.sort_values(by='file_number')

    # Copying Files
    for p, position_folder in enumerate(position_folder_names):
        file_names = contact_files[contact_files['file_number'].isin(positions[p])]
        os.chdir(path)
        for contact_file in file_names.file_name:
            sh.copyfile(rf'run{number}/contact/' + contact_file.name, r'merged_data/SortedData' + r'/' + position_folder + '/contact/' + contact_file.name)

    # STRESS ===================================================================
    stress_file_names = []
    stress_file_number = []
    # Getting all file names
    os.chdir(path + "\\" + f"run{number}")
    for stress_dump in os.scandir('stress'):
        if stress_dump.name.startswith('dump') and stress_dump.is_file():
             stress_file_names.append(stress_dump)
             f = get_numbers_from_filename(stress_dump.name)
             stress_file_number.append(int(f))
    stress_files = pd.DataFrame(data = {'file_name': stress_file_names, 'file_number': stress_file_number})
    stress_files = stress_files.sort_values(by='file_number')

    # Copying Files
    for p, position_folder in enumerate(position_folder_names):
        file_names = stress_files[stress_files['file_number'].isin(positions[p])]
        os.chdir(path)
        for stress_file in file_names.file_name:
            sh.copyfile(rf'run{number}/stress/' + stress_file.name, r'merged_data/SortedData' + r'/' + position_folder + '/stress/' + stress_file.name)

    # VELOCITY ==================================================================
    velocity_file_names = []
    velocity_file_number = []
    # Getting all file names
    os.chdir(path + "\\" + f"run{number}")
    for velocity_dump in os.scandir('velocity'):
        if velocity_dump.name.startswith('dump') and velocity_dump.is_file():
             velocity_file_names.append(velocity_dump)
             f = get_numbers_from_filename(velocity_dump.name)
             velocity_file_number.append(int(f))
    velocity_files = pd.DataFrame(data = {'file_name': velocity_file_names, 'file_number': velocity_file_number})
    velocity_files = velocity_files.sort_values(by='file_number')

    # Copying Files
    for p, position_folder in enumerate(position_folder_names):
        file_names = velocity_files[velocity_files['file_number'].isin(positions[p])]
        os.chdir(path)
        for velocity_file in file_names.file_name:
            sh.copyfile(rf'run{number}/velocity/' + velocity_file.name, r'merged_data/SortedData' + r'/' + position_folder + '/velocity/' + velocity_file.name)
