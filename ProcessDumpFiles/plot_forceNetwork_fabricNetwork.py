"""
Author: Tara Sassel
Date: 09/12/22

This sript creates a 3D reperesenation of the contact network 
"""
import os 
import numpy as np 
from numpy import linalg as LA
import pandas as pd 
import matplotlib as mpl
from matplotlib import cm
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
from matplotlib.lines import Line2D


from basicFunctions.get_fabric_tensor import get_fabric_tensor_cn
from basicFunctions.yimsiriSoga import  get_a_yimsiri_soga
# =============================================================================
dump_file_number = 0 # timestep of dumpfile
path = r'E:\Monotonic_Undrained\300kPa_60\Cycle50\run1'
folder_list = ['atom', 'connectivity', 'stress', 'velocity']

alpha1 = 0.35
LBF = 14
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

    # determining branch vector
    BV = np.sqrt(((X1-X2)**2)+((Y1-Y2)**2)+((Z1-Z2)**2)) # disk disk brach vechtor

    NormalForce = np.zeros((3,len(X1)))
    NormalForce[0,:] = contact_data_n0[3,:]*(X1-X2) # x component of normal force
    NormalForce[1,:] = contact_data_n0[3,:]*(Y1-Y2) # y component of normal force
    NormalForce[2,:] = contact_data_n0[3,:]*(Z1-Z2) # z component of normal force

    ResultantForce = np.zeros((4,len(X1)))
    ResultantForce[0,:] = NormalForce[0,:] + contact_data_n0[0,:] # x component of resultant force, i.e. sum of normal shear force
    ResultantForce[1,:] = NormalForce[1,:] + contact_data_n0[1,:] # x component of resultant force, i.e. sum of normal shear force
    ResultantForce[2,:] = NormalForce[2,:] + contact_data_n0[2,:] # x component of resultant force, i.e. sum of normal shear force

    ResultantForce[3,:] = np.sqrt(ResultantForce[0,:]*ResultantForce[0,:]+ResultantForce[1,:]*ResultantForce[1,:]+ResultantForce[2,:]*ResultantForce[2,:])

    # Unit vectors describing resultant force orientations
    F_nx = ResultantForce[0,:]/ResultantForce[3,:]
    F_ny = ResultantForce[1,:]/ResultantForce[3,:]
    F_nz = ResultantForce[2,:]/ResultantForce[3,:]


    return X1, Y1, Z1, X2, Y2, Z2, BV, F_nx, F_ny, F_nz

# ==============================================================================
# Get contact force 
X1, Y1, Z1, X2, Y2, Z2, BV, F_nx, F_ny, F_nz = get_RSF_NF(path, dump_file_number)
direction = np.zeros((len(X1),))

for i in range(len(X1)):
    # fabric tensor
    Ffabrictensor = np.zeros((3,3))
    Ffabrictensor[0,0] =  F_nx[i]*F_nx[i]
    Ffabrictensor[0,1] =  F_nx[i]*F_ny[i]
    Ffabrictensor[0,2] =  F_nx[i]*F_nz[i]

    Ffabrictensor[1,0] =  F_ny[i]*F_nx[i]
    Ffabrictensor[1,1] =  F_ny[i]*F_ny[i]
    Ffabrictensor[1,2] =  F_ny[i]*F_nz[i]

    Ffabrictensor[2,0] =  F_nz[i]*F_nx[i]
    Ffabrictensor[2,1] =  F_nz[i]*F_ny[i]
    Ffabrictensor[2,2] =  F_nz[i]*F_nz[i]

    w, v = LA.eig(Ffabrictensor)
    direction[i] = np.argmax(w) # find in what postion max index is

# Get slice
ymin = min(Y1)
ymax = max(Y1)
yl = ymax - ymin
maxBV = max(BV)

yrange1 = yl/2 - maxBV
yrange2 = yl/2 + maxBV

d = {"X1":X1, "Y1":Y1, "Z1":Z1, "X2":X2, "Y2":Y2, "Z2":Z2, "direction":direction }
df = pd.DataFrame(data = d)

df = df[(df.Y1 > yrange1) & (df.Y1 < yrange2)]

# sort values
df = df.sort_values(by='X1', ascending=False)
df = df.sort_values(by='Y1', ascending=False)
df = df.sort_values(by='Z1', ascending=False)

# top particles and bottom particles 

zmax = max(Z1)
ztop = zmax*0.99
zbottom = zmax*0.01


 
def find_continuous_link(particle_contacts)

df['toptag'] = np.where(df.Z1> ztop, True, False)

# only x direction:
df = df[df.direction == 0]
df_linked = df.copy()

df_toptag = df[df.toptag == True]
k_range = np.arange(1, len(df_toptag)+1)

for k, X_1 in enumerate(df_toptag.X1):
    df_linked.loc[df_linked.X2==X_1,'Match'] = k_range[k]    

X1, Y1, Z1, X2, Y2, Z2, direction, toptag, linked = df_linked.to_numpy().T

for i in range(len(X1)):
    if df_linked[i] == 1:
        c1 = 'orange'
    if df_linked[i] == 2:
        c1 = 'red'
    else: 
        x1 = "black"
    
    plt.plot([X1[i], X2[i]], [Z1[i], Z2[i]], c=c1) #transparancy_value[i]

plt.xlabel("x-axis [m]", fontsize = LBF)
plt.ylabel("z-axis [m]", fontsize = LBF)
plt.show()
