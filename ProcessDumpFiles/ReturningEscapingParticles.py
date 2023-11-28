"""
Author: Tara Sassel
Date: 07/11/2022

In this script I am taking the concept from Galloway et al. (2022)
"""
# Imports
import os
import re
import fnmatch
import pandas as pd
import numpy as np

from basicFunctions.get_combinedDump import get_combinedDump

# Create a map of dump files:
path = rf'F:\CyclicLoading\Cyclicmean\TX300_FC0p25to0p25_amp90\run{r}'

def get_numbers_from_filename(filename):
    return re.search(r'\d+', filename).group(0)

for r in


# path0 = r'F:\CyclicLoading\Cyclicmean\TX300_FC0p25to0p25_amp90\run1'# Path to the reference file.
# path1 = r'F:\CyclicLoading\Cyclicmean\TX300_FC0p25to0p25_amp90\run1'#  dump2384445400
#
# dump_file_number = 0
# folder_list = ['atom','connectivity','stress','velocity']
# combined_dump0 = get_combinedDump(path0, folder_list,dump_file_number)
# combined_dump1 = get_combinedDump(path1, folder_list,47688908)
#
# merged_dump = pd.merge(combined_dump0, combined_dump1, on ='id')
# xi = merged_dump.x_x.to_numpy().T
# xf = merged_dump.x_y.to_numpy().T
# yi = merged_dump.y_x.to_numpy().T
# yf = merged_dump.y_y.to_numpy().T
# zi = merged_dump.z_x.to_numpy().T
# zf = merged_dump.z_y.to_numpy().T
#
# diff = np.sqrt((xi-xf)**2+(yi-yf)**2+(yi-yf)**2)**2
#
# Dmin = np.min(combined_dump0.radius*2)
# Dmin_sq = Dmin**2
#
# count_escaping = 0
# count_remaining = 0
# for d in diff:
#     if d > Dmin_sq:
#         count_escaping += 1
#     else:
#         count_remaining += 1
#
# print(count_escaping)
# print(count_remaining)
