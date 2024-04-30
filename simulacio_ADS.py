"""
@author: Eva Casals
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import pandas as pd
plt.style.use('default')
#%% Creaóci funció per generar un asenyal modulada AM
def GenAMSignal(t , Fcar , R, Amp) :
    Carr = Amp*np.cos(Fcar*2*np.pi*t ) #es crea la senyal portadora en el nostre cas I=6nA i 
    AMsig = R*Carr
    return AMsig


#%% Creem una funció per demodular la senyal
# Mètode de product detector: injectem una senyal que fa que s'elimini l'ona Carrier i ens quedem amb
# l'ona del missatge
def Demodulation( t , Fs, Fcar2 , AMsig , LFPFreq, Amp) :
    Cdem = 2/(Amp)*(np.cos(Fcar2*2*np.pi*t) + np.sin(Fcar2*2*np.pi*t)*1j)
    Dem = AMsig*Cdem # productori de la senyal AM i una amb la freq de la portadora
    #el resultat és una senyal amn un pic a la FFT al centre i amplitud del missatge 
    Ffilt = LFPFreq/(0.5*Fs) #
    sos = signal.butter( 4 , Ffilt ,'lowpass', output='sos') #creació dels coeficients del filtre
    return signal.sosfiltfilt(sos, Dem, axis=0) #apliquem filtre digital, ens quedem amb la senyal 
    #del missatge
    
    
#%% Definició de els valors de la nostra senyal
plt.close('all')

Fs = 250
Ts = 1/Fs 


Fcar = 31.25
Amp = 6e-6
R = 18e3
fallo=0
Fcar2 = Fcar+fallo
LFPFreq=5


t = np.arange(0, 2.5, Ts) #llargada que tindrà la senyal
AMsig = GenAMSignal(t , Fcar , R, Amp)
Sig = Demodulation( t , Fs, Fcar2 , AMsig, LFPFreq, Amp)

#%% Plot de la senyal que volem demodular
plt.figure()
plt.plot(t, AMsig)
plt.title('AM signal')
plt.xlabel('Time [s]')
plt.ylabel('Amp [V]')
   
#%% FFT de la senyal demodulada vs AM
Fmin = 1
nFFT = int(2**(np.around(np.log2(Fs/Fmin))+1)) #Càlcul de la longitud que ha de tenri la FFT
ff1, psd1 = signal.welch(x=AMsig,fs=Fs,
                       axis=0,
                       nperseg=nFFT,
                       scaling='density',
                    return_onesided=False
                         ) #Càlcul de la FFT

ff2, psd2 = signal.welch(x=Sig,fs=Fs,
                       axis=0,
                       nperseg=nFFT,
                       scaling='density',
                        return_onesided=False)


plt.figure()
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.semilogy(ff1, psd1, color = 'red', label='AMsig')
plt.semilogy(ff2, psd2, color='blue', label='Sig')
plt.xlim(-125,125)
plt.title('Spectral density', fontsize=20, fontweight='bold')
plt.xlabel('Frequency [Hz]', fontsize=16)
plt.legend(fontsize=16)
plt.ylabel('PSD [V**2/Hz]', fontsize=16)
    
    
#%% Plot real-imaginari o modul-fase
fig, (AxR, AxI) = plt.subplots(2, 1, sharex=True)
AxR.plot(t, np.real(Sig), color='blue')  # Color azul para la parte real
AxR.set_ylabel('Real [\u2126]', fontsize=16, color='blue')  # Ajusta tamaño y color de la fuente
AxI.plot(t, np.imag(Sig), color='red')  # Color rojo para la parte imaginaria
AxI.set_ylabel('Imag [\u2126]', fontsize=16, color='red')  # Ajusta tamaño y color de la fuente
AxI.set_xlabel('Time [s]', fontsize=16)

# Título para el primer conjunto de subgráficos
fig.suptitle('Real-imaginary', fontsize=20, fontweight='bold')

# Ajusta los colores de los ejes
for ax in [AxR, AxI]:
    ax.tick_params(axis='both', colors='black', labelsize=12)  # Ajusta tamaño y color de los números de los ejes
    ax.yaxis.label.set_color('black')  # Ajusta color de la etiqueta del eje y

# Plot Magnitud y Fase con colores
fig, (AxM, AxP) = plt.subplots(2, 1, sharex=True)
AxM.plot(t, np.abs(Sig), color='green')  # Color verde para la magnitud
AxM.set_ylabel('Abs [\u2126]', fontsize=16, color='green')  # Ajusta tamaño y color de la fuente
AxP.plot(t, np.angle(Sig, deg=True), color='orange')  # Color naranja para la fase
AxP.set_ylabel('Angle [Deg]', fontsize=16, color='orange')  # Ajusta tamaño y color de la fuente
AxP.set_xlabel('Time [s]', fontsize=16)

# Título para el segundo conjunto de subgráficos
fig.suptitle('Magnitude-phase', fontsize=20, fontweight='bold')

# Ajusta los colores de los ejes
for ax in [AxM, AxP]:
    ax.tick_params(axis='both', colors='black', labelsize=12)  # Ajusta tamaño y color de los números de los ejes
    ax.yaxis.label.set_color('black')  # Ajusta color de la etiqueta del eje y

plt.show()

#%% Diferència entre els valors si es falla amb la freq de mostreig de la senyal injectada
errors = (
            (0, '#333333'),
            (0.1, '#800080'),
            (0.2, '#0000FF'),
            (0.5, '#FF0000'),
            (1, '#FFA500'),
            (2, '#87CEEB'),
            (4,'#98FB98')
            
            )
lines = []  
labels = [] 
fig1, (AxR, AxI) = plt.subplots( 2 , 1 , sharex =True, figsize=(9,20))
fig2 , ( AxM, AxP) = plt.subplots( 2 , 1 , sharex=True, figsize=(9, 20))
for fallo, colors in errors:
    Fcar2 = Fcar+fallo 
    Sig = Demodulation( t , Fs, Fcar2 , AMsig, LFPFreq, Amp)
    lineR, = AxR.plot(t, np.real(Sig), colors)
    lines.append(lineR)  
    labels.append('f real + {} Hz'.format(fallo))
    
    AxI.plot(t, np.imag(Sig), colors)
    
    AxM.plot( t , np.abs(Sig), colors)
    
    
    AxP.plot( t , np.angle( Sig , deg=True), colors )
    

AxR.set_ylabel('Real[\u2126]')
AxI.set_ylabel('Imag [\u2126]')
AxI.set_xlabel('Time[s]')
AxM.set_ylabel(' Abs [\u2126] ')
AxP.set_ylabel('Angle [Deg]')
AxP.set_xlabel('Time [s]')


fig1.legend(lines, labels, loc='center right', fancybox=True, shadow=True, ncol=1)  
fig2.legend(lines, labels, loc='center right', fancybox=True, shadow=True, ncol=1)



fig1.suptitle('Deviation from the Fcar to demodulate (cartesian)', fontsize=20, fontweight='bold')
fig2.suptitle('Deviation from the Fcar to demodulate (trigonometrical)', fontsize=20, fontweight='bold')

# fig1.tight_layout()
# fig2.tight_layout()

fig1.savefig('simu-mismatch-cart.png', dpi=500)


fig2.savefig('simu-mismatch-trig.png', dpi=500)
plt.show()
