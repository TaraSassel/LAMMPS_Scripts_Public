"""
Author: Tara Sassel
Date: 16/11/2022

This script calculates the values required for G0
G0 is defined in Liu Thesis and in a paper of his.
"""
# Imports
from basicFunctions.get_mechVoidRatio import get_mechVoidRatio
from basicFunctions.get_mechCoord import get_mechCoord

# Defining
path = r"G:\PhD_Data_Back_Up\LAMMPS\CyclicLoading\ConstantP\TX300_FC0p25to0p25_amp60\run1"
dump_file_number = 0
p_dash = 100 #kPa

# Getting mechanical void ratio and coodrination number
e_mech = get_mechVoidRatio(path,dump_file_number)
mech_coord = get_mechCoord(path,dump_file_number)

print(e_mech)
print(mech_coord)

# Calculating G0
ratio = mech_coord/(1+e_mech)
print(ratio)

R2 = 0.93 # Distance from Linar Regression line
n = 0.33
A = 59.61
c = 1.653

G = A*((c-e_mech)**2/(1+e_mech))*101.32**(1-n)*p_dash**n

print(G)
