"""
Author: Tara Sassel
Data: 28/11/2022

This script is to create a plot of a 3D surface in the p-q-eps space
"""

import os
import pandas as pd
import numpy as np
from matplotlib import cm
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from scipy.optimize import curve_fit

from basicFunctions.get_strain import get_strain
from basicFunctions.get_cyclicmean_data import get_cyclicmean_data

# ==============================================================================
path_list, color_list =  get_cyclicmean_data('all_V2','F')

# Defining Labels
label_list = [100, 100, 100, 100, 200, 200, 200, 200, 300, 300, 300, 300, 300]
pav = [100, 100, 100, 100, 200, 200, 200, 200, 300, 300, 300, 300, 300]
qav = [5, 10, 20, 30, 5, 10, 20, 30, 5, 6.7, 10, 20, 30]

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

# Initiating figure
fig = plt.figure(figsize = (10,10))
ax = plt.axes(projection='3d')
k = 0

# Points at zero
ax.plot3D(
    [0,0,0,0],
    [5,10,20,30],
    [0,0,0,0],
    ms = 10,
    ls = '',
    marker = 's',
    mec = 'black',
    color = "white",
    zorder = 2)

strain_values = []
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

    strain_values.append(list(strain_amp)[0])

    ax.plot3D(
        pav[p],
        qav[p],
        list(strain_amp)[0],
        ms = 10,
        ls = '',
        marker = 's',
        mec = 'black',
        color = color_list[p],
        zorder = 2)

z = [0,0,0,0] + strain_values

# Points for surface
x = [0,0,0,0,100,100,100,100,200,200,200,200,200,300,300,300,300]
y = [5, 10, 20, 30,5, 10, 20, 30, 5, 10, 20, 30, 5, 6.7, 10, 20, 30]
# test function
def function(data, a, b, c):
    x = data[0]
    y = data[1]
    print(a)
    print(b)
    print(c)
    return a * (x**b) * (y**c)

# get fit parameters from scipy curve fit
parameters, covariance = curve_fit(function, [x, y], z)
print(parameters)

# Residual sum of squares
residuals = z- function([x, y], *parameters)
ss_res = np.sum(residuals**2)

# Total sum of squares
ss_tot = np.sum((z-np.mean(z))**2)

# r squared
r_squared = 1 - (ss_res / ss_tot)
print("R squared")
print(r_squared)

# create surface function model
# setup data points for calculating surface model
model_x_data = np.linspace(min(x), max(x), 30)
model_y_data = np.linspace(min(y), max(y), 30)
X, Y = np.meshgrid(model_x_data, model_y_data)

# calculate Z coordinate array
Z = function(np.array([X, Y]), *parameters)

# plot surface
ax.plot_surface(X, Y, Z, alpha = 0.5, cmap=cm.viridis, edgecolors=(0,0,0,0.3), linewidth = 0.1)

# Add R2
ax.text2D(0.1,0.9, "$R^2$ =  %.4f" %r_squared, transform = ax.transAxes, fontsize = 14,
    bbox=dict(facecolor='none', edgecolor='black', boxstyle='round,pad=1'))

# ax.text2D(0.7,0.9,
#     r"$\epsilon_{zz}^{ampl} = ({%.4e}) \times (p'^{av})^{%.2f} \times (\zeta)^{%.3f}$" % (parameters[0], parameters[1], parameters[2]),
#     transform = ax.transAxes, fontsize = 12,
#     bbox=dict(facecolor='none', edgecolor='black', boxstyle='round,pad=1'))

# colorbar
m = cm.ScalarMappable(cmap=cm.viridis)
m.set_array(Z)
cbar = plt.colorbar(m, fraction = 0.03, pad = 0.1, alpha = 0.5)
cbar.ax.set_ylabel('Strain amplitude $(\epsilon_{zz}^{ampl})$ [%]', fontsize = LBF)
cbar.ax.tick_params(labelsize=TS)

ax.zaxis.set_rotate_label(False)  # disable automatic rotation
ax.set_xlabel("Average mean effective stress $(p'^{av})$ [kPa]", fontsize = LBF, labelpad=10)
ax.set_ylabel('Loading amplitude $(\zeta)$ [%]', fontsize = LBF, labelpad=10)
ax.set_zlabel('Strain amplitude $(\epsilon_{zz}^{ampl})$ [%]', fontsize = LBF, labelpad=10, rotation = 90)

ax.set_xlim(0,)
ax.set_ylim(0,)
ax.set_zlim(0,)

ax.set_facecolor("None")
ax.tick_params(which = 'major', labelsize = TS)
plt.show()
