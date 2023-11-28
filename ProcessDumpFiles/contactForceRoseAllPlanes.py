# Contact force rose 16/04/21

# Importing Libraries
import numpy as np
import sys
import os
import matplotlib.pyplot as plt
import pandas as pd
import math

from matplotlib import cm
from colorspacious import cspace_converter
from collections import OrderedDict
from matplotlib.ticker import *

#===============================================================================
# Define Plot Fontsizes
TF = 25     # Title Font Size
LGF = 19    # Legend Font Size
LBF = 12    # Label Font Size
TS = 18     # Tick Size

# Changing DIRECTORY
path = r"E:\StrainControlledCyclic\300kPa\Strain0p1\SortedData\Starting_Position"

# File Name
contact_file = "dump222739600.contact"

# ==============================================================================
# Processing Data
# ==============================================================================

#  First 14 quantities of the dump.contact_forces are .
#  0,1,2 = shear force components in x, y and z
#  3.	ccel = [magnitude of normal force]/[distance between particle centres]
#  4,5 = tagi & tagj of contacting particles
#  6,7,8 = coordinates x,y,z
#  9 = radius of i
#  10,11,12 = coordj x,y,z
#  13 = radius of j

# Loading Data
os.chdir(path+r"\contact")

data = pd.read_csv(contact_file,skiprows=9,delimiter=" ",header=None)
data = data.drop(data.columns[14],axis=1) # last column was Nan because of delimiter so needed to delete
data = data.to_numpy()  # converting to numpy array

# Get Timestep
timestep = pd.read_table(contact_file,skiprows=1,nrows=1,header=None)
timestep = timestep.to_numpy()
timestep = timestep[0][0]

# Getting Dimensions of Periodic Cell
box = pd.read_csv(contact_file,skiprows=5,nrows=3,delimiter=" ",header=None)
box = box.to_numpy()
box_dim = box[:,1]-box[:,0]

# Filtering Nonzero contact force data
find1 = np.nonzero(data[:,3])
data_n0 = data[find1,:][0]
print("Shape of data array: " + str(np.shape(data)))
print("Shape of data_n0 array: " + str(np.shape(data_n0)))

# Particle 1
X1 = data_n0[:,6]
Y1 = data_n0[:,7]
Z1 = data_n0[:,8]
R1 = data_n0[:,9]

# Particle 2
X2 = data_n0[:,10]
Y2 = data_n0[:,11]
Z2 = data_n0[:,12]
R2 = data_n0[:,13]

# 1. Distance between centroids (branch vector)
BV = np.zeros((len(X2),3))
BV[:,0] = X1-X2
BV[:,1] = Y1-Y2
BV[:,2] = Z1-Z2

BVL = np.sqrt(((X1-X2)**2)+((Y1-Y2)**2)+((Z1-Z2)**2))

# 2. Contact Normal Force
CNF = data_n0[:,3]*BVL
FT = np.zeros((3,3))            # Initializing Fabic Tensor
thetaxy = np.zeros((len(BV),))  # Initializing theta xy
thetaxz = np.zeros((len(BV),))  # Initializing theta xz
thetayz = np.zeros((len(BV),))  # Initializing theta yz

string1 = 'Adjustment needed for displacements and periodic boundary'

for i in range(len(BV)):
    if (np.abs(BV[i,0])>0.5*box_dim[0]):
        print(string1)
        break
    if (np.abs(BV[i,1])>0.5*box_dim[1]):
        print(string1)
        break
    if (np.abs(BV[i,2])>0.5*box_dim[2]):
        print(string1)
        break

    # Contact Normal Orientation
    # Nomalzing Branch Vector
    n = np.zeros((3,))
    n[0] = BV[i,0]/BVL[i]
    n[1] = BV[i,1]/BVL[i]
    n[2] = BV[i,2]/BVL[i]

    for k in range(3):
        for m in range(3):
            FT[k,m] = FT[k,m]+n[k]*n[m]

    if n[0]!=0:
        thetaxy[i] = np.arctan(n[1]/n[0])
        thetaxz[i] = np.arctan(n[2]/n[0])
    else:
        print("ZeroDevision at n[0]: " + str(i))
        thetaxy[i] = 0
        thetaxz[i] = 0
    if n[1]!=0:
        thetayz[i] = np.arctan(n[2]/n[1])
    else:
        print("ZeroDevision at n[1]: " + str(i))
        thetayz[i] = 0

FT = FT/len(BV)

# ==============================================================================
# FIGURES
# ==============================================================================
# A. Histogram

# Define Plot Colors
ec1 = "black"   # Edge Color
fc1 = "royalblue"  # Face Color

# Define Plot Fontsizes
TF = 25     # Title Font Size
LBF = 12    # Label Font Size
TS = 18     # Tick Size

# Initializing Figure
fig, ax = plt.subplots(1,3)

# Subplot 1
ax[0].set_title(r"$\Theta_{xy}$",fontsize = TF)
ax[0].hist(thetaxy*180/np.pi,10,ec=ec1, fc= fc1)

# Subplot 2
ax[1].set_title(r"$\Theta_{xz}$",fontsize = TF)
ax[1].hist(thetaxz*180/np.pi,10,ec=ec1, fc= fc1)

# Subplot 3
ax[2].set_title(r"$\Theta_{yz}$",fontsize = TF)
ax[2].hist(thetayz*180/np.pi,10,ec=ec1, fc= fc1)

