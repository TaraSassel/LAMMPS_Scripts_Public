"""
Author: Tara
Date: 03/11/2022

Script contains function fetch all columns from dump files
"""
# Imports
import os
import fnmatch
import pandas as pd
from typing import List

def get_combinedDump(
        path: str,
        folder_list: List,
        dump_file_number: int)-> pd.DataFrame:
    """
    Function creates a df that containing all columns
    from dump files for this specified timestep
    """
    # Collecting Data
    all_dump_files = {}
    for folder in folder_list:
        os.chdir(path+ r'/' + folder)
        file_name = fnmatch.filter(os.listdir('.'), f'dump{dump_file_number}.*')

        with open(file_name[0], 'r') as fp:
            header_line = fp.readlines()[8]
            header_line = header_line.replace("ITEM: ATOMS ", "")
            header_line = header_line.split()

            dump_file = pd.read_csv(
                file_name[0],
                skiprows = 9,
                header = None,
                names = header_line,
                delimiter = ' ',
                index_col=False)
            all_dump_files[folder] = dump_file

    # Combining all dump files on sphere id
    combined_dump = pd.merge(all_dump_files['atom'], all_dump_files['connectivity'], on = 'id')
    combined_dump = pd.merge(combined_dump, all_dump_files['stress'], on = 'id')
    combined_dump = pd.merge(combined_dump, all_dump_files['velocity'], on = 'id')

    # Checking if there is diameter, Ovito needs radius
    header_list = combined_dump.columns.tolist()
    if 'diameter' in header_list:
        combined_dump['diameter'] = combined_dump['diameter'].div(2)
        combined_dump.rename(columns = {'diameter':'radius'}, inplace = True)

    return combined_dump
