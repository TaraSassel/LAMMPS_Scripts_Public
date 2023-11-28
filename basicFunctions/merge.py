# Function to merge data
import os
import re
import pandas as pd
import fnmatch

def merge_runs(
    path: str,
    merge_stress: bool = False,
    merge_energy: bool = False,
    merge_coord: bool = False,
    merge_void: bool = False
) -> pd.DataFrame:
    '''
    This function merges the txt files in diffrent runs.
    Creates a csv file that is returned in a a subdirectory called merged_data
    '''
    os.chdir(path)
    print (f"{'Directory to be merged: ':<30}{path:<40}")
    dirName = 'merged_data' # Name of subdirectory where data is saved
    print("File names:")
    # Names of Files
    for (dirpath, dirnames, filenames) in os.walk(path + r'\run1'): #run1
        for file in filenames:
            if file.endswith(".txt"):
                if fnmatch.fnmatch(file,"*stress*"):
                    stress_file = file
                    print(f"{'':<30}{stress_file:<30}")
                if fnmatch.fnmatch(file,"*voidratio*"):
                    void_ratio_file = file
                    print(f"{'':<30}{void_ratio_file:<30}")
                if fnmatch.fnmatch(file,"*coord*"):
                    coord_file = file
                    print(f"{'':<30}{coord_file:<30}")
                if fnmatch.fnmatch(file,"*energy*"):
                    energy_file = file
                    print(f"{'':<30}{energy_file:<30}")

    # Finding all run directories in this directory
    folder = []
    folder_n = []
    def get_numbers_from_filename(filename):
        return re.search(r'\d+', filename).group(0)

    for directory in os.scandir(path):
         if directory.name.startswith('run') and directory.is_dir():
             #print(directory.name)
             f = get_numbers_from_filename(directory.name)
             folder_n.append(int(f))
             folder.append(directory)
    folder_n.sort()

    # Creating new subfolder
    try :
        os.mkdir(dirName)
    except FileExistsError:
        pass
        #print("Directory " ,dirName,  " already exists")

    # Initiating DataFrames
    stress_data = pd.DataFrame()
    energy_data = pd.DataFrame()
    void_data = pd.DataFrame()
    coord_data = pd.DataFrame()

    for number in folder_n:
        os.chdir(path + "\\" + f"run{number}")
        print('Current Folder: run' + str(number))

        if merge_stress is True:
            stress_names = [
            'step_s',
            'stress_xx',
            'stress_yy',
            'stress_zz',
            'stress_xy',
            'stress_xz',
            'stress_yz',
            'length_x',
            'length_y',
            'length_z'
            ]

            stress_data_run = pd.read_csv(stress_file, index_col=None, delimiter = ' ', skiprows = 1, names = stress_names)
            stress_data = stress_data.append(stress_data_run)

        if merge_energy is True:
            energy_names = [
            'step_e',
            'tkE',
            'rkE',
            'kE',
            'friE',
            'volE',
            'distE',
            'boundE',
            'normE',
            'shearE',
            'strainE',
            'locdampE',
            'viscodampE',
            'dampE'
            ]
            energy_data_run = pd.read_csv(energy_file, index_col=None, delimiter = ' ', skiprows = 1, names = energy_names)
            energy_data = energy_data.append(energy_data_run)

        if merge_coord is True:
            coord_names = ['step_c', 'coord_number']
            coord_data_run = pd.read_csv(coord_file, index_col=None, delimiter = ' ', skiprows = 1, names = coord_names)
            coord_data = coord_data.append(coord_data_run)

        if merge_void is True:
            void_names = ['step_v', 'void_ratio']
            void_data_run = pd.read_csv(void_ratio_file, index_col=None, delimiter = ' ', skiprows = 1, names = void_names)
            void_data = void_data.append(void_data_run)

    # Saving data as csv files
    os.chdir(path + "\\" +dirName)
    if merge_stress is True:
        #stress_data.step_s = stress_data.step_s - stress_data.step_s.iloc[0] # reset step number
        stress_data.to_csv('stress_data.csv',index=False)
    if merge_energy is True:
        #energy_data.step_e = energy_data.step_e - energy_data.step_e.iloc[0] # reset step number
        energy_data.to_csv('energy_data.csv',index=False)
    if merge_coord is True:
        #coord_data.step_c = coord_data.step_c - coord_data.step_c.iloc[0] # reset step number
        coord_data.to_csv('coord_data.csv',index=False)
    if merge_void is True:
        #void_data.step_v = void_data.step_v - void_data.step_v.iloc[0] # reset step number
        void_data.to_csv('void_data.csv',index=False)
    print("ALL DONE")
