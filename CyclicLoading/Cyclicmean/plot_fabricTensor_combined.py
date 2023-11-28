"""
Author: Tara Sassel
Date: 30/11/2022
In this script the fabric tensor is for the loaded and unloaded position
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from matplotlib.lines import Line2D

# Definig Plot Fontsizes
TF = 24     # Text font
LGF = 16   # Legend Font Size
LBF = 16    # Label Font Size
TS = 12     # Tick Size
lw1 = 3     # Line Width

pos_list = ['0_StartingPos', '2_NeutralPos']
ls_list = [':','--']
color_list = ["forestgreen", "cornflowerblue"]
label_list = ["Position 0", "Position 2"]

for i, pos in enumerate(pos_list):
        path = r'E:\CyclicLoading\Cyclicmean\TX300_FC0p25to0p25_amp90\merged_data\SortedData' + r'\\' + pos
        os.chdir(path)

        fabric_tensor = pd.read_csv("fabric_tensor.csv")
        fabric_tensor_xyz = pd.read_csv("fabric_tensor_xyz.csv")
        print(fabric_tensor.head())

        # Calculating deviatoric fabric
        ft1 =  fabric_tensor.ft1.to_numpy().T
        ft3 =  fabric_tensor.ft3.to_numpy().T

        ftxx = fabric_tensor_xyz.ftxx.to_numpy().T
        ftyy = fabric_tensor_xyz.ftxx.to_numpy().T
        ftzz = fabric_tensor_xyz.ftxx.to_numpy().T

        ftq = ft1 - ft3

        fabric_tensor["q"] = (0.5*((fabric_tensor.ft1-fabric_tensor.ft1)**2))**(0.5)

        plt.figure(1, figsize = (7,7))
        plt.plot(fabric_tensor_xyz.ftxx, marker = 'v',markevery = 5, mec = 'black', ls = ":", color = color_list[i], lw = lw1,label = '$F_{11}$')
        plt.plot(fabric_tensor_xyz.ftyy, marker = 'o',markevery = 5, mec = 'black', ls = "--", color = color_list[i], lw = lw1,label = '$F_{22}$')
        plt.plot(fabric_tensor_xyz.ftzz, marker = '^',markevery = 5, mec = 'black', ls = "-", color = color_list[i], lw = lw1,label = '$F_{33}$')

        plt.figure(2, figsize = (7,7))
        plt.plot(ftq, marker = 's', mec = 'black', ls = "-", color = color_list[i], lw = lw1,label = label_list[i])

plt.figure(1, figsize = (7,7))
# legend
custom_lines1 = [Line2D([0], [0], color = "gray", lw=2, ls = ':',marker = 'v', mec = 'black'),
                Line2D([0], [0], color = "gray", lw=2, ls = '--',marker = 'o', mec = 'black'),
                Line2D([0], [0], color = "gray", lw=2, ls = '-',marker = '^', mec = 'black')]
custom_lines2 = [Line2D([0], [0], lw=8, color = color_list[0]),
                Line2D([0], [0], lw=8, color = color_list[1])]

lg1 = plt.gca().legend(custom_lines1, ['$F_{xx}$', '$F_{yy}$', '$F_{zz}$'], loc = 'lower right', fontsize = LGF)
lg2 = plt.gca().legend(custom_lines2, ['Position 0', 'Position 2'], loc = 'upper right', fontsize = LGF)
plt.gca().add_artist(lg1)
plt.xlabel('Cycle Number', fontsize = LBF)
plt.ylabel('Princical Fabric', fontsize = LBF)
plt.gca().yaxis.set_major_formatter(mtick.FormatStrFormatter('%.3f'))
plt.gca().tick_params(which = 'major', labelsize = TS)
plt.xlim(-1,50)
plt.grid()
plt.tight_layout()

plt.figure(2, figsize = (7,7))
plt.legend(loc='upper right', fontsize = LGF)
plt.xlabel('Cycle Number', fontsize = LBF)
plt.ylabel('Deviatoric Fabric ($F_d$)', fontsize = LBF)
plt.gca().yaxis.set_major_formatter(mtick.FormatStrFormatter('%.3f'))
plt.gca().tick_params(which = 'major', labelsize = TS)
plt.xlim(-1,50)
plt.grid()
plt.tight_layout()
plt.show()
