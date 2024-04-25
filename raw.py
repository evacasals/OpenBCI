from Helpers import *
import matplotlib.pyplot as plt
import matplotlib as mpl
from PhyREC import SignalProcess as Spro
from PhyREC import PlotWaves as Rplt
from collections import OrderedDict
import math
colors = plt.cm.tab10.colors
plt.style.use('MyStyle.mplstyle')
mpl.use('Qt5Agg')
#
excel = pd.read_excel('experiments/data.xlsx', sheet_name='experiments')
file_label = dict(zip(excel['name'], excel['label']))
FileIn = 'experiments/20240423_6.txt'

Sigs = read_file_oBCI(FileIn,
                      colors=colors)
Sigs_ECG = [Sigs[i] for i in [0, 2]]
#%% Filters
NonFilt = [{'function': Spro.Filter, 'args': {'Type': 'highpass',
                                                       'Order': 4,
                                                       'Freqs': (1,)}}, ]
Filt50 = [
          # {'function': Spro.SetZero, 'args': {'TWind': (5 * pq.s, 6* pq.s)}},
          # {'function': Spro.Filter, 'args': {'Type': 'bandstop',
          #                                    'Order': 4,
          #                                    'Freqs': (49.5, 50)}},
          ]


# Axes properties
Ax50 = {
    'ylim': (-1, 1),
    'facecolor': '#FFFFFF00',
    'autoscaley_on': True,
    'xaxis': {'visible': False,
              },
    'yaxis': {'visible': True,
              },
}
AxNoFilt = {
    'ylim': (-0.2, 0.2),
    'facecolor': '#FFFFFF00',
    'autoscaley_on': True,
    'xaxis': {'visible': False,
              },
    'yaxis': {'visible': True,
              },
}


Procs = (
    {'ProcesChain': Filt50,
     'SlotFunc': Rplt.WaveSlot,
     'TwinAx': False,
     'SigSufix': 'FB',
     'FunctionKwarg': {'Units': 'mV',
                       'color': 'k',
                       # 'linewidth': 1,
                       'alpha': 1,
                       'AxKwargs': Ax50,
                       'clip_on': False,
                       }
     },
     {'ProcesChain': NonFilt,
      'SlotFunc': Rplt.WaveSlot,
      'TwinAx': True,
      'SigSufix': 'NonFilt',
      'FunctionKwarg': {'Units': 'mV',
                        'color': 'auto',
                        'alpha': 1,
                        'AxKwargs': AxNoFilt,
                        'clip_on': False,
                        }
     }
)
#%% Figures
SlotsECG, Fig, AxsNoFilt = GenSlots(Sigs_ECG, Procs)

#%%
SpltECG = Rplt.PlotSlots(SlotsECG,
                         Fig=Fig,
                         LiveControl=True,
                         TimeAxis=-1,
                         )

SpltECG.PlotChannels(Time=(5*pq.s, None))
AxsNoFilt[0].set_xlabel('Time [s]', fontsize=14)
AxsNoFilt[0].set_ylabel('Voltage [mV]', fontsize=14)
AxsNoFilt[1].set_ylabel('Voltage [mV]', fontsize=14)
fig.suptitle('No Bias and GND')