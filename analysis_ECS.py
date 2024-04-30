import pandas as pd
import matplotlib.pyplot as plt
from scipy import signal
from neo.core import AnalogSignal
from neo.core import Event
import quantities as pq
import numpy as np
from PhyREC import SignalProcess as Spro
from PhyREC import PlotWaves as Rplt
from PhyREC import SignalAnalysis as San


plt.style.use('MyStyle.mplstyle')
plt.close('all')


Freqs = 250
Ts = 1/Freqs
freqs = Freqs/(0.5 * Freqs)
colors = plt.cm.tab10.colors
Irms = 6*pq.nA / np.sqrt(2)

def read_file(FileIn):
    data = pd.read_table(FileIn['file'], sep=', ', header=4, engine='python')
    data = data.iloc[:, list(range(1, 4)) + [8]]
    # data = data.iloc[:, list(range(1, 9))]
    SigsPl = []
    for c, color in zip(data.columns, FileIn['colors']) :
        
        sig= AnalogSignal(data[c],
                                 units='uV',
                                 sampling_rate=250 * pq.Hz,
                                 name=c)
        sig.annotate(color=color)
    
        SigsPl.append(sig)
        
    return SigsPl
#%% FFT
def plot_spectral_density(sig, time, Freqs, Fmin, ax, color, name=None, typeline=None, alpha=None):

    c = sig.time_slice(*time)
    nFFT = int(2**(np.around(np.log2(Freqs/Fmin))+1))  # Cálculo de la longitud que ha de tener la FFT
    ff1, psd1 = signal.welch(x=c, fs=Freqs,
                             axis=0,
                             nperseg=nFFT,
                             scaling='density')  # Cálculo de la FFT
    
    
    if name is not None:
        ax.semilogy(ff1, psd1,
                    color=color,
                    label=name,
                    linestyle=typeline,
                    alpha=alpha)
    else: 
        ax.semilogy(ff1, psd1,
                    color=color,
                    linestyle=typeline,
                    alpha=alpha)
# #%% Plot impedance
# def plot_impedance(sig, time, Freqs, Fmin, ax, color, name=None):
#     c = sig.time_slice(*time)
#     ff1, psd1 = signal.welch(x=c, fs=Freqs,
#                              axis=0,
#                              nperseg=nFFT,
#                              scaling='density') 
    

#%% Read files        
FilesIn = (
    {'file': 'data/240122/240122.exp1.txt', 'colors': colors[:8]},
    {'file': 'data/240122/240122.exp2.txt', 'colors': colors[:8]},
    {'file': 'data/240122/240122.exp3.txt', 'colors': colors[:8]}
)  

SigsPl = read_file(FilesIn[0]) 
SigsImp =read_file(FilesIn[1])     
SigsPr = read_file(FilesIn[2])  

#%% GENERATING FIGURE 1
nSigs = len(SigsPl)
Figplot, Axs = plt.subplots(nSigs, 1, sharex=True)
Axs = Axs.flatten()

FiltEmpty = [{'function': Spro.Filter, 'args': {'Type': 'bandstop',
                                              'Order': 4,
                                              'Freqs': (49.5,50.5)}}, ]

# FiltEmpty = []

FiltEMG = FiltEmpty + [{'function': Spro.Filter, 'args': {'Type': 'highpass',
                                                          'Order': 4,
                                                          'Freqs': (1,)}}, ]

AxLEMG = {
    'ylim': (-0.2, 0.2),
    'facecolor': '#FFFFFF00',
    'autoscaley_on': False,
    'xaxis': {'visible': False,
              },
    'yaxis': {'visible': True,
              },
}

AxDC = {
    'ylim': (-150, -30),
    'facecolor': '#FFFFFF00',
    'autoscaley_on': False,
    'xaxis': {'visible': False,
              },
    'yaxis': {'visible': True,
              },
}


Procs = (

    {'ProcesChain':  FiltEmpty,
     'SlotFunc': Rplt.WaveSlot,
     'TwinAx': False,
     'SigSufix': 'EphysSig',
     'FunctionKwarg': {'Units': 'mV',
                       'color': 'k',
                       # 'linewidth': 1,
                       'alpha': 1,
                       'AxKwargs': AxDC,
                       'clip_on': False,
                       }
     },
    {'ProcesChain':  FiltEMG,
     'SlotFunc': Rplt.WaveSlot,
     'TwinAx': True,
     'SigSufix': 'fullsingal',
     'FunctionKwarg': {'Units': 'mV',
                       'color': 'auto',
                       'alpha': 1,
                       'AxKwargs': AxLEMG,
                       'clip_on': False,
                       }
     },
)


