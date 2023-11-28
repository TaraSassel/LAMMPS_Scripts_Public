
#Author: Tara Sassel
#Date: 23/06/2023

# Importing
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# =============================================================================
# Define Path
path = r'E:\CyclicLoading\Cyclicmean_OneWay\TX300_To_240z\merged_data' # Path to merged_data

# Time Step
time_step = 5.242309e-09 # s required to calculate wall velocity

# Define Plot Fontsizes
TF = 24     # Text font
LGF = 12   # Legend Font Size
LBF = 15    # Label Font Size
TS = 12     # Tick Size
lw1 = 2     # Line Width

# =============================================================================
# PROCESSING
# Load data
os.chdir(path)
void_data = pd.read_csv('void_data.csv')

plt.plot(void_data.step_v, void_data.void_ratio, lw = 2, c = 'navy')
plt.xlabel('Step number')
plt.ylabel('Void ratio (e)')
plt.tight_layout()
plt.show()
