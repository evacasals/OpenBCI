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

excel = pd.read_excel('experiments\\data.xlsx', sheet_name='experiments')
file_label = dict(zip(excel['name'], excel['label']))

#%%
# Load OpenBCI Files
FilePath = 'experiments'
FilesIn = ['20240403_1.txt',
           '20240403_4.txt',
           '20240403_2.txt',
           '20240403_3.txt'

           ]
signals = {}
for File in FilesIn:
    file_path = os.path.join(FilePath, File)
    signal_data= read_file_oBCI(file_path)
    name = os.path.splitext(File)[0]
    signals[name] = signal_data



#%% plot PSD All Channels
nCols = 2
nRows = 4
fig, ax = plt.subplots(nCols, nRows, sharex=True, sharey=True)
ax = ax.flatten()
for i, experiment in enumerate(signals):
    color = colors[i]
    for j, sig in enumerate(signals[experiment]):
        plot_spectral_density(sig,
                              ax=ax[j],
                              label=file_label[experiment],
                              color=color,
                              time=(5*pq.s, 50*pq.s),
                              alpha = 0.7
                              )
        ax[j].set_title(f'Channel {j+1}')
        # ax[j].legend(loc='right')
        # ax[j].set_ylim([0.001, 10])
#%%
ax[4].set_xlabel('Frequency [Hz]')
ax[5].set_xlabel('Frequency [Hz]')
ax[6].set_xlabel('Frequency [Hz]')
ax[7].set_xlabel('Frequency [Hz]')
ax[0].set_ylabel('PSD [uV^2/Hz]')
ax[2].set_ylabel('PSD [uV^2/Hz]')
ax[4].set_ylabel('PSD [uV^2/Hz]')
ax[6].set_ylabel('PSD [uV^2/Hz]')
fig.suptitle('Input-Referred Noise in Normal Mode, PGA GAIN = 1', fontsize=20, fontweight='bold')

#%% #%% plot PSD One Channels
signals2 = {}
for sig in signals:
    signals2[sig] = [signals[sig][i] for i in [1]]

#%% plot PSD Some Channels
fig, ax = plt.subplots(1, 1, sharex=True, sharey=True)
for i, experiment in enumerate(signals2):
    color = colors[i]
    for j, sig in enumerate(signals2[experiment]):
        plot_spectral_density(sig,
                              ax=ax,
                              label=file_label[experiment],
                              color=color,
                              time=(5*pq.s, 60*pq.s),
                              alpha = 0.8
                              )
        ax.set_title(f'Channel {j + 1}', fontsize=16)

        ax.set_xlim(0, 500)
        ax.set_xlabel('Frequency (Hz)', fontsize=14)
        ax.set_ylabel('PSD ($\mu$V$^2$/Hz)',  fontsize=14)
        ax.tick_params(axis='both', which='major', labelsize=12)
        ax.legend(loc='upper right', fontsize=12)
        ax.grid(True)
fig.suptitle('Input-Referred Noise in Normal Mode, PGA GAIN = 1', fontsize=20, fontweight='bold')
ax.axvline(x=262, color='black', linestyle='--', label='262 Hz')
ax.axvline(x=65.5, color='black', linestyle='--', label='65 Hz')
ax.text(265, ax.get_ylim()[1]*0.9, '262 Hz', color='black', fontsize=12, ha='left', va='top')
ax.text(68.5, ax.get_ylim()[1]*0.9, '65 Hz', color='black', fontsize=12, ha='left', va='top')


