# Author: Tara Sassel
# Date: 04/07/2023

"""
Script to create csv file containg:
    - Mechanical coordination number
    - Mean degree of anisotrophy
    - Mean contact normal force 

    Note: dump files should be sorted 
"""

# Imports
import os 
import numpy as np 
import pandas as pd

from basicFunctions.MechanicalCoordinationNumber import get_mechCoord
from basicFunctions.MeanFN import get_meanFN
from basicFunctions.get_a import get_a

# Path 
path = None # Specify path

# Mechanical Coordination Number
mech_coord = get_mechCoord(
    path + r'\SortedData\Neutral_Pos\connectivity',
    ['id','diameter','coord'])

# Mechanical Coordination Number
mean_FN = get_meanFN(
    path + r'\SortedData\Neutral_Pos\contact')

# Get degree of Anisotrophy 
a_value = get_a(
    path + r'\SortedData\Neutral_Pos\contact')

merged_data = mech_coord.merge(mean_FN, how = 'left', on = 'step_number')
merged_data = merged_data.merge(a_value, how = 'left', on = 'step_number')

# Adding cycle numbers
cycle_number = np.arange(0,len(merged_data.step_number),1)
merged_data['cycle_number'] = cycle_number

print(merged_data)
# Save DataFrame 
os.chdir(path + r'\SortedData\Neutral_Pos')
merged_data.to_csv("FN_CN_a.csv", index=False)  