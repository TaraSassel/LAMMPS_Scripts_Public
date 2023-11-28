"""
Author: Tara Sassel 
Date: 15/02/2023

"""
import re
import os 
import numpy as np 
import pandas as pd 
import seaborn as sns
from tqdm import tqdm
import matplotlib.pyplot as plt 
from matplotlib.lines import Line2D
import matplotlib.patches as mpatches
from sympy import symbols, Eq, solve

from basicFunctions.yimsiriSoga import  get_a_yimsiri_soga

import warnings
warnings.filterwarnings('ignore')
# ==============================================================================
# FIGURE
# Define Plot Fontsizes
TF = 24     # Text font
LGF = 15   # Legend Font Size
LBF = 18    # Label Font Size
TS = 14     # Tick Size
lw1 = 3


position = 1
pos_list = ['0_StartingPos', '1_LoadedPos', '2_NeutralPos', '3_UnloadedPos']
wanted_pos_list = [pos_list[position]]

print(wanted_pos_list)
for k, pos_folder in enumerate(wanted_pos_list):
    # Defining Path
    drive = "E"
    path_300_15 = rf'{drive}:\CyclicLoading\Cyclicmean\TX300_FC0p25to0p25_amp15\merged_data\SortedData\{pos_folder}\contact'
    path_300_20 = rf'{drive}:\CyclicLoading\Cyclicmean\TX300_FC0p25to0p25_amp20\merged_data\SortedData\{pos_folder}\contact'
    path_300_30 = rf'{drive}:\CyclicLoading\Cyclicmean\TX300_FC0p25to0p25_amp30\merged_data\SortedData\{pos_folder}\contact'
    path_300_60 = rf'{drive}:\CyclicLoading\Cyclicmean\TX300_FC0p25to0p25_amp60\merged_data\SortedData\{pos_folder}\contact'
    path_300_90 = rf'{drive}:\CyclicLoading\Cyclicmean\TX300_FC0p25to0p25_amp90\merged_data\SortedData\{pos_folder}\contact'

    path_list = [path_300_90]
    label_list = ["Whole contact network", "Weak contact network", "Strong contact network"]
    color_list = ['cornflowerblue', "darkorange","indianred", "forestgreen"]

    # ==============================================================================
    # ==============================================================================
    # Function 
    def get_vectors_describing_cno(contact_data: pd.DataFrame) -> np.array:
        """
        Function for contact normal orientations 
            Input: pd.DataFrame of contact force dump file
            Output: N_nx, N_ny, N_nz
        """
        # Idenitify contacts with non-zero force
        contact_data_n0 = contact_data[contact_data[3]>0]
        contact_data_n0  = contact_data_n0.to_numpy().T

        # DETRMINING CONTACT FORCE ----------------------------------------------------
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

        # unit vectors describing contact normal orientation
        N_nx = (X1-X2)/BV
        N_ny = (Y1-Y2)/BV
        N_nz = (Z1-Z2)/BV

        # Normal Force
        NF = contact_data_n0[3,:]*BV

        return  N_nx, N_ny, N_nz, NF

    # Get FT
    def get_FT(N_nx: np.array, N_ny: np.array, N_nz: np.array) -> np.array:
        """
        Function to calculate Fabric tensor 
        """
        CNfabrictensor = np.zeros((3,3))

        CNfabrictensor[0,0] =   np.sum(N_nx*N_nx)
        CNfabrictensor[0,1] =   np.sum(N_nx*N_ny)
        CNfabrictensor[0,2] =   np.sum(N_nx*N_nz)

        CNfabrictensor[1,0] =   np.sum(N_ny*N_nx)
        CNfabrictensor[1,1] =   np.sum(N_ny*N_ny)
        CNfabrictensor[1,2] =   np.sum(N_ny*N_nz)

        CNfabrictensor[2,0] =   np.sum(N_nz*N_nx)
        CNfabrictensor[2,1] =   np.sum(N_nz*N_ny)
        CNfabrictensor[2,2] =   np.sum(N_nz*N_nz)

        CNfabrictensor[:,:] = np.nan_to_num(CNfabrictensor[:,:]/len(N_nx))

        return CNfabrictensor

    # Function for "a"
    def get_a(CNfabrictensor: np.array) -> float:
        """
        Function to calculate the degree of anisotropy 
        as in Yimsiri and Soga (2010)
        """
        a1 = symbols('a1')
        a2 = symbols('a2')
        a3 = symbols('a3')
        eq1 = Eq((3*a1-5)/(5*(a1-3))-CNfabrictensor[0,0])
        eq2 = Eq((3*a2-5)/(5*(a2-3))-CNfabrictensor[1,1])
        eq3 = Eq((-(5+a3))/(5*(a3-3))-CNfabrictensor[2,2])

        # Solving equations for a
        a_val1 = solve(eq1)[0]
        a_val2 = solve(eq2)[0]
        a_val3 = solve(eq3)[0]

        # Getting average value of a
        a = (a_val1 + a_val2 + a_val3)/3
        return a 
    # ==============================================================================
    # ==============================================================================

    for p, path in enumerate(path_list): 
        # Loading dump file
        folder = r'\contact'
        os.chdir(path)

        # Getting Contact Dump Files
        contact_files = os.listdir()

        step_number = []
        print(contact_files)
        for contact_file in contact_files:
            step_number.append(re.findall('\d+', contact_file))

        print(contact_files)
        step_number = [int(step[0]) for step in step_number] # Convert string to integer

        yimsiri_soga_a_value = pd.DataFrame(data = {'file_name':contact_files, 'step_number':step_number})
        yimsiri_soga_a_value = yimsiri_soga_a_value.sort_values(by = ['step_number'], ascending = True)

        # Initiating lists
        a_whole = []    # 'a' for the whole system 
        a_weak = []     # 'a' for the weak system 
        a_strong = []   # 'a' for the strong system 

        len_whole = []    # number of contacts for the whole system 
        len_weak = []     # number of contacts for the weak system 
        len_strong = []   # number of contacts for the strong system 

        # Iterating trough dump files
        for contact_file in tqdm(yimsiri_soga_a_value.file_name):

            contact_data = pd.read_csv(
                contact_file,
                skiprows = 9,
                header = None,
                delimiter = ' ',
                index_col=False)

            # Calculating CN Orientation
            N_nx, N_ny, N_nz, NF =  get_vectors_describing_cno(contact_data)
            d = {"N_nx": N_nx, "N_ny": N_ny, "N_nz": N_nz, "NF": NF}
            df = pd.DataFrame(data = d)

            # Devide into strong and weak 
            df['Network'] = np.where(df['NF'] < np.mean(df['NF']), "Weak", "Strong")
            df_weak = df[df["Network"] == "Weak"]
            df_strong = df[df["Network"] == "Strong"]

            # Number of contacts in each network
            len_whole.append(len(df))
            len_weak.append(len(df_weak))
            len_strong.append(len(df_strong))

            # Printing for checks 
            #print("Whole:" + str(len(df)))
            #print(np.mean(df.NF))
            #print("Weak:" + str(len(df_weak)))
            #print(np.mean(df_weak.NF))
            #print("Strong:" + str(len(df_strong)))
            #print(np.mean(df_strong.NF))

            # Geting CN Orientation for weak and strong network 
            N_nx_weak = df_weak["N_nx"].to_numpy()
            N_ny_weak = df_weak["N_ny"].to_numpy()
            N_nz_weak = df_weak["N_nz"].to_numpy()

            N_nx_strong = df_strong["N_nx"].to_numpy()
            N_ny_strong = df_strong["N_ny"].to_numpy()
            N_nz_strong = df_strong["N_nz"].to_numpy()


            CNfabrictensor = get_FT(N_nx, N_ny, N_nz)                               # Here inputs from line 166 that is the whole dataframe
            CNfabrictensor_weak = get_FT(N_nx_weak, N_ny_weak, N_nz_weak)           # The weak dataframe 
            CNfabrictensor_strong = get_FT(N_nx_strong, N_ny_strong, N_nz_strong)   # The strong dataframe 
        

            a_whole.append(get_a(CNfabrictensor))
            a_weak.append(get_a(CNfabrictensor_weak))
            a_strong.append(get_a(CNfabrictensor_strong))



        yimsiri_soga_a_value['a_whole'] = a_whole
        yimsiri_soga_a_value['a_weak'] = a_weak 
        yimsiri_soga_a_value['a_strong'] = a_strong
    
        yimsiri_soga_a_value['size_whole'] = len_whole
        yimsiri_soga_a_value['size_weak'] = len_weak 
        yimsiri_soga_a_value['size_strong'] = len_strong

        yimsiri_soga_a_value['strong_percentage'] = [strong*100/whole for strong, whole in zip(len_strong,len_whole)]

        # FIGURE =======================================================================
        plt.figure(1, figsize = (10,7))
        cycle_n = np.arange(0,len(yimsiri_soga_a_value.a_whole),1)

        plt.plot(cycle_n, yimsiri_soga_a_value.a_whole, color = color_list[position], ls = '-', lw = 3, marker = 'o', mec = 'black',mfc=color_list[position], ms =10, markevery =5)
        plt.plot(cycle_n, yimsiri_soga_a_value.a_weak, color = color_list[position], ls = ':', lw = 3, marker = 'v', mec = 'black',mfc=color_list[position], ms = 10, markevery =5)
        plt.plot(cycle_n, yimsiri_soga_a_value.a_strong, color = color_list[position], ls = '--', lw = 3, marker = '^', mec = 'black',mfc=color_list[position], ms = 10, markevery =5)

