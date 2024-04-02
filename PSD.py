import os
from Helpers import *
import matplotlib.pyplot as plt
import matplotlib as mpl
from PhyREC import SignalProcess as Spro
from PhyREC import PlotWaves as Rplt
from collections import OrderedDict
import math

plt.style.use('MyStyle.mplstyle')
mpl.use('Qt5Agg')
plt.close('all')

colors= plt.cm.tab10.colors[:8]
# Load OpenBCI Files
FilesIn = {'20240321_1.txt',
           '20240321_2.txt',
           '20240321_3.txt',
           '20240321_4.txt'

           }
signals = {}
for File in FilesIn:
    file_path = os.path.join(FilePath, File)
    signal_data= read_file_oBCI(file_path)
    name = os.path.splitext(File)[0]
    signals[name] = signal_data



#%% plot PSD Channels
nCols = 4
nRows = 2
fig, ax = plt.subplots(nCols, nRows, sharex=True, sharey=True)
ax = ax.flatten()
for i, experiment in enumerate(signals):
    color = colors[i]
    for j, sig in enumerate(signals[experiment]):
        plot_spectral_density(sig,
                              ax=ax[j],
                              label=f'{experiment}',
                              color=color)
        ax[j].set_title(f'Channel {j+1}')
        ax[j].legend(loc='right')

ax[6].set_xlabel('Frequency [Hz]')
ax[7].set_xlabel('Frequency [Hz]')
ax[0].set_ylabel('PSD [uV^2/Hz]')
ax[2].set_ylabel('PSD [uV^2/Hz]')
ax[4].set_ylabel('PSD [uV^2/Hz]')
ax[6].set_ylabel('PSD [uV^2/Hz]')


