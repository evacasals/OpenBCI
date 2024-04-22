#%%
from Helpers import *
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
import os
import quantities as pq

plt.style.use('MyStyle.mplstyle')
mpl.use('Qt5Agg')
#
excel = pd.read_excel('experiments\\data.xlsx', sheet_name='experiments')
file_label = dict(zip(excel['name'], excel['label']))
FilePath = ('experiments')
FilesIn = ['20240418_1.txt',
           '20240418_2.txt']
colors= ('blue', 'red', 'green', 'yellow', 'purple')
signals = {}
for File in FilesIn:
    print(File)
    file_path = os.path.join(FilePath, File)
    signal_data = read_file_oBCI(file_path)
    name = os.path.splitext(File)[0]
    signals[name] = signal_data
for sig in signals:
    signals[sig] = [signals[sig][i] for i in [0,1]]
#%% PSD
fig, ax = plt.subplots(1, 1, sharex=True, sharey=True)
line = (':', '-')
labels=('Vout', 'Bias')
for i, experiment in enumerate(signals):
    color = colors[i]

    for j, sig in enumerate(signals[experiment]):
        linestyle = line[j]
        label = labels[j]
        plot_spectral_density(sig,
                              ax=ax,
                              label=f'{label} ({file_label[experiment]})',
                              color=color,
                              linestyle=linestyle,
                              time=(5*pq.s, 40*pq.s),
                              alpha = 1
                              )

        ax.set_xlim(0, 100)
        ax.set_xlabel('Frequency (Hz)', fontsize=14)
        ax.set_ylabel('PSD ($\mu$V$^2$/Hz)',  fontsize=14)
        ax.tick_params(axis='both', which='major', labelsize=12)
        ax.legend(loc='best', fontsize=12)
        ax.grid(True)
ax.axvline(x=75, color='black', linestyle='--', label='110 Hz', alpha=0.7)
ax.axvline(x=10.5, color='black', linestyle='--', label='50 Hz', alpha=0.7)
ax.text(78, ax.get_ylim()[1]*0.9, '110 Hz', color='black', fontsize=12, ha='left', va='top')
ax.text(13, ax.get_ylim()[1]*0.9, '10 Hz', color='black', fontsize=12, ha='left', va='top')
fig.suptitle('Validation: Comparison of bias signal application and non-application', fontsize=20, fontweight='bold')