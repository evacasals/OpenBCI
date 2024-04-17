#%%
from Helpers import *
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
import os

plt.style.use('MyStyle.mplstyle')
mpl.use('Qt5Agg')
plt.close('all')

FilePath = ('simulation')
FilesIn = ['bias-cyton.csv',
           'nobias.csv']
colors= ('blue', 'red', 'green', 'yellow', 'purple')
signals = {}
for File in FilesIn:
    file_path = os.path.join(FilePath, File)
    signal_data= read_excel(file_path)
    name = os.path.splitext(File)[0]
    signals[name] = signal_data

#%% PSD
fig, ax = plt.subplots(1, 1, sharex=True, sharey=True)
for simulations in signals:

    for j, sig in enumerate(signals[simulations]):
        color = colors[j]
        plot_spectral_density(sig,
                              ax=ax,
                              color=color,
                              label=f' {sig.name[3:-2]} ({simulations})',
                              alpha = 0.9
                              )
        ax.set_xlim(0, 150)
        ax.set_ylim(10**-16, 10**0)
        ax.grid()
        ax.legend(loc='upper left', ncol=2)

ax.axvline(x=110, color='black', linestyle='--', label='110 Hz', alpha=0.7)
ax.axvline(x=50, color='black', linestyle='--', label='50 Hz', alpha=0.7)
ax.text(113, ax.get_ylim()[1]*0.9, '110 Hz', color='black', fontsize=12, ha='left', va='top')
ax.text(53, ax.get_ylim()[1]*0.9, '50 Hz', color='black', fontsize=12, ha='left', va='top')
fig.suptitle('Comparison of bias signal application and non-application', fontsize=20, fontweight='bold')

