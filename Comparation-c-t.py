#%%
from Helpers import *
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
import os
import quantities as pq

plt.style.use('MyStyle.mplstyle')
mpl.use('Qt5Agg')
plt.close('all')

FilePath = ('simulation')
FilesIn = ['cyton.csv',
           'texas.csv']
colors= ('blue', 'red', 'green', 'yellow', 'purple')
signals = {}
for File in FilesIn:
    print(File)
    file_path = os.path.join(FilePath, File)
    signal_data= read_excel(file_path)
    name = os.path.splitext(File)[0]
    signals[name] = signal_data

#%% PSD
fig, ax = plt.subplots(1, 1, sharex=True, sharey=True)
line = ('-', ':')
for i, simulations in enumerate(signals):
    linestyle = line[i]
    for j, sig in enumerate(signals[simulations]):
        color = colors[j]
        plot_spectral_density(sig.rescale('uV'),
                              ax=ax,
                              color=color,
                              label=f' {sig.name[3:-2]} ({simulations})',
                              alpha = 0.9,
                              linestyle=linestyle
                              )
        ax.set_xlim(0, 160)
        ax.set_ylim(10**-11, 10**12)

        ax.legend(loc='best', fontsize=14)
        ax.set_xlabel('Frequency [Hz]',  fontsize=14)
        ax.set_ylabel('PSD ($\mu$V$^2$/Hz)',  fontsize=14)
ax.grid()
ax.axvline(x=110, color='black', linestyle='--', label='110 Hz', alpha=0.7)
ax.axvline(x=50, color='black', linestyle='--', label='50 Hz', alpha=0.7)
ax.tick_params(axis='both', which='major', labelsize=12)
ax.text(113, ax.get_ylim()[1]*0.9, '110 Hz', color='black', fontsize=12, ha='left', va='top')
ax.text(53, ax.get_ylim()[1]*0.9, '50 Hz', color='black', fontsize=12, ha='left', va='top')
fig.suptitle('Comparison of bias between Texas structure and Cyton structure', fontsize=20, fontweight='bold')



