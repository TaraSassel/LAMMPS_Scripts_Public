"""
    Author: Tara Sassel
    Date: 20/10/2022

    This script calculates the parameter "a" in accordance with Yimsiri and Soga
    For all cyclic loading simulations
"""

# Import Libraries
import re
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from basicFunctions.get_fabric_tensor import get_fabric_tensor_cn
from basicFunctions.yimsiriSoga import  get_a_yimsiri_soga

# ==============================================================================
# FIGURE
# Define Plot Fontsizes
TF = 24     # Text font
LGF = 12   # Legend Font Size
LBF = 15    # Label Font Size
TS = 12     # Tick Size
lw1 = 3

# Defining Path
path = r'F:\CyclicLoading\Cyclicmean\TX300_FC0p25to0p25_amp90\merged_data\SortedData\0_StartingPos'

# ==============================================================================
os.chdir(path)

# Getting Contact Dump Files
contact_files = os.listdir()

step_number = []
for contact_file in contact_files:
    step_number.append(re.findall('\d+', contact_file))
step_number = [int(step[0]) for step in step_number] # Convert string to integer

yimsiri_soga_a_value = pd.DataFrame(data = {'file_name':contact_files, 'step_number':step_number})
yimsiri_soga_a_value = yimsiri_soga_a_value.sort_values(by = ['step_number'], ascending = True)

# Initiating lists
a = []
a1 = []
a2 = []
a3 = []

# Iterating trough dump files
for contact_file in yimsiri_soga_a_value.file_name:

    # Loading contact file
    contact_data = pd.read_csv(
            contact_file,
            skiprows = 9,
            delimiter = ' ',
            index_col = False,
            header = None
        )

    # Getting Fabric Tensor
    CNfabrictensor = get_fabric_tensor_cn(contact_data)

    # Getting mean a
    a_mean, a_val1, a_val2, a_val3 = get_a_yimsiri_soga(CNfabrictensor)
    a.append(a_mean)
    a1.append(a_val1)
    a2.append(a_val2)
    a3.append(a_val3)

yimsiri_soga_a_value['a_mean'] = a
yimsiri_soga_a_value['a1'] = a1
yimsiri_soga_a_value['a2'] = a2
yimsiri_soga_a_value['a3'] = a3

# FIGURE =======================================================================
plt.figure(figsize = (10,7))
cycle_n = np.arange(0,len(yimsiri_soga_a_value.a_mean),1)
plt.plot(cycle_n, yimsiri_soga_a_value.a_mean, label = 'a', color = 'indianred', lw = 3)
plt.plot(cycle_n, yimsiri_soga_a_value.a1, label = 'a1', color = 'darkgreen', ls = '--')
plt.plot(cycle_n, yimsiri_soga_a_value.a2, label = 'a2', color = 'forestgreen', ls = ':', lw = 2)
plt.plot(cycle_n, yimsiri_soga_a_value.a3, label = 'a3', color = 'limegreen', ls = '-')

plt.legend(loc = 'upper right')
plt.xlabel('Cycle number (N)', fontsize = LBF)
plt.ylabel('a value from Yimsiri & Soga (2010)', fontsize = LBF)
plt.gca().tick_params(which='major', labelsize=TS)
plt.xlim(0,)
plt.grid()
plt.show()
