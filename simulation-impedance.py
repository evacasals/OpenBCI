#%%
from Helpers import *
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
import os
colors=['blue', 'red', 'green']
plt.style.use('MyStyle.mplstyle')
mpl.use('Qt5Agg')
# plt.close('all')

FilePath = ('simulation-impedance')
FilesIn = ['bias_resistor.csv',
           'bias_short-circuited.csv',
           'no_bias.csv']

signals = {}
for File in FilesIn:
    print(File)
    file_path = os.path.join(FilePath, File)
    signal_data= read_excel(file_path)
    name = os.path.splitext(File)[0]
    signals[name] = signal_data
for sig in signals:

    signals[sig] = [signals[sig][i] for i in [1,2]]
#%% PSD
fig, ax = plt.subplots(1, 1, sharex=True, sharey=True)
line = ('-', 'dashed',':','-')
for i, simulations in enumerate(signals):
    linestyle = line[i]

    for j, sig in enumerate(signals[simulations]):
        color = colors[j]

        plot_spectral_density(sig.rescale('uV'),
                              ax=ax,
                              color=color,
                              label=f' {sig.name[3:-2]} ({simulations})',
                              alpha = 0.75,
                              linestyle=linestyle
                              )

        ax.set_xlim(0, 150)
        ax.set_ylim(10**-8,10**13)
        ax.legend(loc='best', fontsize=14)
        ax.set_xlabel('Frequency [Hz]',  fontsize=14)
        ax.set_ylabel('PSD ($\mu$V$^2$/Hz)',  fontsize=14)
ax.grid(True)
ax.axvline(x=31.5, color='black', linestyle='--', label='31.5 Hz', alpha=0.7)
ax.tick_params(axis='both', which='major', labelsize=12)
ax.text(33, ax.get_ylim()[1]*0.9, '31.5 Hz', color='black', fontsize=12, ha='left', va='top')
fig.suptitle('Comparison of bias_out pin connection and non-connection', fontsize=20, fontweight='bold')
