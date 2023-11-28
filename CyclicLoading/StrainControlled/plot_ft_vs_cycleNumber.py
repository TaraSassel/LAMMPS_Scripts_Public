"""
Author: Tara Sassel
Date: 06/04/2023
This figure plots the deviatoric stress tensor vs cycle number  
"""

# Imports 
import re 
import os 
import numpy as np
from numpy import linalg as LA
import pandas as pd
import seaborn as sns 
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
import matplotlib.ticker as ticker
import matplotlib.colors

from cyclicStrain import get_strain_info
from basicFunctions.get_fabric_tensor import get_fabric_tensor_cn

# =================================================================================================
strainInfo = get_strain_info("E") # Drive Number example: 'E'
N = 101             # Number of cycles
pos = "Starting_Position"

# Fontisze
LBF = 18    # Label Fontsize
TS = 16     # Ticksize
CBF = 18    # Colorbar Font

# Define wanted dataset 
which_iso_stress = 300             # 100, 200 or 300
which_strain_amplitude = 1       # 0.1, 0.5 or 1
which_friction_coefficient = 0.25   # 0.1, 0.15 or 0.25

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

# Get cyclic turns 
os.chdir(path + r'\template')
for line in open('continue_cyclic.in'):
    match = re.search('interval_dump equal (\d+)', line)
    if match:
        cyclic_turns = 2*int(match.group(1))
        print(cyclic_turns)

os.chdir(path + rf'\SortedData\{pos}\contact')

# Initiating df 
data = []
files_df = pd.DataFrame(data)


directory = os.getcwd()
for root, dirs, files in os.walk(directory):
    for file in files:
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
            print(ft)
            w, v = LA.eig(ft)
            print(w)
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

# Figure
plt.plot(files_df.cycle,files_df.ftd, marker = 'o', mec = 'black', mfc = 'navy')


plt.xlabel('Cycle number (N)')
plt.ylabel(r'Deviatoric fabric tensor ($\psi_d$)')
plt.show()
