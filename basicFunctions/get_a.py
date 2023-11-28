"""
    Author: Tara Sassel
    Date:   17/10/22

"""

import os
import re
import pandas as pd
import numpy as np
from typing import List

from basicFunctions.get_fabric_tensor import get_fabric_tensor_cn
from basicFunctions.yimsiriSoga import  get_a_yimsiri_soga

def get_a(path: str) -> float:
    """
    Function to calcutale the degree of anisotophy
    The path of the required run file should be provided.
    """
    os.chdir(path)

    # Getting Connectivity Dump Files

    # Getting Contact Dump Files
    contact_files = os.listdir()

    step_number = []
    for contact_file in contact_files:
        step_number.append(re.findall('\d+', contact_file))
    step_number = [int(step[0]) for step in step_number] # Convert string to integer

    a_value = pd.DataFrame(data = {'file_name':contact_files, 'step_number':step_number})
    a_value = a_value.sort_values(by = ['step_number'], ascending = True)

    # Initiating lists
    a = []

    # Iterating trough dump files
    for contact_file in a_value.file_name:

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


    a_value['a_mean'] = a_mean
        
    return a_value
    