# Legend 
labels_1 = ['Whole network', 'Strong network', 'Weak network']
custom_lines1 = [Line2D([0], [0], color = color_list[position], lw=2, ls = '-',marker = 'o', mec = 'black', ms = 10),
                Line2D([0], [0], color = color_list[position], lw=2, ls = '--',marker = '^', mec = 'black', ms = 10),
                Line2D([0], [0], color = color_list[position], lw=2, ls = ':',marker = 'v', mec = 'black', ms = 10)]

labels_2 = ['Position 0', 'Position 2']
patch1 = mpatches.Patch(color= color_list[position], label= labels_2[0])
patch2 = mpatches.Patch(color= color_list[position], label= labels_2[1])

ax = plt.gca()
lg1 = ax.legend(custom_lines1,['Whole network', 'Strong network', 'Weak network'],  loc = 'lower right', fontsize = LGF) # bbox_to_anchor=(1, 0.2)
#lg2 = ax.legend(handles=[patch1, patch2], loc = 'upper right', fontsize = LGF)
ax.add_artist(lg1)

#plt.ylim(-0.15, 0.1)
plt.ylim(-0.5, 0.3)
plt.xlabel('Cycle number (N)', fontsize = LBF)
plt.ylabel('Degree of anisotropy (a)', fontsize = LBF)
plt.gca().tick_params(which='major', labelsize=TS)
plt.xlim(0,50)
plt.grid()


# Adding figure for percentage of strong contacts
#plt.figure(2, figsize = (10,7))
#ax = plt.bar(cycle_n, yimsiri_soga_a_value.strong_percentage)

print(yimsiri_soga_a_value.head(51))
plt.show()


