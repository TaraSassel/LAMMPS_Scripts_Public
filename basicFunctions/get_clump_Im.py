# Script to calculate Intertia and mass for a clump
import numpy as np
import math
import matplotlib.pyplot as plt

def get_mI(rho,d,AR,coord,flag_overlap,flag_trans):
    # flag_overlap: 1 if overlapping region is substracted
    #               0 if overlap is calculated twice
    x0 = coord[0]                       # sphere x coodrinate
    y0 = coord[1]                       # sphere y coodrinate
    z0 = coord[2]                       # sphere z coodrinate
    r = d/2                             # Radius
    OD = d*(2-AR)                       # Overlap distance
    CW = OD/2                           # Spherical cap width
    Vs = (4/3)*np.pi*r**3               # Volume of Sphere 1
    dc_x = r-CW                         # Distance from center of sphere to the CM of the overlap
    Vsc = (1/3)*np.pi*CW**2*(3*r-CW)    # Volume of spherical cap
    Vcs = Vs - Vsc                      # Volume of cutoff sphere
    I_s0 = (2/5)*(rho*Vs)*r**2          # Inertia of a sphere in respect to its center
    I_s = np.eye(3,3)*I_s0              # Tensor of a single sphere

    if flag_overlap == 1:
        m_comp = rho*Vcs                    # Mass of 1/2 clump (overlapping region substracted)
        m_clump = 2*m_comp                  # Mass of clump (overlapping region substracted)

        # m_comp = rho*Vcs          # Mass of 1/2 clump (overlapping region substracted)
        # m_clump = rho*Vcs+Vs*rho                 # Mass of clump (overlapping region substracted)

        # Inertia of a spherical cap respect to the center of a sphere
        I_cap = np.eye(3,3)
        I_cap[0,0] = (rho/30)*(np.pi*CW**3)*(3*CW**2-15*CW*r+20*r**2)
        I_cap[1,1] = (rho/60)*(np.pi*CW**2)*(-9*CW**3+45*CW**2*r-80*CW*r**2+60*r**3)
        I_cap[2,2] = I_cap[1,1]

        # Cut-off sphere inertia (respect to sphere center)
        I_cs = I_s - I_cap

        # Cut-off sphere inertia (respect to the center of mass of the clump)
        I_cc = I_cs
        I_cc[1,1] = I_cc[1,1]+m_comp*dc_x**2
        I_cc[2,2] = I_cc[2,2]+m_comp*dc_x**2

    if flag_overlap == 0:
        m_comp = rho*Vs                    # Mass of 1 Sphere
        m_clump = 2*m_comp                 # Mass of 2 Spheres

        # Inertia including double intersection
        I_cc = I_s
        I_cc[1,1] = I_cc[1,1]+m_comp*dc_x**2
        I_cc[2,2] = I_cc[2,2]+m_comp*dc_x**2

    # Clump inertia
    I_clump0 = 2*I_cc
    return I_clump0, m_clump

def get_transition(I_clump0,m_clump,coord,flag_trans,d,AR):
    r = d/2                             # Radius
    OD = d*(2-AR)                       # Overlap distance
    CW = OD/2                           # Spherical cap width
    # Translation matrix (parallel axis theorem)
    T_d0 = np.zeros((3,3))

    if flag_trans == 1:

        x0 = coord[0,0]-np.mean(coord[:,0])
        y0 = coord[0,1]-np.mean(coord[:,1])
        z0 = coord[0,2]-np.mean(coord[:,2])

        #x1=x0+r-CW
        x1 = x0

        T_d0[0,0]=m_clump*(y0**2+z0**2)
        T_d0[0,1]=-m_clump*(x1*y0)
        T_d0[0,2]=-m_clump*(x1*z0)
        T_d0[1,0]=T_d0[0,1]
        T_d0[1,1]=m_clump*(x1**2+z0**2)
        T_d0[1,2]=-m_clump*(y0*z0)
        T_d0[2,0]=T_d0[0,2]
        T_d0[2,1]=T_d0[1,2]
        T_d0[2,2]=m_clump*(x1**2+y0**2)
        print(T_d0)
    I_clump = I_clump0 + T_d0
    print('This is my transitional matrix:')
    print(T_d0)
    return I_clump