# Adding Labels
for i, ax in enumerate(fig.axes):
    ax.set_xlabel("Degrees (°)", fontsize = LBF)
    ax.set_ylabel("Number of contacts per bin", fontsize = LBF)
    ax.set_xlim(-90,90)
    ax.tick_params(axis='both', which='major', labelsize = TS)

# ==============================================================================
# B. Rose Diagram

# Prcessing Rose Diagram Data
nbins = 20
binangle=2*np.pi/20
print("The number of bins is: " + str(nbins))
print("The defined bin angle is: " + str(np.rad2deg(binangle)))

xybin = np.floor(thetaxy/binangle)-1 #Values between 0 and 9
xybin = xybin - np.min(xybin)

xzbin = np.floor(thetaxz/binangle)-1 #Values between 0 and 9
xzbin = xzbin - np.min(xzbin)

yzbin = np.floor(thetayz/binangle)-1 #Values between 0 and 9
yzbin = yzbin - np.min(yzbin)

a = int(nbins/2)

forcexy = np.zeros((a,))
forcexz = np.zeros((a,))
forceyz = np.zeros((a,))
bincountxy = np.zeros((a,))
bincountxz = np.zeros((a,))
bincountyz = np.zeros((a,))

# Getting avarage contact force in that bin
for i in range(a):
    axy = np.argwhere(xybin==i)
    axz = np.argwhere(xzbin==i)
    ayz = np.argwhere(yzbin==i)

    bincountxy[i] = len(axy)
    bincountxz[i] = len(axz)
    bincountyz[i] = len(ayz)

    for m in range(len(axy)):
        forcexy[i] = forcexy[i] + CNF[axy[m]]

    for m in range(len(axz)):
        forcexz[i] = forcexz[i] + CNF[axz[m]]

    for m in range(len(ayz)):
        forceyz[i] = forceyz[i] + CNF[ayz[m]]

    forcexy[i] = forcexy[i]/len(axy)
    forcexz[i] = forcexz[i]/len(axz)
    forceyz[i] = forceyz[i]/len(ayz)

c = np.arange(-90,90,np.rad2deg(binangle))+np.rad2deg(binangle)/2
angles = np.deg2rad(c)

#Figure
fig, ax = plt.subplots(1,3, subplot_kw=dict(projection="polar"))

def definecolor(fillvals,plot_n):
    cmap = cm.get_cmap("Blues") #"BuGn #Reds #seismic
    #minval = min(fillvals)
    #maxval = max(fillvals)
    minval = 0.01
    maxval = 0.018
    space = maxval - minval
    norm = cm.colors.Normalize(vmin = minval, vmax = maxval,clip = False)
    precision = [4,3,3] # Should be adjsuted according to space mangnitude
    tickarray = [minval,minval+space/2,maxval]

    cbar = fig.colorbar(cm.ScalarMappable(norm=norm, cmap=cmap),ax=ax[plot_n],
    shrink=2,pad=0.1, orientation="horizontal", ticks = tickarray)
    cbar.ax.set_xticklabels(np.round(tickarray,precision[plot_n]), size=TS)
    #cbar.ax.tick_params(labelsize=LBF)
    cbar.set_label(label=r'Average contact normal force [N]',fontsize = 20)
    sm = cm.ScalarMappable(norm=norm,cmap=cmap)
    if plot_n != 1:
        cbar.remove()
    return sm

# Subplot 1
plot_n = 0
sm = definecolor(forcexy,plot_n)
ax[plot_n].set_title(r"$\Theta_{xy}$",fontsize = TF)
ax[plot_n].bar(angles,bincountxy,width=binangle, color=sm.to_rgba(forcexy), edgecolor='k',lw=2)
ax[plot_n].set_xticks(np.arange(np.deg2rad(-90),np.deg2rad(110),binangle))
ax[plot_n].set_xlim(np.deg2rad(-90),np.deg2rad(90))
ax[plot_n].text(np.deg2rad(-120),max(bincountxy)-10,ha = "center", s ="Number of Contacts", fontsize = LBF+5,rotation = 90)
ax[plot_n].tick_params(which = 'both', labelsize = TS, pad = 15)
# Subplot 2
plot_n = 1
sm = definecolor(forcexz,plot_n)
ax[plot_n].set_title(r"$\Theta_{xz}$",fontsize = TF)
ax[plot_n].bar(angles,bincountxz,width=binangle, color=sm.to_rgba(forcexz), edgecolor='k',lw=2)
ax[plot_n].set_xticks(np.arange(np.deg2rad(-90),np.deg2rad(110),binangle))
ax[plot_n].set_xlim(np.deg2rad(-90),np.deg2rad(90))
ax[plot_n].text(np.deg2rad(-120),max(bincountxz)-10,ha = "center", s ="Number of Contacts", fontsize = LBF+5,rotation = 90)
ax[plot_n].tick_params(which = 'both', labelsize = TS, pad = 15)
# Subplot 3
plot_n = 2
sm = definecolor(forceyz,plot_n)
ax[plot_n].set_title(r"$\Theta_{yz}$",fontsize = TF)
ax[plot_n].bar(angles,bincountyz,width=binangle, color=sm.to_rgba(forceyz), edgecolor='k',lw=2)
ax[plot_n].set_xticks(np.arange(np.deg2rad(-90),np.deg2rad(110),binangle))
ax[plot_n].set_xlim(np.deg2rad(-90),np.deg2rad(90))
ax[plot_n].text(np.deg2rad(-120),max(bincountyz)-10,ha = "right", s ="Number of Contacts", fontsize = LBF+5,rotation = 90)
ax[plot_n].tick_params(which = 'both', labelsize = TS, pad = 15)
# Show Figures
plt.show()
