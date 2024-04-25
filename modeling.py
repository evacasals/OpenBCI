import os
from Helpers import *
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd

from PhyREC import SignalProcess as Spro
from PhyREC import PlotWaves as Rplt
from collections import OrderedDict
import math

plt.style.use('MyStyle.mplstyle')
mpl.use('Qt5Agg')
plt.close('all')

colors= plt.cm.tab10.colors

excel = pd.read_excel('experiments/data.xlsx', sheet_name='experiments')
file_label = dict(zip(excel['name'], excel['label']))
#%% Noise
Vpp = 1*pq.uV
f=70*pq.Hz
rms = Vpp/(2*math.sqrt(2))
noise_psd = (rms**2)/f
#%%
# Load OpenBCI Files
FilePath = 'experiments'
FilesIn = ['20240423_5.txt',
           '20240423_6.txt'
           ]
signals = {}
for File in FilesIn:
    file_path = os.path.join(FilePath, File)
    signal_data= read_file_oBCI(file_path)
    name = os.path.splitext(File)[0]
    signals[name] = signal_data
for sig in signals:
    signals[sig] = [signals[sig][i] for i in [0]]


#%%Figure
fig, ax = plt.subplots(1, 1, sharex=True, sharey=True)
for i, experiment in enumerate(signals):
    for j, sig in enumerate(signals[experiment]):
        plot_spectral_density(sig,
                              ax=ax,
                              label=file_label[experiment],
                              alpha = 0.8,
                              time=(80*pq.s, 200*pq.s)
                              )


        ax.set_xlim(0, 70)
        ax.set_ylim(10**-11, 10**12)
        ax.legend(loc='best', fontsize=14)
        ax.set_xlabel('Frequency [Hz]', fontsize=14)
        ax.set_ylabel('PSD ($\mu$V$^2$/Hz)', fontsize=14)
ax.grid()
ax.axhline(y=noise_psd, color='r', linestyle='--', label='Noise Level')
ax.text(70.5, noise_psd, 'Input Referred Noise', color='r', fontsize=12, verticalalignment='center', horizontalalignment='left', rotation=90)
fig.suptitle('Comparison of bias signal application and non-application', fontsize=20, fontweight='bold')