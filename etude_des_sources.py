#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 16 11:49:33 2022

@author: andromede
"""

import os
import numpy as np
import soundfile as sf
from soundfile import SoundFile
from scipy import signal
from scipy.fft import fftshift
import matplotlib.pyplot as plt
import librosa
import librosa.display

sources = 'DATA/STIMULI'

 
for fichierSon in os.listdir(sources):
    f = os.path.join(sources, fichierSon)
    if os.path.isfile(f) & (f[-4:]=='.wav') :
        sfSon = SoundFile(f)
        print(f, sfSon.samplerate, sfSon.channels, sfSon.format, sfSon.subtype)
        son = sfSon.read()
        freqEch = sfSon.samplerate
        sfSon.close()
        
        police = 23 # 21 ok
        
        fig1 = plt.figure(f, figsize=(11, 6))
        plt.title(f[13:], fontsize=police)
        plt.xlabel("Temps (s)", fontsize=police)
        plt.ylabel("Amplitude (SU)", fontsize=police)
        durree = 1 # secondes

        
        plt.plot(np.linspace(0,durree, durree*freqEch), son[:freqEch])
        plt.xticks(fontsize=police)
        plt.yticks(fontsize=police)
        plt.tight_layout()
        fig1.savefig( 'figures/'+f[13:-4]+'_PCM'+'.pdf', transparent=True, pad_inches=0.0 )   
        
        # autre methode pour calculer le spectrograme des sources
        # nperseg=8192
        # noverlap = nperseg // 2
        # freqs, t, Sxx = signal.spectrogram(son, freqEch, nperseg=nperseg, noverlap=noverlap) #, nperseg=10, noverlap=1)
        
        # plt.figure()
        # plt.title(f[13:])
        # plt.pcolormesh(t, freqs[1:], np.log10(Sxx[1:,:]), shading='gouraud', cmap= 'inferno')
        # #plt.imshow(np.log10(Sxx[1:,:]))
        # plt.yscale('symlog')

        # window_size = 8192
        # hop_length = 512
        
        # window = np.hanning(window_size)
        # stft= librosa.core.spectrum.stft(son, n_fft = window_size, hop_length = hop_length, window=window)
        # out = 2 * np.abs(stft) / np.sum(window)
        
        # fig2 = plt.figure(f+'spectro', figsize=(11, 6))
        # plt.title(f[13:], fontsize=police)
        # plt.set_cmap('hot')
        # librosa.display.specshow(librosa.amplitude_to_db(out, ref=np.max), y_axis='log', x_axis='time',sr=freqEch)
        # plt.ylabel('Fréquence (Hz)', fontsize=police)
        # plt.xlabel("Temps (s)", fontsize=police)  
        # plt.xticks(fontsize=police)
        # plt.yticks(fontsize=police)
        # plt.tight_layout()
        # fig2.savefig( 'figures/'+f[13:-4]+'_spectrogram.pdf', transparent=True, pad_inches=0.0 )        
            
