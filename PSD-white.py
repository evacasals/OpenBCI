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

colors= ['blue', 'red']

excel = pd.read_excel('experiments\\data.xlsx', sheet_name='experiments')
file_label = dict(zip(excel['name'], excel['label']))
#%% Noise
BW=1000*pq.Hz
rms = 0.28*pq.uV
noise_psd = (rms**2)/BW
#%%
# Load OpenBCI Files
FilePath = 'experiments'
FilesIn = ['20240429_1.txt'
           ]
signals = {}
for File in FilesIn:
    file_path = os.path.join(FilePath, File)
    signal_data= read_file_oBCI(file_path)
    name = os.path.splitext(File)[0]
    signals[name] = signal_data

#%% plot all PSD Some Channels
sum = 0
fig, ax = plt.subplots(1, 1, sharex=True, sharey=True)
mean_signals = []

for i, experiment in enumerate(signals):
    color = colors[i]
    for j, sig in enumerate(signals[experiment]):

        plot_spectral_density(sig,
                              ax=ax,
                              color=color,
                              alpha = 0.3
                              )
        sum += np.sum(sig.magnitude, axis=1)
        print(sum)
        print(sig)

# mean_signal = AnalogSignal(sum/3,
#                                units='uV',
#                                sampling_rate=1000*pq.Hz)
# plot_spectral_density(mean_signal,
#                               ax=ax,
#                               label='mean',
#                               color=color,
#                               alpha=1
#                               )

ax.set_xlim(0, 500)
ax.set_xlabel('Frequency (Hz)', fontsize=14)
ax.set_ylabel('(PSD $\mu$V$^2$/Hz)',  fontsize=14)
ax.tick_params(axis='both', which='major', labelsize=12)
    # ax.legend(loc='upper right', fontsize=12)
ax.grid(True)
fig.suptitle('Input-Referred Noise, PGA=24', fontsize=20, fontweight='bold')
ax.axhline(y=noise_psd, color='r', linestyle='--', label='Noise Level')
ax.axvline(x=262, color='black', linestyle='--', label='-3 dB')
ax.text(265, ax.get_ylim()[1]*0.9, '-3 dB Bandwidth: 262 Hz', color='black', fontsize=12, ha='left', va='top')
ax.text(502.5, noise_psd, 'Input Referred Noise', color='r', fontsize=12, verticalalignment='center', horizontalalignment='left', rotation=90)


