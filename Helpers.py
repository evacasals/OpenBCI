
import pandas as pd
from matplotlib import pyplot as plt
from neo.core import AnalogSignal
from scipy import signal
import numpy as np
import quantities as pq
from PhyREC import SignalProcess as Spro

def read_file_oBCI(FileIn, colors=None):
    CMD_nChannels = '%Number of channels'
    CMD_Fs = '%Sample Rate'

    Header_count = 0
    Fin = open(FileIn, 'r')
    while True:
        line = Fin.readline()
        if line.startswith('%'):
            Header_count += 1
            # print(line)
            if line.startswith(CMD_nChannels):
                nChannels = int(line.split('=')[1])
            if line.startswith(CMD_Fs):
                Fs = int(line.split('=')[1].split(' ')[1]) * pq.Hz
        else:
            break
    Fin.close()

    data = pd.read_table(FileIn, sep=', ', header=Header_count, engine='python')
    data = data.iloc[:, 1:nChannels + 1]

    Sigs = []
    for ic, c in enumerate(data.columns):
        sig = AnalogSignal(data[c],
                           units='uV',
                           sampling_rate=Fs,
                           name=c)
        if colors is not None:
            sig.annotate(color=colors[ic])
        Sigs.append(sig)
    return Sigs
# %% FFT
def plot_spectral_density(sig, ax, Fmin=1, time=None, **kwargs):
    if time is not None:
        c = sig.time_slice(*time)
    else:
        c = sig
    Fs = sig.sampling_rate.magnitude
    nFFT = int(2 ** (np.around(np.log2(Fs / Fmin)) + 1))  # Cálculo de la longitud que ha de tener la FFT
    ff1, psd1 = signal.welch(x=c, fs=Fs,
                             axis=0,
                             nperseg=nFFT,
                             scaling='density'
                             )  # Cálculo de la FFT

    ax.semilogy(ff1, psd1, **kwargs)


def GenSlots(SigsPl, Procs):
    nSigs = len(SigsPl)
    Figplot, Axs = plt.subplots(nSigs, 1, sharex=True)
    Axs = Axs.flatten()

    SlotsPl = []
    for ic, sig in enumerate(SigsPl):
        axp = None
        for proc in Procs:
            axi = Axs[ic]
            if proc['TwinAx']:
                axp = plt.twinx(axi)
            else:
                axp = axi

            fkwarg = proc['FunctionKwarg'].copy()
            if fkwarg['color'] == 'auto':
                fkwarg['color'] = sig.annotations['color']

            sp = Spro.ApplyProcessChain(sig, proc['ProcesChain'])
            sp.name = sp.name + ' ' + proc['SigSufix']
            sp.annotations.update(proc)
            SlotsPl.append(proc['SlotFunc'](sp,
                                          Ax=axp,
                                          **fkwarg))
    return SlotsPl, Figplot, Axs