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
FilesIn = ['nobias.csv']

signals = {}
for File in FilesIn:
    file_path = os.path.join(FilePath, File)
    signal_data= read_excel(file_path)
    name = os.path.splitext(File)[0]
    signals[name] = signal_data

#%%
# for simulations in signals:
#     diff = signals[simulations][2] - signals[simulations][2]
#     sig = AnalogSignal(diff,
#                        units='uV',
#                        sampling_rate=10000 * pq.Hz,
#                        name='diff'
#                        )
#     signals[simulations].append(sig)
#%% Plot Signals
fig, ax = plt.subplots(1, 1, sharex=True, sharey=True)
#
# ax = ax.flatten()
#for j, simulations in enumerate(signals):
#    for sig in signals[simulations]:
#       ax[j].plot(sig)
#        print(sig.name)
#       print(j)
for j, simulations in enumerate(signals):
    print(j)
    for sig in signals[simulations]:
        ax.plot(sig, label=sig.name)
        ax.legend()

plt.grid()
#%% PSD
fig, ax = plt.subplots(1, 1, sharex=True, sharey=True)
for j, simulations in enumerate(signals):
    for sig in signals[simulations]:
        plot_spectral_density(sig,
                              ax=ax,
                              label=sig.name,
                              alpha = 0.7
                              )
        ax.set_xlim(0, 150)
        ax.legend()

