import os
import numpy as np 
import pandas as pd 
import seaborn as sns 
import matplotlib.pyplot as plt 

from scipy.optimize import curve_fit
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.model_selection import train_test_split

# Definig Plot Fontsizes
TF = 24     # Text font
LGF = 18   # Legend Font Size
LBF = 16    # Label Font Size
TS = 14     # Tick Size
LW1 = 2

# Training Data 
path15_P0_0 = r'E:\CyclicLoading\Cyclicmean\TX300_FC0p25to0p25_amp15\merged_data\SortedData\0_StartingPos'
path15_P0_1 = r'E:\Monotonic_Undrained\300kPa_15'

path30_P0_0 = r'E:\CyclicLoading\Cyclicmean\TX300_FC0p25to0p25_amp30\merged_data\SortedData\0_StartingPos'
path30_P0_1 = r'E:\Monotonic_Undrained\300kPa_30'

path60_P0_0 = r'E:\CyclicLoading\Cyclicmean\TX300_FC0p25to0p25_amp60\merged_data\SortedData\0_StartingPos'
path60_P0_1 = r'E:\Monotonic_Undrained\300kPa_60'

path90_P0_0 = r'E:\CyclicLoading\Cyclicmean\TX300_FC0p25to0p25_amp90\merged_data\SortedData\0_StartingPos'
path90_P0_1 = r'E:\Monotonic_Undrained\300kPa_90'

path90_P2_0 = r'E:\CyclicLoading\Cyclicmean\TX300_FC0p25to0p25_amp90\merged_data\SortedData\2_NeutralPos'
path90_P2_1 = r'E:\Monotonic_Undrained\300kPa_90_P2'

# DataSets for prediction 
path0_0 = r'E:\CyclicLoading\Cyclicmean_OneWay\TX390_FC0p25to0p25_amp90\SortedData\Neutral_Pos'
path0_1 = r'E:\CyclicLoading\Cyclicmean_OneWay\UndrainedShearing\TX390_FC0p25to0p25_amp90\Position3'

path1_0 = r'E:\CyclicLoading\Cyclicmean_OneWay\TX330_FC0p25to0p25_amp30\SortedData\Neutral_Pos'
path1_1 = r'E:\CyclicLoading\Cyclicmean_OneWay\UndrainedShearing\TX330_FC0p25to0p25_amp30\Position3'

path2_0 = r'E:\CyclicLoading\Cyclicmean_OneWay\TX360_FC0p25to0p25_amp60\SortedData\Neutral_Pos'
path2_1 = r'E:\CyclicLoading\Cyclicmean_OneWay\UndrainedShearing\TX360_FC0p25to0p25_amp60\Position3'

path3_0 = r'E:\CyclicLoading\Cyclicmean_OneWay\TX270_FC0p25to0p25_amp30_rate1000\SortedData\Neutral_Pos'
path3_1 = r'E:\CyclicLoading\Cyclicmean_OneWay\UndrainedShearing\TX270_FC0p25to0p25_amp30\Position1'

path4_0 = r'E:\CyclicLoading\Cyclicmean_OneWay\TX240_FC0p25to0p25_amp60_rate1000\SortedData\Neutral_Pos'
path4_1 = r'E:\CyclicLoading\Cyclicmean_OneWay\UndrainedShearing\TX240_FC0p25to0p25_amp60\Position1'

cycles = [0,1,2,3,4,5,10,20,30,40,50]
cycles_u = [1,2,3,4,5,6,10,20,30,40,50]

def get_merged_df(path0, path1, cycles):
    os.chdir(path0)
    FN_CN_a = pd.read_csv('FN_CN_a.csv')
    FN_CN_a['ratio'] = FN_CN_a.meanRSF/FN_CN_a.meanFN
    q_max = []
    e_list = []
    for c in cycles:
        os.chdir(path1 + rf'\Cycle{c}\merged_data')
        stress_data = pd.read_csv('stress_data.csv')

        # Convert to numpy
        np_stress_data = {}
        col_names = stress_data.columns
        for i, name in enumerate(col_names):
            np_stress_data[f"{name}"] = stress_data.iloc[:,i].to_numpy().T

        stress_xx = stress_data.stress_xx.to_numpy()
        stress_yy = stress_data.stress_yy.to_numpy()
        stress_zz = stress_data.stress_zz.to_numpy()
        stress_xy = stress_data.stress_xy.to_numpy()
        stress_yz = stress_data.stress_yz.to_numpy()
        stress_xz = stress_data.stress_xz.to_numpy()

        # Calculate q p
        #q = (np_stress_data['stress_zz'] - np_stress_data['stress_xx'])
        q = np.sqrt(0.5*((stress_xx-stress_yy)**2+(stress_yy-stress_zz)**2+(stress_xx-stress_zz)**2+3*(stress_xy**2+stress_yz**2+stress_xz**2)))

        q_max.append(np.max(q))

        # void ratio
        v_data = pd.read_csv('void_data.csv')
        e = v_data.void_ratio[0]
        e_list.append(e)

    d = {'cycle_number': cycles, 'q_max': q_max, 'void_ratio': e}
    q_max_df = pd.DataFrame(data=d)

    merged_df = FN_CN_a.merge(q_max_df, on = 'cycle_number')
    return merged_df 

