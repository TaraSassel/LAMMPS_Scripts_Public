"""
    Aim:    This script is to calculate the mechanical coordination number
    Date:   17/10/22
    Author: Tara Sassel
"""

import os
import re
import pandas as pd
import numpy as np
from typing import List

def get_mechCoord(path: str, col_names: List[str]) -> pd.DataFrame:
    """
    Function to calcutale the mechnaical coodringation Number
    Input:
        path:
        Iterates over all dump files in defined folder

        col_names:
        Names for the header.
        The column containg the coordination number has to be named coord.

    Output:
        pd.DataFrame containg file_name, step_number, mechanical_coord
    """
    os.chdir(path)

    # Getting Connectivity Dump Files
    connectivity_files = os.listdir()

    step_number = []
    for connectivity_file in connectivity_files:
        step_number.append(re.findall('\d+', connectivity_file))

    step_number = [int(step[0]) for step in step_number] # Convert string to integer

    mechanical_coord = pd.DataFrame(data = {'file_name':connectivity_files, 'step_number':step_number})
    mechanical_coord = mechanical_coord.sort_values(by = ['step_number'], ascending = True)

    mech_coord = []
    for file in mechanical_coord.file_name:
        connectivity_data = pd.read_csv(file, skiprows = 9, names = col_names, header = None, delimiter = " ", index_col = False)
        connectivity_data = connectivity_data[connectivity_data.coord > 1] # Only including particles with contact
        mech_coord.append(np.mean(connectivity_data.coord))
    mechanical_coord['mechanical_coord'] = mech_coord

    return mechanical_coord
