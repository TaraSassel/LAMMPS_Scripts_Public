# Tara Sassel
# 16/06/2023

# This script is to compare the original and the modified void ratio 

# Imports 
import os 
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)

# Fonts 
LBF = 16
LGF = 16
TS = 12
xlim = 1.6*10e7

# Changing path 
path = r'E:\Molecules\ISOCOMP_6kSample\AR1p1_ISO200_FC0p25'
os.chdir(path)

# Loading data 
void_names = ['step_v', 'void_ratio']
void_data = pd.read_csv('voidratio.txt', index_col=None, delimiter = ' ', skiprows = 1, names = void_names)
void_data_mod = pd.read_csv('voidratio_mod.txt', index_col=None, delimiter = ' ', skiprows = 1, names = void_names)

# plot
plt.figure(figsize=(10,5))
plt.plot(void_data.step_v, void_data.void_ratio, c = 'maroon', label = r'Original void ratio ($e$)', lw = 2)
plt.plot(void_data_mod.step_v, void_data_mod.void_ratio, c = 'darkgreen', label = r'Modified void ratio ($e_{mod}$)', lw = 2)

plt.text(xlim-0.1*10e7, 0.0, f'{void_data.void_ratio[xlim/1000]:.2f}', c = 'maroon')
plt.text(xlim-0.1*10e7, 0.7, f'{void_data_mod.void_ratio[xlim/1000]:.2f}', c = 'forestgreen')

plt.ylabel(r'Void ratio', fontsize = LBF)
plt.xlabel('Timestep', fontsize = LBF)
plt.legend(loc = 'upper right', fontsize = LGF)

plt.gca().tick_params(axis='both', which='major', labelsize=TS)
plt.gca().yaxis.set_major_locator(MultipleLocator(1))
plt.gca().yaxis.set_minor_locator(MultipleLocator(0.2))
plt.grid(ls = '--', color = 'gray')
plt.xlim(0,xlim)
plt.show()