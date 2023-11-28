"""
Author: Tara Sassel
Date: 26/10/2022

Recreating Wichtmann et al. 2007 Figure 3 with my data
Note: Slighly messy script
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

from basicFunctions.get_strain import get_strain
from basicFunctions.get_cyclicmean_data import get_cyclicmean_data
# ==============================================================================
which_data = 'pav300_V2'
drive = 'F'
path_list, color_list =  get_cyclicmean_data(which_data, drive)

# Defining xticks
x_ticks = [15, 20, 30, 60, 90]
x_lim = 100
# ==============================================================================
# Define Plot Fontsizes
TF = 24     # Text font
LGF = 12   # Legend Font Size
LBF = 15    # Label Font Size
TS = 12     # Tick Size
lw1 = 2     # Line Width
# ==============================================================================
# Calculating cycle length
time_step = 5.242309e-09
period = 0.25
cycle_length = int(period/(time_step))

wanted_cycles = np.array([50]).astype(float)
wanted_stepsL = [cycle*cycle_length + cycle_length/4 for cycle in wanted_cycles]
wanted_stepsU = [cycle*cycle_length + 3*cycle_length/4 for cycle in wanted_cycles]
# ==============================================================================
def epsqv(xstrain_val, ystrain_val, zstrain_val):
    # In this version I took eps out and put eps_zz instead and no gamma
    eps_q = (2/3)*(zstrain_val - 0.5*(xstrain_val + ystrain_val))
    eps_v = (xstrain_val + ystrain_val + zstrain_val)
    gamma = (zstrain_val - 0.5*(xstrain_val + ystrain_val))
    eps = zstrain_val
    return eps_v, eps_q, gamma, eps

# define the true objective function
def objective(x, a, b, c):
	return a * x + b * x**2 + c
# ==============================================================================
eps_z_all = [0]
eps_v_all = [0]
eps_q_all = [0]

for p, path in enumerate(path_list):
    os.chdir(path)
    strain_data = pd.read_csv('stress_data.csv')

    step_s = strain_data.step_s.to_numpy().T
    length_x = strain_data.length_x.to_numpy().T
    length_y = strain_data.length_y.to_numpy().T
    length_z = strain_data.length_z.to_numpy().T
    xstrain = get_strain(length_x)
    ystrain = get_strain(length_y)
    zstrain = get_strain(length_z)

    eps_v, eps_q, gamma, eps_z = epsqv(xstrain, ystrain, zstrain)
    eps_values = [eps_z, eps_v, eps_q]

    # Getting index of minima and maxima
    wanted_indexL = []
    for step in wanted_stepsL:
        wanted_indexL.append(np.argmax(step_s>=step))
    wanted_indexU = []
    for step in wanted_stepsU:
        wanted_indexU.append(np.argmax(step_s>=step))

    #for eps in eps_values:
    # Getting strains at Maxima and Minima
    wanted_strainL = zstrain[wanted_indexL]
    wanted_stepsL = step_s[wanted_indexL]
    wanted_strainU = zstrain[wanted_indexU]
    wanted_stepsU = step_s[wanted_indexU]

    wanted_eps_vL = eps_v[wanted_indexL]
    wanted_stepsL = step_s[wanted_indexL]
    wanted_eps_vU = eps_v[wanted_indexU]
    wanted_stepsU = step_s[wanted_indexU]

    wanted_eps_qL = eps_q[wanted_indexL]
    wanted_stepsL = step_s[wanted_indexL]
    wanted_eps_qU = eps_q[wanted_indexU]
    wanted_stepsU = step_s[wanted_indexU]

    # Calculating amplitude
    eps_z_amp = np.abs(wanted_strainL-wanted_strainU)
    eps_v_amp = np.abs(wanted_eps_vL-wanted_eps_vU)
    eps_q_amp = np.abs(wanted_eps_qL-wanted_eps_qU)

    # Appending to list for curve fitting
    eps_z_all = np.append(eps_z_all, (eps_z_amp/100)*1000)
    eps_v_all = np.append(eps_v_all, (eps_v_amp/100)*1000)
    eps_q_all = np.append(eps_q_all, (eps_q_amp/100)*1000)

    # Adding to figure
    plt.figure(1)
    plt.plot(
        x_ticks[p],
        (eps_z_amp/100)*1000,
        marker = 'o',
        mec = 'k',
        color = color_list[p],
        zorder = 3)
    plt.plot(
        x_ticks[p],
        (eps_v_amp/100)*1000,
        marker = 's',
        mec = 'k',
        color = color_list[p],
        zorder = 3)
    plt.plot(
        x_ticks[p],
        (eps_q_amp/100)*1000,
        marker = 'v',
        mec = 'k',
        color = color_list[p],
        zorder = 3)

    if which_data == "pav300_V2":
        if p == 0:

            x_val = np.arange(0,100,1)
            plt.plot(x_val, 0.0055*x_val, '--k', zorder = 1)
            plt.plot(x_val, 0.0046*x_val, '--k', zorder = 1)
            plt.plot(x_val, 0.0029*x_val, '--k', zorder = 1)

# Legend
custom_lines = [Line2D([0], [0], color='white',marker = 'o', mec = 'k', ls = '', ms = 7),
                Line2D([0], [0], color='white',marker = 's', mec = 'k', ls = '', ms = 7),
                Line2D([0], [0], color='white',marker = 'v', mec = 'k', ls = '', ms = 7)]
plt.legend(
    custom_lines,
    [
        '$\epsilon_{zz}^{ampl}$',
        '$\epsilon_v^{ampl}$',
        '$\epsilon_q^{ampl}$'
    ],
    loc = 'upper left',
    fontsize = LGF)

# Ajust Labels
plt.xlim(0,100)
plt.ylim(0,)
plt.xlabel('Stress amplitude ($q^{ampl}) [kPa]$', fontsize = LBF)
plt.ylabel('Strain amplitude ($\epsilon^{ampl}$) [$10^{-4}$]', fontsize = LBF)
plt.grid(ls = '--', lw = 1, color = 'gray')
plt.gca().tick_params(which = 'major', labelsize = TS)
plt.tight_layout()

os.chdir(r'C:\Users\shrab\Google Drive\PhD\My Writing\Paper_CyclicMean')
plt.savefig(f'StrainAmplitude_qampl_{which_data}_cyclicmean.png', format='png')
plt.savefig(f'StrainAmplitude_qampl_{which_data}_cyclicmean.eps', format='eps')
plt.show()
