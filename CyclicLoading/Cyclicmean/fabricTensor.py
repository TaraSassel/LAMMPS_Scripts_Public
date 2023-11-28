"""
Author: Tara Sassel
Date: 10/11/2022

This scrip creates a csv file containing the fabric tensor
"""
# Imports
import re
import os
import pandas as pd
import multiprocessing
from typing import Tuple
from basicFunctions.get_fabric_tensor import get_fabric_tensor_cn

# ==============================================================================
path = r"E:\CyclicLoading\Cyclicmean\TX300_FC0p25to0p25_amp15\merged_data\SortedData" # Path to sorted data
pos_list = ['0_StartingPos', '1_LoadedPos', '2_NeutralPos', '3_UnloadedPos']

# ==============================================================================
def get_tensor(path: str, pos: str)-> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    This calculates the fabric tensor
    The two dataframes that are output are:
        fabric tensor: smallest to largest
            step_number
            ft1
            ft2
            ft3
        file_names:
            file_name
            step_number
    """

    # Chaning directory
    os.chdir(path + r'\\' + pos + r'\\contact')

    # Sorting Contact Dump Files
    contact_files = os.listdir()


    step_number = []
    for contact_file in contact_files:
        step_number.append(re.findall('\d+', contact_file))
    step_number = [int(step[0]) for step in step_number] # Convert string to integer

    file_names = pd.DataFrame(data = {'file_name':contact_files, 'step_number':step_number})
    file_names = file_names.sort_values(by = ['step_number'], ascending = True)
    file_names.reset_index()

    # Processing Dumpfiles
    fabric_tensor = pd.DataFrame(data={'step_number':[],'ft3':[], 'ft2':[], 'ft1':[]})
    fabric_tensor_xyz = pd.DataFrame(data={'step_number':[],'ftxx':[], 'ftyy':[], 'ftzz':[]})

    for i, contact_file in enumerate(file_names.file_name):
            step_number = file_names.step_number[i]

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
            t1 = CNfabrictensor[0,0]
            t2 = CNfabrictensor[1,1]
            t3 = CNfabrictensor[2,2]
            ftxyz = [t1,t2,t3]
            ftxyz.insert(0, step_number)
            fabric_tensor_xyz.loc[len(fabric_tensor)] = ftxyz

            ft = [t1,t2,t3]
            ft.sort()
            ft.insert(0, step_number)
            fabric_tensor.loc[len(fabric_tensor)] = ft

    return fabric_tensor, fabric_tensor_xyz, file_names

# ==============================================================================

for pos in pos_list:
    print(pos)
    fabric_tensor, fabric_tensor_xyz, file_names = get_tensor(path, pos)
    fabric_tensor_data = pd.merge(file_names, fabric_tensor, on = 'step_number')
    fabric_tensor_data_xyz = pd.merge(file_names, fabric_tensor_xyz, on = 'step_number')
    os.chdir(path + r'\\' + pos)
    fabric_tensor_data.to_csv("fabric_tensor.csv",index=False)
    fabric_tensor_data_xyz.to_csv("fabric_tensor_xyz.csv",index=False)
