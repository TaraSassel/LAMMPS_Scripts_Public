"""
Author: Tara Sassel
Date: 06/04/2023
This figure plots the deviatoric stress tensor vs cycle number  
"""

# Imports 
import re 
import os 
import pandas as pd
import numpy as np
from numpy import linalg as LA
from tqdm import tqdm


from cyclicStrain import get_strain_info
from basicFunctions.get_fabric_tensor import get_fabric_tensor_cn

# =================================================================================================
strainInfo = get_strain_info(None)   # Drive Number example: 'E'
N = 101                              # Number of cycles
pos = "Starting_Position"

# Define wanted dataset 
which_iso_stress =  None                # 100, 200 or 300
which_strain_amplitude = None           # 0.1, 0.5 or 1
which_friction_coefficient = None       # 0.1, 0.15 or 0.25

# =================================================================================================
# change directory to selected data set
wanted_data = strainInfo[
    (strainInfo.iso_stress == which_iso_stress) &\
    (strainInfo.strain_amplitude == which_strain_amplitude) &\
    (strainInfo.friction_coefficient == which_friction_coefficient)]

path_list = list(wanted_data.path)
cyclic_turns = list(wanted_data.cyclic_turns)

os.chdir(path_list[0] + r'/merged_data')

path = path_list[0]
print(path)

# Get cyclic turns 
os.chdir(path + r'\template')
for line in open('continue_cyclic.in'):
    match = re.search('interval_dump equal (\d+)', line)
    if match:
        cyclic_turns = 2*int(match.group(1))

os.chdir(path + rf'\SortedData\{pos}\contact')

# Initiating df 
data = []
files_df = pd.DataFrame(data)


directory = os.getcwd()
for root, dirs, files in os.walk(directory):
    for file in tqdm(files):
        if file.endswith('.contact'):

            num = re.findall(r'\d+', file) 
            number = int(num[0])
            cycle = int(number/cyclic_turns)

            # Loading contact file
            contact_df = pd.read_csv(
                    f'dump{number}.contact',
                    skiprows = 9,
                    delimiter = ' ',
                    index_col = False,
                    header = None
                )
            # Get mech coord
            ft = get_fabric_tensor_cn(contact_df)
            w, v = LA.eig(ft)
            ftd = max(w) - min(w)

            data = {
                    'number': [number], 
                    'ftd': ftd, 
                    'file_name':[file]
                }
            
            temp_df = pd.DataFrame(data)

            files_df = pd.concat([files_df, temp_df], ignore_index=True)


files_df = files_df.sort_values(by = ['number'])
files_df['cycle'] = np.arange(0,len(files_df))

os.chdir(path_list[0] + r'/merged_data')

print("Saving file")
# Saving data 
files_df.to_csv("deviatoricFabric.csv", index=False)