"""
    Author: Tara Sassel
    Date:   17/10/22

"""

import os
import re
import pandas as pd
import numpy as np
from typing import List

def get_meanFN(path: str) -> float:
    """
    Function to calcutale the mean contact normal force
    The path of the required run file should be provided.
    """
    os.chdir(path)

    # Getting Connectivity Dump Files
    contact_files = os.listdir()

    step_number = []
    for contact_file in contact_files:
        step_number.append(re.findall('\d+', contact_file))

    step_number = [int(step[0]) for step in step_number] # Convert string to integer

    ContactNormalForce = pd.DataFrame(data = {'file_name':contact_files, 'step_number':step_number})
    ContactNormalForce = ContactNormalForce.sort_values(by = ['step_number'], ascending = True)

    FN_data = []
    for file in ContactNormalForce.file_name:
        # Loading contact data


        contact_data = pd.read_csv(
            file,
            skiprows = 9,
            header = None,
            delimiter = ' ',
            index_col=False)
        
        # Non zero contacts
        contact_data_n0 = contact_data[contact_data[3]>0]
        contact_data_n0 = contact_data_n0.to_numpy().T
    
        tfx = contact_data_n0[0,:]
        tfy = contact_data_n0[1,:]
        tfz = contact_data_n0[2,:]

        # 1. Distance between centroids (branch vector)
        X1 = contact_data_n0[6,:]
        Y1 = contact_data_n0[7,:]
        Z1 = contact_data_n0[8,:]
        R1 = contact_data_n0[9,:]

        X2 = contact_data_n0[10,:]
        Y2 = contact_data_n0[11,:]
        Z2 = contact_data_n0[12,:]
        R2 = contact_data_n0[13,:]

        n0_contacts = len(R2)

        # determining branch vector
        BV = np.sqrt(((X1-X2)**2)+((Y1-Y2)**2)+((Z1-Z2)**2)) # disk disk brach vechtor

        # Normal Force
        NF = np.mean(contact_data_n0[3,:]*BV)

        # Resulatnt shear force
        rsf = np.sqrt(tfx**2+tfy**2+tfz**2)
        FN_data.append(np.mean(NF))
    
    ContactNormalForce['meanFN'] = FN_data

    return ContactNormalForce
 