# %% Slots implementation
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


Splt = Rplt.PlotSlots(SlotsPl,
                      Fig=Figplot,
                      LiveControl=True,
                      TimeAxis=-1,
                      )

Splt.PlotChannels(None)
Splt.AddLegend()

#%% GENERATING FIGURE 2: Impedance
nSigs = len(SigsImp)
Figplot, Axs = plt.subplots(nSigs, 1, sharex=True)
Axs = Axs.flatten()

FiltImp = [{'function': Spro.Filter, 'args': {'Type': 'bandpass',
                                              'Order': 4,
                                              'Freqs': (22.88 ,34.33)}}, ]

tovrms = FiltImp + [{'function': Spro.sliding_window, 'args': {'timewidth': 1*pq.s}} ]



AxLEMG = {
    'ylim': (-0.4, 0.4),
    'facecolor': '#FFFFFF00',
    'autoscaley_on': False,
    'xaxis': {'visible': False,
              },
    'yaxis': {'visible': True,
              },
}

AxDC = {
    'ylim': (-200, -30),
    'facecolor': '#FFFFFF00',
    'autoscaley_on': False,
    'xaxis': {'visible': False,
              },
    'yaxis': {'visible': True,
              },
}


Procs = (

    {'ProcesChain':  FiltImp,
     'SlotFunc': Rplt.WaveSlot,
     'TwinAx': False,
     'SigSufix': 'ImpSig',
     'FunctionKwarg': {'Units': 'mV',
                       'color': 'k',
                       # 'linewidth': 1,
                       'alpha': 1,
                       'AxKwargs': AxDC,
                       'clip_on': False,
                       }
     },
    {'ProcesChain':  tovrms,
     'SlotFunc': Rplt.WaveSlot,
     'TwinAx': False,
     'SigSufix': 'VrmsSig',
     'FunctionKwarg': {'Units': 'mV',
                       'color': 'k',
                       # 'linewidth': 1,
                       'alpha': 1,
                       'AxKwargs': AxDC,
                       'clip_on': False,
                       }
     },
)


# %% Slots implementation
SlotsImp = []
for ic, sig in enumerate(SigsImp):
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
        SlotsImp.append(proc['SlotFunc'](sp,
                                      Ax=axp,
                                      **fkwarg))


Splt = Rplt.PlotSlots(SlotsImp,
                      Fig=Figplot,
                      LiveControl=True,
                      TimeAxis=-1,
                      )

Splt.PlotChannels(None)
Splt.AddLegend()
#%% #%% GENERATING FIGURE 3: Impedance + Protocol
nSigs = len(SigsPr)
Figplot, Axs = plt.subplots(nSigs, 1, sharex=True)
Axs = Axs.flatten()

FiltEmpty = [{'function': Spro.Filter, 'args': {'Type': 'bandstop',
                                              'Order': 4,
                                              'Freqs': (22.88 ,34.33)}}, ]
FiltImp = [{'function': Spro.Filter, 'args': {'Type': 'bandpass',
                                              'Order': 4,
                                              'Freqs': (22.88 ,34.33)}}, ]

# FiltEmpty = []

FiltEMG = FiltEmpty+[{'function': Spro.Filter, 'args': {'Type': 'highpass',
                                                          'Order': 4,
                                                          'Freqs': (1,)}}, ]
tovrms = FiltImp + [{'function': Spro.sliding_window, 'args': {'timewidth': 1*pq.s}} ]
# sliding_window(sig, timewidth, func=None, steptime=None, **kwargs):
AxLEMG = {
    'ylim': (-0.4, 0.4),
    'facecolor': '#FFFFFF00',
    'autoscaley_on': False,
    'xaxis': {'visible': False,
              },
    'yaxis': {'visible': True,
              },
}

AxDC = {
    'ylim': (-150, -30),
    'facecolor': '#FFFFFF00',
    'autoscaley_on': False,
    'xaxis': {'visible': False,
              },
    'yaxis': {'visible': True,
              },
}


