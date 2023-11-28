import os
import fnmatch
import numpy as np
import pandas as pd
from matplotlib.pyplot import cm
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,
                               AutoMinorLocator)
from sklearn.linear_model import LinearRegression
import scipy.fftpack

# PROCESSING ==================================================================
# Calculating strain
def get_strain(length):
    strain = ((length[0]-length)/length[0])*100
    return strain

TF = 24     # Text font
LGF = 12   # Legend Font Size
LBF = 15    # Label Font Size
TS = 12     # Tick Size
lw1 = 2     # Line Width

# strain range
smin = 0
smax = 20.01
sint = 0.01

# IMPORTING DATA ==============================================================
root_path = r'E:\YieldSurface\YieldSurface_Cyclicmean\Shear_TX300_90'
dirs = ['0','C1','C5','C10','C20','C30','C40', 'C50']
labels = ['Initial Sample', 'Cycle 1', 'Cycle 5','Cycle 10', 'Cycle 20', 'Cycle 30', 'Cycle 40', 'Cycle 50']

color_list = cm.bone(np.linspace(0, 1, 10))[::-1]
plt.figure(figsize = (7,7))
print(color_list)
for i in range(len(dirs)):
    path = root_path + '\\' + dirs[i] +'\\merged_data'
    if i == 0:
        path = r"E:\YieldSurface\YieldSurface_Cyclicmean\C0\merged_data"

    os.chdir(path)
    print('Current Directory')
    print(path)

    # Importing Stress
    df = pd.read_csv('stress_data.csv')
    print(df.head())
    step, xxstress, yystress, zzstress, xystress, xzstress, yzstress, xlength, ylength, zlength = df.to_numpy().T

    # Calculating Strain and Deviatoric Stress
    xstrain = get_strain(xlength)
    ystrain = get_strain(ylength)
    zstrain = get_strain(zlength)

    eps_q = (2/3)*(zstrain - 0.5*(xstrain + ystrain))
    eps_v = (xstrain + ystrain + zstrain)

    q = (zzstress - xxstress)
    p = (xxstress + yystress + zzstress)/3

    delta_zzstress = (zzstress-zzstress[0])/1000
    Delta_p = (p-p[0])/1000

    Delta_q = (q-q[0])/1000
    Delta_eps_q = (eps_q-eps_q[0])

    delta_q = np.zeros((len(q)-1))
    delta_eps_q = np.zeros((len(q)-1))
    secant_stiffness = []
    strain_val = np.arange(smin,smax,sint)
    for val in strain_val:
        index1 = np.argmax(zstrain>=val)
        secant_stiffness.append((q[index1]-q[0])/(zstrain[index1]*100-zstrain[0]*100)/1000)
    # FIGURE
    if i == 0:
        plt.semilogy(strain_val, secant_stiffness,c='forestgreen',lw = 2, ls = '--', alpha = 0.8, label = labels[i], zorder = 3)
    elif i == len(dirs)-1:
        plt.semilogy(strain_val, secant_stiffness,c='indianred',lw = 2, alpha = 0.8, label = labels[i], zorder = 2)
    else:
        plt.semilogy(strain_val, secant_stiffness,c=color_list[i],lw = lw1, alpha = 1, label = labels[i], zorder = 1)

# Figure Adjustments
plt.legend(fontsize = LGF, loc = 'upper right')
#plt.xlim(0,1)
plt.ylim(0,100)

plt.xlabel('Axial Strain ($\epsilon_{zz}$) [%]', fontsize = LBF)
plt.ylabel('Secant Stiffness [GPa]', fontsize = LBF)
#plt.title('Sheared samples after cyclic loading at $p\'$=300kPa and $\sigma\'_{zz}^{amp}=90kPa$', fontsize = TF)
ax = plt.gca()
ax.tick_params(which='major', labelsize=TS)

plt.grid(ls = '--', c ='gray', lw = 1)
plt.show()
