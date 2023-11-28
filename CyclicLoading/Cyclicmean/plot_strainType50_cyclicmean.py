import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from basicFunctions.get_strain import get_strain
from basicFunctions.get_cyclicmean_data import get_cyclicmean_data

# ==============================================================================
path_list, color_list =  get_cyclicmean_data('all','F')

# Defining Labels
label_list = [100, 100, 100, 100, 200, 200, 200, 200, 300, 300, 300, 300]
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

    eps_v, eps_q, gamma, eps = epsqv(xstrain, ystrain, zstrain)

    wanted_indexL = []
    for step in wanted_stepsL:
        wanted_indexL.append(np.argmax(step_s>=step))
    wanted_indexU = []
    for step in wanted_stepsU:
        wanted_indexU.append(np.argmax(step_s>=step))

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

    strain_amp = np.abs(wanted_strainL-wanted_strainU)
    eps_v_amp = np.abs(wanted_eps_vL-wanted_eps_vU)
    eps_q_amp = np.abs(wanted_eps_qL-wanted_eps_qU)

    plt.figure(1)
    plt.plot(
        label_list[p],
        (strain_amp/100)*1000,
        marker = 'o',
        mec = 'k',
        color = color_list[p])
    plt.plot(
        label_list[p],
        (eps_v_amp/100)*1000,
        marker = 's',
        mec = 'k',
        color = color_list[p])
    plt.plot(
        label_list[p],
        (eps_q_amp/100)*1000,
        marker = 'v',
        mec = 'k',
        color = color_list[p])

from matplotlib.lines import Line2D
custom_lines = [Line2D([0], [0], color='gray',marker = 'o', mec = 'k', ls = '', ms = 7),
                Line2D([0], [0], color='gray',marker = 's', mec = 'k', ls = '', ms = 7),
                Line2D([0], [0], color='gray',marker = 'v', mec = 'k', ls = '', ms = 7)]


plt.legend(custom_lines, ['$\epsilon_{zz}^{ampl}$', '$\epsilon_v^{ampl}$', '$\epsilon_q^{ampl}$'], loc = 'upper left', fontsize = LGF)
plt.xlabel('Avarage mean pressure ($p^{av}) [kPa]$', fontsize = LBF)
plt.ylabel('Strain amplitude ($\epsilon^{ampl}$) [$10^{-4}$]', fontsize = LBF)
plt.grid(ls = '--', lw = 1, color = 'gray')
plt.gca().tick_params(which = 'major', labelsize = TS)
plt.show()