Procs = (

    {'ProcesChain':  FiltEmpty,
     'SlotFunc': Rplt.WaveSlot,
     'TwinAx': False,
     'SigSufix': 'EphysSig',
     'FunctionKwarg': {'Units': 'mV',
                       'color': 'k',
                       # 'linewidth': 1,
                       'alpha': 1,
                       'AxKwargs': AxDC,
                       'clip_on': False,
                       }
     },
    {'ProcesChain':  FiltEMG,
     'SlotFunc': Rplt.WaveSlot,
     'TwinAx': True,
     'SigSufix': 'fullsingal',
     'FunctionKwarg': {'Units': 'mV',
                       'color': 'auto',
                       'alpha': 1,
                       'AxKwargs': AxLEMG,
                       'clip_on': False,
                       }
     },
    {'ProcesChain':  FiltImp,
     'SlotFunc': Rplt.WaveSlot,
     'TwinAx': False,
     'SigSufix': 'ImpSig',
     'FunctionKwarg': {'Units': 'mV',
                       'color': 'k',
                       # 'linewidth': 1,
                       'alpha': 1,
                       'AxKwargs': AxDC,
                       'clip_on': False,
                       }
     },
    {'ProcesChain':  tovrms,
     'SlotFunc': Rplt.WaveSlot,
     'TwinAx': False,
     'SigSufix': 'VrmsSig',
     'FunctionKwarg': {'Units': 'mV',
                       'color': 'k',
                       # 'linewidth': 1,
                       'alpha': 1,
                       'AxKwargs': AxDC,
                       'clip_on': False,
                       }
     },
)



# %% Slots implementation
SlotsPr = []
for ic, sig in enumerate(SigsPr):
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
        SlotsPr.append(proc['SlotFunc'](sp,
                                      Ax=axp,
                                      **fkwarg))


Splt = Rplt.PlotSlots(SlotsPr,
                      Fig=Figplot,
                      LiveControl=True,
                      TimeAxis=-1,
                      )

Splt.PlotChannels(None)
Splt.AddLegend()


#%% MEASURING EEG vs. MEASURING EEG DURING AN IMPEDANCE MEASURAMENT


AlphaTime = (160*pq.s, 340*pq.s)
QuickPest = (50*pq.s, 85*pq.s)
JawStrength = (110*pq.s, 145*pq.s)
Basal = (7*pq.s, 30*pq.s)

AlphaTime_i = (220*pq.s, 280*pq.s)
QuickPest_i = (50*pq.s, 80*pq.s)
JawStrength_i = (170*pq.s, 220*pq.s)
Basal_i = (7*pq.s, 30*pq.s)

meanalpha = []
meanquickpest = []
meanjawstrength = []
meanbasal = []

meanalpha_i = []
meanquickpest_i = []
meanjawstrength_i = []
meanbasal_i = []

#%% FIGURE THAT SHOWS THIS TWO SIGNALS COMPARED WHEN THEY ARE FILTERED
fig1, axs = plt.subplots(4, 1, sharex=True)
axs = axs.flatten()
compare = ({'signal' : SlotsPl,
            'analysistemes' : ((AlphaTime, 'Alpha', '#ADD8E6', meanalpha),
                  (QuickPest, 'Blink', '#87CEEB', meanquickpest),
                  (JawStrength, 'Jaw', '#AFEEEE', meanjawstrength),
                  (Basal, 'Basal', '#B0E0E6', meanbasal)),
            'typeline': 'solid',
            'axes' : axs,
            'color' : 'b',
            'name': 'REC EEG',
            'ylim': (-250, 250)},
           {'signal' : SlotsPr, 
           'analysistemes' : ((AlphaTime_i, 'Impedance Alpha', '#FFA500', meanalpha_i),
                 (QuickPest_i, 'Impedance Blink', '#FFD700', meanquickpest_i ),
                 (JawStrength_i, 'Impedance Jaw', '#FF8C00', meanjawstrength_i),
                 (Basal_i, 'Impedance Basal', '#FF6347', meanbasal_i)),
           'typeline': 'dashed',
           'color' : 'r',
           'name': 'REC EEG + Impedance',
           'ylim': (-1500, 1500)})

