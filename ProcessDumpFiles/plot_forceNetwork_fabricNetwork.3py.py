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
from matplotlib.lines import Line2D
from typing import List, Tuple
from tqdm import tqdm
from heapq import heappush, heappop


from basicFunctions.get_fabric_tensor import get_fabric_tensor_cn
from basicFunctions.yimsiriSoga import  get_a_yimsiri_soga
# =============================================================================
dump_file_number = 0 # timestep of dumpfile
path = r'E:\Monotonic_Undrained\300kPa_60\Cycle50\run1'
folder_list = ['atom', 'connectivity', 'stress', 'velocity']

alpha1 = 0.35
LBF = 14
# ==============================================================================

# Identify top and bottom spheres 
# Loading dump file
folder = r'\atom'
os.chdir(path + folder)
col_names = ["id", "type", "x", "y", "z"]
atom_data = pd.read_csv(
    "dump0.atom",
    skiprows = 9,
    header = None,
    delimiter = ' ',
    index_col=False,
    names=col_names)

id = atom_data.id.to_numpy().T
x = atom_data.x.to_numpy().T
y = atom_data.y.to_numpy().T
z = atom_data.z.to_numpy().T

zmax = max(z)
ztop = zmax-0.0001
top_index = np.argwhere(z > ztop)
bottom_index = np.argwhere(z < 0.0001)

dt = {"id": np.concatenate(id[top_index]), "x": np.concatenate(x[top_index]), "y": np.concatenate(y[top_index]), "z ":  np.concatenate(z[top_index])}
top_particles = pd.DataFrame(data = dt)
db =  {"id": np.concatenate(id[bottom_index]), "x": np.concatenate(x[bottom_index]), "y": np.concatenate(y[bottom_index]), "z ":  np.concatenate(z[bottom_index])}
bottom_particles = pd.DataFrame(data = db)

top_particle_id_list = list(top_particles.id)
bottom_particle_id_list = list(bottom_particles.id)

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
        
    # Normal Force
    NF = contact_data_n0[3,:]*BV


    return X1, Y1, Z1, X2, Y2, Z2, BV, F_nx, F_ny, F_nz, NF 

# ==============================================================================
# Get contact force 
X1, Y1, Z1, X2, Y2, Z2, BV, F_nx, F_ny, F_nz, NF = get_RSF_NF(path, dump_file_number)
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


d = {"X1":X1, "Y1":Y1, "Z1":Z1, "X2":X2, "Y2":Y2, "Z2":Z2, "direction":direction, "NF": NF }
contact_df = pd.DataFrame(data = d)
print(len(contact_df))
# Adding ids
for i in range(len(atom_data)):
    id = atom_data.id[i]
    x = atom_data.x[i]
    y = atom_data.y[i]
    z = atom_data.z[i]
    contact_df.loc[(contact_df.X1.round(4) == x.round(4)) & (contact_df.Z1.round(4) == z.round(4)),'id_A'] = id
    contact_df.loc[(contact_df.X2.round(4) == x.round(4)) & (contact_df.Z2.round(4) == z.round(4)),'id_B'] = id

# ==========================================================================================================================
# Figure
NF_max = max(NF)
NF_min = min(NF)

NF_mean = np.mean(NF)


# Get slice
zmin = min(X1)
zmax = max(X1)
zl = zmax - zmin
maxBV = max(BV)

zrange1 = zl/2 - maxBV
zrange2 = zl/2 + maxBV

df = contact_df[(contact_df.X1 > zrange1) & (contact_df.X1 < zrange2)]
X1, Y1, Z1, X2, Y2, Z2, direction, NF, id_A, id_B =contact_df.to_numpy().T
print("Number of contacts in section")
print(len(NF))
print(len(id_A))