# get training data
merged_df15 = get_merged_df(path15_P0_0, path15_P0_1, cycles)
merged_df30 = get_merged_df(path30_P0_0, path30_P0_1, cycles)
merged_df60 = get_merged_df(path60_P0_0, path60_P0_1, cycles)
merged_df90 = get_merged_df(path90_P0_0, path90_P0_1, cycles)
merged_df90_P2 = get_merged_df(path90_P2_0, path90_P2_1, cycles)

# Merging data for scaling 
frames = [merged_df15, merged_df30, merged_df60, merged_df90, merged_df90_P2]
whole_data = pd.concat(frames) 

# get prediction data 
merged_df0 = get_merged_df(path0_0, path0_1, cycles)
merged_df1 = get_merged_df(path1_0, path1_1, cycles)
merged_df2 = get_merged_df(path2_0, path2_1, cycles)
merged_df4 = get_merged_df(path4_0, path4_1, cycles_u)

# Scaling 
scaler = StandardScaler()

# Model Training with whole df 
X = scaler.fit_transform(whole_data[['mechanical_coord', 'ratio','a_mean', 'void_ratio']])
y = scaler.fit_transform(whole_data[['q_max']])

model = LinearRegression()
model.fit(X, y)

#calculate R-squared of regression model
r_squared = model.score(X, y)
print(r_squared)

# Predict 1
def get_prediction(merged_df, cycles): 

    X_p = scaler.fit_transform(merged_df[['mechanical_coord', 'ratio','a_mean', 'void_ratio']])
    y_p = scaler.fit_transform(merged_df[['q_max']])

    predicted = model.predict(X_p)
    predicted = scaler.inverse_transform(predicted)
    real = merged_df.q_max.to_numpy()
    predicted_list = [item for sublist in predicted for item in sublist]

    d = {'predicted': predicted_list, 'real':real}
    df = pd.DataFrame(data=d)

    return real, predicted_list, df 


real0, predicted0, df0  = get_prediction(merged_df0, cycles)
real1, predicted1, df1  = get_prediction(merged_df1, cycles)
real2, predicted2, df2  = get_prediction(merged_df2, cycles)
#real3, predicted3, df3  = get_prediction(merged_df3, cycles)
real4, predicted4, df4  = get_prediction(merged_df4, cycles)

print(df0)
print('Intercept:', model.intercept_)
print('Coefficients:', model.coef_)

plt.figure(1, figsize = (7,5))
x1 = merged_df0.cycle_number
y1 = [val/1000 for val in real0]
y2 = [val/1000 for val in predicted0]
plt.plot(x1, y1, color = 'forestgreen', marker = 's', mec = 'black', ls = ':', lw = LW1, label = "Actual $q^{peak}$")
plt.plot(x1, y2, color = 'indianred', marker = 's', mec = 'black', ls = ':', lw = LW1, label = "Modelled $q^{peak}$")

plt.xlabel("Cycle number (N)", fontsize = LBF)
plt.ylabel("Peak deviatoric stress ($q^{peak}$) [kPa]", fontsize = LBF)
plt.legend(loc = 'lower right', fontsize = LGF)
plt.gca().tick_params(axis='both', which='major', labelsize=TS)
plt.grid()
plt.tight_layout()

coefficients =  [i for b in model.coef_ for i in b]
print(sum(coefficients))

# Figure 2 
plt.figure(2, figsize = (7,5))

plt.bar(x = [r'$\bar{C}^*_N$', r'$\frac{F_t^{mean}}{F_n^{mean}}$',r'$a$', r'$e$'], 
        height = coefficients, 
        color = 'dimgray', 
        edgecolor = 'black',
        width = 0.3)
plt.hlines(y = 0, xmin=-1, xmax=3.5, ls = '--', color = 'black')

plt.xlim(-0.5,3.5)
plt.xlabel("Feature name", fontsize = LBF)
plt.ylabel("Feature importance $(t)$", fontsize = LBF)
plt.gca().tick_params(axis='both', which='major', labelsize=TS)
plt.tight_layout()

plt.show()