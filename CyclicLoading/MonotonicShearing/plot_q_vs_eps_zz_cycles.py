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

# FIGURE
# Define Plot Fontsizes
TF = 24     # Text font
LGF = 12   # Legend Font Size
LBF = 15    # Label Font Size
TS = 12     # Tick Size
lw1 = 1

# IMPORTING DATA ==============================================================
root_path = r'F:\YieldSurface\YieldSurface_Cyclicmean\Shear_TX300_60'
dirs = ['0','C1','C5','C10','C20','C30','C40', 'C50']
labels = ['Initial Sample', 'Cycle 1', 'Cycle 5','Cycle 10', 'Cycle 20', 'Cycle 30', 'Cycle 40', 'Cycle 50']

color_list = cm.bone(np.linspace(0, 1, 10))[::-1]
plt.figure(figsize = (15,10))
print(color_list)
for i in range(len(dirs)):
    path = root_path + '\\' + dirs[i] +'\\merged_data'
    if i == 0:
        path = r"F:\YieldSurface\YieldSurface_Cyclicmean\300C0\merged_data"

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

    # FIGURE
    if i == 0:
        plt.plot(zstrain,q/10000,marker = '',markevery = 10,c='forestgreen',lw = lw1, alpha = 1, label = labels[i])
    elif i == len(dirs)-1:
        plt.plot(zstrain,q/10000,marker = '',markevery = 10,c='indianred',lw = lw1, alpha = 1, label = labels[i])
    else:
        plt.plot(zstrain,q/10000,marker = '',markevery = 10,c=color_list[i],lw = lw1, alpha = 0.9, label = labels[i])

# Figure Adjustments
plt.legend(fontsize = LGF, loc = 'lower right')
plt.xlim(-5,40)
plt.ylim(0,35)
plt.xlabel('Axial Strain ($\epsilon_{zz}$) [%]', fontsize = LBF)
plt.ylabel('Deviatoric Stress (q) [kPa]', fontsize = LBF)
plt.title('Sheared samples after cyclic loading at $p\'$=300kPa and $\sigma\'_{zz}^{amp}=60kPa$')
ax = plt.gca()
ax.tick_params(which='major', labelsize=TS)

plt.grid(ls = '--', c ='gray', lw = 1)
plt.show()