normalized_NF = np.zeros((len(NF),))
transparancy_value2 = np.zeros((len(NF),))
counter = 0 
for i, NF_value in enumerate(NF):
    if NF_value < NF_mean:
        transparancy_value2[i] = alpha1
        normalized_NF[i] = (NF_value - NF_mean)/(NF_mean - NF_min)
    else: 
        normalized_NF[i] = (NF_value - NF_mean)/(NF_max - NF_mean)
        transparancy_value2[i] = 1
        counter += 1
# Define transparancy range
transparancy_value =  (NF - NF_min)/(NF_max - NF_min)
print("Number of strong contacts in section")
print(counter)
# map range
norm = mpl.colors.LogNorm(vmin=NF_min, vmax=NF_max)
norm = mpl.colors.Normalize(vmin=NF_min, vmax=NF_max)

# Figure 
fig, ax = plt.subplots(1, 1, figsize = (7,7))
# Hide the right and top spines
ax.spines[['right', 'top']].set_visible(False)

for i in range(len(X1)):
    if NF[i] > NF_mean:
        c1 = 'maroon'
    else:
        c1 = 'forestgreen'
    plt.plot([Z1[i], Z2[i]], [Y1[i], Y2[i]], alpha = transparancy_value2[i], c=c1, lw = 2) #transparancy_value[i]

plt.xlabel("z-axis [m]", fontsize = LBF)
plt.ylabel("y-axis [m]", fontsize = LBF)

custom_lines = [Line2D([0], [0], color="forestgreen", lw=4, alpha = alpha1),
                Line2D([0], [0], color="maroon", lw=4)]

ax.legend(custom_lines, [f'$F_N$ < {NF_mean:.3g} [N]', f'$F_N \leqq$  {NF_mean:.3g} [N]'], loc = 'lower left')               

# ==========================================================================================================================

# Zipping two list to put IDs togeter 
def zip_lists(list1, list2):
    # Check that the two lists have the same length
    if len(list1) != len(list2):
        raise ValueError("Lists must be of equal length.")

    # Use the zip() function to create a list of tuples
    zipped_list = list(zip(list1, list2))

    # Return the zipped list
    return zipped_list

contact_pairs = zip_lists(id_A, id_B)
z_coords = zip_lists(Z1, Z2)
y_coords = zip_lists(Y1, Y2)



def find_strongest_paths(links, forces, top_ids, bottom_ids, z_coords):
    # Create a dictionary to store the force of each link
    link_forces = dict(zip(links, forces))
    
    # Sort the links by force in descending order
    sorted_links = sorted(links, key=lambda link: link_forces[link], reverse=True)
    
    # Initialize a set to keep track of the visited contacts
    visited = set()
    
    # Initialize a list to store the paths
    paths = []
    
    # Iterate over the sorted links, starting with the top contact with the largest force
    for link in tqdm(sorted_links):
        if link[0] in top_ids and link[1] not in visited:
            visited.add(link[0])
            visited.add(link[1])
            path = [link[0], link[1]]
            curr_id = link[1]
            
            # Follow the link in the z direction to the next contact
            while curr_id not in bottom_ids:
                next_links = [(l, f) for l, f in zip(links, forces) if l[0] == curr_id and l[1] not in visited and z_coords[l[1]] > z_coords[curr_id]]
                if not next_links:
                    break
                next_link = max(next_links, key=lambda l_f: l_f[1])
                visited.add(next_link[0][1])
                path.append(next_link[0][1])
                curr_id = next_link[0][1]
            
            # If the path reaches a bottom contact, add it to the list of paths
            if curr_id in bottom_ids:
                paths.append(path)
            
            # If all bottom contacts have been reached, return the paths
            if set(bottom_ids).issubset(visited):
                return paths
    
    # If no path reaches all bottom contacts, return None
    return None




link_list = find_strongest_paths(contact_pairs, NF, top_particle_id_list, bottom_particle_id_list, z_coords)

for link in link_list:
    print(link)
    link_df = contact_df["Z1", "Y1"][contact_df['id_A'].isin(link)].drop_duplicates()
    plt.plot(Z1, Y1, c = 'black', lw = 1)

plt.show()