for group in compare:  
    j=0
    for c in group['signal']:
      if "fullsingal" in c.Signal.name:
            ax = axs[j] if group['signal'] == SlotsPl else axs[j].twinx()
            ax.set_ylim(group['ylim'])
            ax.set_ylabel('mV')
            ax.plot(c.Signal, color = group['color'], alpha=0.5, label = group['name'])
            ax.legend()
            j += 1
            



#%% FIGURE THAT SHOWS THIS TWO SIGNALS COMPARED WITH PSD
fig, ax = plt.subplots(figsize=(16, 9))
ax.set_xlim(0, 125)
ax.set_ylabel('PSD [V**2/Hz]')


for group in compare:  
    for c in group['signal']:
        if "fullsingal" in c.Signal.name:
            for time, name, color, mean in group['analysistemes']:
                plot_spectral_density(c.Signal, time, Freqs, 1, ax=ax, color=color, typeline=group['typeline'], alpha=0.25)
                mean.append(c.Signal)
    
                    
for group in compare:                   
    for time, name, color, mean in group['analysistemes']: 
        mean = AnalogSignal(np.mean(np.array(mean), axis=0),
                            units='uV',
                            sampling_rate=250 * pq.Hz,
                            name='mean'+name)
        plot_spectral_density(mean, time, Freqs, 1, ax=ax, color=color, name=name, typeline=group['typeline'])  
        
            
ax.grid()
ax.legend(loc='upper right')
fig.suptitle('Spectral density')
ax.set_xlabel('Frequency [Hz]')
fig.savefig('PSD-compare-protocol-impedanceornot.png', dpi=600)

#%% Figura Impedance Vrms Protocol vs no Protocol 

cmap_red = plt.cm.Reds(np.linspace(0.2, 1, 20))
cmap_blue = plt.cm.Blues(np.linspace(0.2, 1, 20))

compare_imp = ({'signal' : SlotsPr, 
                'alpha': 0.5,
                'group': 'REC EEG', 
                'color': cmap_red,},
                {'signal' : SlotsImp,
                 'alpha': 0.5,
                 'group': 'No REC EEG', 
                 'color': cmap_blue})


figi, axi = plt.subplots(figsize=(16, 9))
for group in compare_imp:
    cr=[]    
    for ic, c in enumerate(group['signal']):
        if "Vrms" in c.Signal.name:
            cr.append(c.Signal / Irms)
            axi.plot(cr[-1], label = group['group'] + ': ' + c.Signal.name, alpha=0.3, color=group['color'][ic])
    group['mean'] = np.mean(np.array(cr), axis=0)
    axi.plot(group['mean'], label=group['group'] + ': Mean', linestyle='--', color=group['color'][-1])

figi.suptitle('Impedance measurament')
axi.set_xlabel('Time [s]')
axi.set_ylabel('Impedance ['+u'\u03A9'+']')
axi.legend(loc='upper left', bbox_to_anchor=(0.85, 1), borderaxespad=0.)
axi.set_ylim(0, 400)
figi.savefig('Impedance measurament-compare-impedance-protocolornot.png', dpi=600)

# Events_QuickPest = Event(tuple(range(55, 86, 5))*pq.s
#                           ) 

# analysistimes = ((AlphaTime, 'Alpha', None),
#                   (QuickPest, 'Blink', Events_QuickPest),
#                   (JawStrength, 'Jaw', None),
#                   (Basal, 'Basal', None))

# for time, name, event_time in analysistimes:
#     Splt.PlotChannels(time)
#     if event_time is not None:
#         print(event_time)
#         Splt.PlotEvents(event_time, linestyles = 'dotted')
#         Splt.Fig.savefig(name+'.png')
        

# fig,ax = plt.subplots(4,1, sharex='all')
# ax= ax.flatten()
# for ic, c in enumerate(SigsPl):
#     axp = ax[ic]
    
#     axp.set_xlim(0, 125)
#     axp.set_ylabel('PSD [V**2/Hz]')
    
    
#     for time, name, event_time in analysistimes:
#         plot_spectral_density(c, time, Freqs, 1, name,
#                               ax=axp)
#     axp.legend(loc='upper right')
# fig.suptitle('Spectral density')
# ax[-1].set_xlabel('Frequency [Hz]')
# fig.savefig('PSD'+'.png')





    