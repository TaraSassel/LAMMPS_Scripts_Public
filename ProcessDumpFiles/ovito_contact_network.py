"""
Author: Tara Sassel
Date: 09/12/2022

This script creates a dump file for the contact force network in Ovito
"""

# Imports
import os
import fnmatch
import pandas as pd
import numpy as np

from basicFunctions.get_combinedDump import get_combinedDump

# =============================================================================
dump_file_number = 0 # timestep of dumpfile
path = r'D:\CyclicLoading\Cyclicmean\TX300_FC0p25to0p25_amp90\merged_data\SortedData\0_StartingPos'
folder_list = ['atom', 'connectivity', 'stress', 'velocity']


# ==============================================================================
def get_RSF_NF(path: str, dump_file_number: int) -> np.array:
    """
    Calcualting resultant shear force / normal force
    """

    # Loading dump file
    folder = r'\contact'
    os.chdir(path + folder)
    contact_data = pd.read_csv(
        "dump0.contact",
        skiprows = 9,
        header = None,
        delimiter = ' ',
        index_col=False)

    # Non zero contacts
    contact_data_n0 = contact_data[contact_data[3]>0]
    contact_data_n0 = contact_data_n0.to_numpy().T

    FC = 0.25 # Friction coefficent

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
    NF = contact_data_n0[3,:]*BV

    # Resulatnt shear force
    RSF = np.sqrt(tfx**2+tfy**2+tfz**2)

    return X1, Y1, Z1, X2, Y2, Z2, NF, RSF, BV
    
# ==============================================================================
# Get contact force 
X1, Y1, Z1, X2, Y2, Z2, NF, RSF, BV = get_RSF_NF(path, dump_file_number)

# Getting Custom Dump data
combined_dump = get_combinedDump(path, folder_list,dump_file_number)

id = combined_dump.id.to_numpy().T
x = combined_dump.x.to_numpy().T
y = combined_dump.y.to_numpy().T
z = combined_dump.z.to_numpy().T

ovito_contact_data = np.zeros((len(X1), 5))
ovito_contact_data[:,2] = NF
ovito_contact_data[:,3] = RSF
ovito_contact_data[:,4] = BV

def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3

# get identifier 1
for i, X in enumerate(X1):
    Y = Y1[i]
    lst1 = list(np.where(X == x))
    lst2 = list(np.where(Y == y))
    try :
        lst3 = intersection(lst1,lst2)
        ovito_contact_data[i,0] = lst3[0][0]
    except:
        pass
    

# get identifier 2
for j, X in enumerate(X2):
    Z = Z2[j]
    lst1 = list(np.where(X == x))
    lst2 = list(np.where(Z == z))
    try :
        lst3 = intersection(lst1,lst2)
        ovito_contact_data[j,1] = lst3[0][0]
    except:
        pass

# Deleting data if id is 0:
ovito_df = pd.DataFrame(ovito_contact_data, columns = ['id1','id2','ContactNormalForce','ResultantShearForce','BrancheVector'])
ovito_df = ovito_df[ovito_df.id1 != 0]
ovito_df = ovito_df[ovito_df.id2 != 0]

os.chdir(path + r"/atom")
# Creating header 
with open(f'dump{dump_file_number}.atom') as myfile:
    hearder_section = [next(myfile) for x in range(8)]
hearder_section = ''.join(hearder_section)

line1 = ' id1 id1 ContactNormalForce ResultantShearForce BrancheVector'
line1 = "ITEM: ATOMS " + line1 + "\n"
hearder_section = hearder_section + line1


# ------------------------------------------------------------------------------
# Creating Directory to store dump files
directory_name = 'ovito_dump'
os.chdir(path)
try:
    os.mkdir(directory_name)
except FileExistsError:
    print("Directory " ,directory_name,  " already exists")
os.chdir(path + '\\' + directory_name)

# ------------------------------------------------------------------------------
# Creating file containg custom data
ovito_df.to_csv("data.txt", sep=' ', index=False, header=False)

# Creating text file containg header section
try :
    os.remove("header.txt")
except FileNotFoundError:
    pass

file_object = open("header.txt","a")
file_object.seek(0)
file_object.write(hearder_section)
file_object.close()

filenames = ['header.txt', 'data.txt']
with open(f'dump{dump_file_number}.contact', 'w') as outfile:
    for fname in filenames:
        with open(fname) as infile:
            for line in infile:
                outfile.write(line)

os.remove("header.txt")
os.remove("data.txt")