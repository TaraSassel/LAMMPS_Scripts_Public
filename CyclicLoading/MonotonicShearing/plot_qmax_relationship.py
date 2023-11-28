"""
Author:Tara Sassel
Date: 11/01/2023

Draft script
Idea to find a realationship to get qmax
"""


import os
import numpy as np 
import pandas as pd
import seaborn as sns 
import matplotlib.pyplot as plt 
from sklearn import linear_model 

# Define Plot Fontsizes
TF = 24     # Text font
LGF = 7   # Legend Font Size
LBF = 12    # Label Font Size
TS = 10     # Tick Size
lw1 = 2     # Line Width


os.chdir(r'E:\Monotonic_Undrained')
color_list = ['#f0f9e8', '#7bccc4', '#43a2ca', '#0868ac']
label_list = [
    '$q^{peak}$ = 15kPa Position 0',
    '$q^{peak}$ = 30kPa Position 0',
    '$q^{peak}$ = 60kPa Position 0',
    '$q^{peak}$ = 90kPa Position 0'
    ]

a_df = pd.read_csv('a_values300.csv')
mechCoord_df = pd.read_csv('mechCoord_values300.csv')

amplitudes = [15, 30, 60, 90]

for i, amp in enumerate(amplitudes):
    qmax_df = pd.read_csv(rf'qmax_e_{amp}.csv')
    qmax_values = qmax_df.qmax.to_numpy().T/1000
    void_values = qmax_df.void_ratio.to_numpy().T
    a_values = a_df[rf'a_{amp}_P0'].to_numpy().T
    mechCoord_values = mechCoord_df[rf'mechCoord_{amp}_P0'].to_numpy().T

    X = pd.DataFrame({'coord': mechCoord_values, 'a': a_values,'e':void_values})
    print(X)
    y = pd.DataFrame({'qmax':qmax_values})
    regr = linear_model.LinearRegression()
    regr.fit(X, y) 
    print(regr.coef_) 
    #Spredictedqmax =  regr.predict([np.arange(0,120)]) 

    plt.plot(a_values*mechCoord_values,qmax_values, c = color_list[i], label = label_list[i])

plt.legend(loc = 'upper right', fontsize = LGF)
plt.xlabel(r"$a \times \bar{C^*_N}$", fontsize = LBF)
plt.ylabel("Maximum deviatoric stress ($q^{max}$) [kPa]", fontsize = LBF)
plt.gca().tick_params(which = "both", labelsize = TS)
plt.grid()
plt.tight_layout()

plt.show()
plt.show()