"""
    Author: Tara Sassel
    Date:   17/10/22

"""

import os
import re
import pandas as pd
import numpy as np
from typing import List

def get_mechCoord(path: str, dump_file_number: int) -> float:
    """
    Function to calcutale the mechnaical coodringation Number
    The path of the required run file should be provided.
    """

    # Loading connectivity data
    os.chdir(path + r'\connectivity')
    with open(f"dump{dump_file_number}.connectivity", 'r') as fp:
        header_line = fp.readlines()[8]
        header_line = header_line.replace("ITEM: ATOMS ", "")
        header_line = header_line.split()

        connectivity_data= pd.read_csv(
            f"dump{dump_file_number}.connectivity",
            skiprows = 9,
            header = None,
            names = header_line,
            delimiter = ' ',
            index_col=False)
    # ==========================================================================
    # PROCESSING DATA
    # Renaming column with coordination number
    # The only column name with a c_ will be the coordination number
    col_names = list(connectivity_data.columns)

    coordination_name = [name for name in col_names if (name[0:1] in "c_")]
    connectivity_data = connectivity_data.rename(columns = {coordination_name[0]: "coord"})

    mech_data = connectivity_data[connectivity_data["coord"]>1]
    mech_coord = np.mean(mech_data["coord"])

    return mech_coord