# ==============================================================================

def get_translation_check(coord_cm,flag_trans):
    # Translation matrix (parallel axis theorem)
    T_d0 = np.zeros((3,3))

    if flag_trans == 1:

        x0 = coord_cm[0]
        y0 = coord_cm[1]
        z0 = coord_cm[2]
        #x1=x0+r-CW
        x1 = x0

        T_d0[0,0]=(y0**2+z0**2)
        T_d0[0,1]=-(x1*y0)
        T_d0[0,2]=-(x1*z0)
        T_d0[1,0]=T_d0[0,1]
        T_d0[1,1]=(x1**2+z0**2)
        T_d0[1,2]=-(y0*z0)
        T_d0[2,0]=T_d0[0,2]
        T_d0[2,1]=T_d0[1,2]
        T_d0[2,2]=(x1**2+y0**2)

    return T_d0


def inscribed_clumps(P, AR, r_part):

    # Creating initial array
    sp = P.shape
    print('This is the shape of P')
    print(sp)
    P_clump = np.zeros((sp[0],sp[1]))
    P_clump_CM = np.zeros((sp[0],sp[1]))

    rd = r_part -(2-AR)*r_part
    i = 0
    j = 0
    while i < (sp[0]):
        P_clump[i,:] = [P[j,0]-rd[i],P[j,1],P[j,2]]
        P_clump[i+1,:] = [P[j,0]+rd[i],P[j,1],P[j,2]]

        P_clump_CM[i,:] = [-rd[i],0,0]
        P_clump_CM[i+1,:]  = [rd[i],0,0]
        i = i + 2
        j = j + 2

    return P_clump_CM , P_clump

def get_rotMat(v):
    r = np.sqrt(v[0]**2+v[1]**2+v[2]**2)
    ex = np.array([0, 0, 1]).T # x-axis, y-axis, z-axis
    cross1 = np.cross(v,ex)
    alpha = -np.arctan2(np.linalg.norm(cross1),np.dot(v,ex)) # angle between v and ex (MINUS)
    k = cross1/(np.linalg.norm(v)*np.linalg.norm(ex)*np.sin(alpha)) # unit normal of plane spanned by v, ex
    # Rotational formula
    vr0 = v*np.cos(alpha) + np.cross(k,v)*np.sin(alpha)+k*np.dot(k,v)*(1-np.cos(alpha))
        # Matrix form
        # See: https://en.wikipedia.org/wiki/Rodrigues%27_rotation_formula
    KM = np.array([[0,-k[2],k[1]],[k[2],0,-k[0]],[-k[1],k[0],0]])   # Matrix form of k
    R = np.eye(3) + np.sin(alpha)*KM + (1-np.cos(alpha))*np.dot(KM,KM) # Rotational Matrix
    R = R
    print('Rotational Matrix:')
    print(R)
    return R

def get_vol(d1,coord1,d2,coord2):

    x1 = coord1[0]                       # sphere x coodrinate
    y1 = coord1[1]                       # sphere y coodrinate
    z1 = coord1[2]                       # sphere z coodrinate
    r1 = d1/2                             # Radius

    x2 = coord2[0]                       # sphere x coodrinate
    y2 = coord2[1]                       # sphere y coodrinate
    z2 = coord2[2]                       # sphere z coodrinate
    r2 = d2/2                             # Radius

    dist = ((x2-x1)**2+(y2-y1)**2+(z2-z1)**2)**(0.5) # Distance between centroids
    clump_l = dist + d1 #Clump length
    AR = clump_l/d1
    print('Apsect Ratio')
    print(AR)
    OD = d1*(2-AR)                       # Overlap distance
    CW = OD/2                           # Spherical cap width
    Vs = (4/3)*np.pi*r1**3               # Volume of Sphere 1
    dc_x = r1-CW                         # Distance from center of sphere to the CM of the overlap
    Vsc = (1/3)*np.pi*CW**2*(3*r1-CW)    # Volume of spherical cap
    Vcs = Vs - Vsc                      # Volume of cutoff sphere
    Vclump = Vcs*2

    return Vclump
