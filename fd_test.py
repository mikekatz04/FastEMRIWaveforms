#%%
from few.waveform import FastSchwarzschildEccentricFlux, RunSchwarzEccFluxInspiral
from few.utils.utility import *
from few.utils.constants import *
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal


sum_kwargs = dict(pad_output=True)

few_base = FastSchwarzschildEccentricFlux(
    sum_kwargs=sum_kwargs,
)
# p0=12;e0=0.3 -> mismatch =  0.000778239562794103

M = 1e6; mu = 40; p0 = 10; e0 = 0.7; theta= np.pi/3; phi = np.pi/5 # mismatch =  0.0014153820095872405

#M = 1e6; mu = 50; p0 = 11.48; e0 = 0.7; theta= np.pi/3; phi = np.pi/5 # mismatch =  0.02257016504821807

traj_module = RunSchwarzEccFluxInspiral()

traj_args = [M, p0, e0]
traj_kwargs = {}
index_of_mu = 1

t_out = 1.
# run trajectory
mu = get_mu_at_t(traj_module, t_out, traj_args)
print(mu)
# mism 0.0024275870323797744
dt=10
T=1.


l=2 #2
m=2 #1
n=2 #-4

#%% TIME DOMAIN
wave_22 = few_base(M, mu, p0, e0, theta, phi,T=T,dt=dt,mode_selection=[(l,m,n)],include_minus_m=True) #,eps=1e-2)# 
freq_fft = np.fft.fftfreq(len(wave_22),dt)
fft_wave = np.fft.fft(wave_22 )*dt #* signal.tukey(len(wave_22))

rect_fft = np.fft.fft(np.ones_like(wave_22)) #* signal.tukey(len(wave_22))


sum_kwargs = dict(pad_output=True, output_type="fd")

wave = FastSchwarzschildEccentricFlux(sum_kwargs=sum_kwargs)

fd_h = wave(M,mu,p0,e0,theta,phi,T=T,dt=dt,mode_selection=[(l,m,n)],include_minus_m=True) #,eps=1e-2)# , mode_selection=[(l,m,n)],include_minus_m=True) #

f = np.arange(-1/(2*dt),+1/(2*dt),1/(len(fd_h)*dt))


#%% mismatch
print("nans in waveform", np.sum(np.isnan(fd_h)))

fd_h_correct = -np.roll( np.flip(np.real(fd_h)) + 1j* np.flip(np.imag(fd_h)), 1)#np.sin(dt*len(wave_22)*freq_fft/4/np.pi)/np.sin(dt*freq_fft/4/np.pi)#*np.exp(-1j* (len(wave_22)-1)/2 )
index_nonzero = [np.abs(fd_h_correct) !=complex(0.0)][0]

# check nan

den = np.sqrt(np.real(np.dot(np.conj(fft_wave[index_nonzero]),fft_wave[index_nonzero])) * np.real(np.dot(np.conj(fd_h_correct[index_nonzero]),fd_h_correct[index_nonzero])) )
print('den',den,'index',np.sum(index_nonzero))
print("mismatch = " ,1-np.real(np.dot(np.conj(fd_h_correct[index_nonzero]) , fft_wave[index_nonzero] ) )/den)

den = np.sqrt(np.real(np.dot(np.conj(fft_wave[index_nonzero]),fft_wave[index_nonzero])) * np.real(np.dot(np.conj(fd_h_correct[index_nonzero]),fd_h_correct[index_nonzero])) )
print('den',den,'index',np.sum(index_nonzero))
print("mismatch = " ,1-np.real(np.dot(np.abs(fd_h_correct[index_nonzero]) , np.abs(fft_wave[index_nonzero]) ) )/den)


# np.dot(np.real(fft_wave),-np.real(fd_h)) + np.dot(np.imag(fft_wave),-np.imag(fd_h))
"""
# figure
plt.figure()
plt.ylabel(r'Re $\tilde{h}(f)$')
plt.xlabel('f [Hz]')
# TD model
plt.plot(freq_fft, np.real(fft_wave), label='fft TD waveform')
# FD model
plt.plot(freq_fft, np.real(fd_h_correct),'--',alpha=0.9,label='FD domain waveform' )
plt.legend(loc='right')
plt.show()


# %%


# figure
plt.figure()
plt.ylabel(r'Imag $\tilde{h}(f)$')
plt.xlabel('f [Hz]')
# TD model
plt.plot(freq_fft, np.imag(fft_wave), label='fft TD waveform')
# FD model
plt.plot(freq_fft, np.imag(fd_h_correct),'--',alpha=0.9,label='FD domain waveform' )
plt.legend()
plt.show()
"""
# %%

# figure
plt.figure()
plt.ylabel(r'Ang $\tilde{h}(f)$')
plt.xlabel('f [Hz]')
# TD model
plt.plot(freq_fft, np.angle(fft_wave), label='fft TD waveform')
# FD model
plt.plot(freq_fft, np.angle(fd_h_correct),'--',alpha=0.9,label='FD domain waveform' )
plt.legend()
plt.show()


# figure
plt.figure()
plt.ylabel(r' $|\tilde{h}(f)|$')
plt.xlabel('f [Hz]')
# TD model
plt.plot(freq_fft, np.abs(fft_wave), label='fft TD waveform')
# FD model
plt.plot(freq_fft, np.abs(fd_h_correct),'--',alpha=0.9,label='FD domain waveform' )
plt.legend()
plt.show()