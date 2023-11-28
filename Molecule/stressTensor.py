# Author: Tara Sassel
# Date: 30/03/23

# This script is to check the stress tensor for the molecules

# Imports
import os 
import numpy as np 
import pandas as pd 

# Select Data
path = r'E:\Molecules\CyclicMolecule_6k\AR1p4_FC0p25_200_60\run1' # Path to contatc dump file 
number = 0 # Number of dump file 
os.chdir(path + r'\stress')

colnames = ['id', 'mol', 'stress_xx', 'stress_yy', 'stress_zz', 'stress_xy', 'stress_xz', 'stress_yz']

# Loading contact file
stress_data = pd.read_csv(
        f'dump{number}.stress',
        skiprows = 9,
        delimiter = ' ',
        index_col = False,
        header = None,
        names=colnames
    )

print(stress_data)

os.chdir(path + r'\contact')
colnames = ['fx', 'fy', 'fz', 'ccel', 'tag_1', 'tag_2', 'x1', 'y1', 'z1', 'r1', 'x2', 'y2', 'z2', 'r2']

# Loading contact file
contact_data = pd.read_csv(
        f'dump{number}.contact',
        skiprows = 9,
        delimiter = ' ',
        index_col = False,
        header = None,
        names=colnames
    )

print(contact_data)


def get_stress_tensor(contact_data: pd.DataFrame) -> np.array:
    """
    Fabric tensor for the resultant force orientation
        Input: pd.DataFrame of contact force dump file
        Output: fabric tensor in the resultant force orientation as np.array
    """
    # Idenitify contacts with non-zero force
    contact_data_n0 = contact_data[contact_data['ccel']>0]
    contact_data_n0  = contact_data_n0.to_numpy().T

    # DETRMINING CONTACT FORCE ----------------------------------------------------
    # 1. Distance between centroids (branch vector)
    X1 = contact_data_n0.x1
    Y1 = contact_data_n0.y1
    Z1 = contact_data_n0.z1
    R1 = contact_data_n0.r1

    X2 = contact_data_n0.x2
    Y2 = contact_data_n0.y2
    Z2 = contact_data_n0.z2
    R2 = contact_data_n0.r2

    NormalForce = np.zeros((3,len(X1)))
    NormalForce[0,:] = contact_data_n0.ccel*(X1-X2) # x component of normal force
    NormalForce[1,:] = contact_data_n0.ccel*(Y1-Y2) # y component of normal force
    NormalForce[2,:] = contact_data_n0.ccel*(Z1-Z2) # z component of normal force

    FT = np.zeros((3,len(X1)))
    FT[0,:] = NormalForce[0,:] + contact_data_n0.fx # x component of resultant force, i.e. sum of normal shear force
    FT[1,:] = NormalForce[1,:] + contact_data_n0.fy # y component of resultant force, i.e. sum of normal shear force
    FT[2,:] = NormalForce[2,:] + contact_data_n0.fz # z component of resultant force, i.e. sum of normal shear force


    stress_tensor = NormalForce



