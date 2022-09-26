#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 15 08:02:13 2022

@author: andromede
"""

import soundfile as sf
from soundfile import SoundFile

import numpy as np
import matplotlib.pyplot as plt

import os
from scipy.signal import savgol_filter


def calcule_RI_classic_mono(stim_str, rep_str) :
    """ Calcule la réponse impulsionnelle en prenant en entree un stimulus mono
    et la reponse en mono
    
    Parameters
    ----------
    stim : STR
        repertoire du fichier .wav de la stimulation
    rep : STR
        repertoire du fichier .wav de la reponse enregistree

    Returns
    -------
    ri : réponse en PCM
    """
    
    sfStim = SoundFile(stim_str)
    sfRep = SoundFile(rep_str)
    
    print("Ouverture de {}, fe={}Hz, canals={}, type={}bits".format(
        stim_str, sfStim.samplerate, sfStim.channels, sfStim.subtype))
    print("Ouverture de {}, fe={}Hz, canals={}, type={}bits".format(
        rep_str, sfRep.samplerate, sfRep.channels, sfRep.subtype))  
    
    if sfStim.samplerate != sfRep.samplerate :
        raise ValueError(
            'La frequence du stimulus : {}Hz ne correspond pas a celle de la reponse : {}Hz'.format(
            sfStim.samplerate,sfRep.samplerate))
        
    if sfRep.channels != 1 :
        raise ValueError(
            "Le fichier de la reponse doit etre mono. \n channels={} or il faut channels=1.".format(
                sfRep.channels))
        
    stim = sfStim.read()
    rep = sfRep.read()
    
    freqEch = sfStim.samplerate
    
    sfStim.close(); sfRep.close()
    
    
    # ========================================================================
    #     fade in et out sur la reponse de la salle
    # ========================================================================

    fadeLen = int(0.005 * freqEch) # 5ms
    
    fadeIn = np.linspace(0,1,fadeLen)
    fadeOut = np.linspace(1,0,fadeLen)
    
    rep[0:fadeLen] *= fadeIn
    rep[-fadeLen:] *= fadeOut 
    
    # ========================================================================
    #     calcul des fft
    # ========================================================================
  
    stimFft = np.fft.fft(stim,len(rep))
    
    rep_fft = np.fft.fft(rep)
    
    h = rep_fft/stimFft #fonction de transfert
    
    police = 23 # 21 ok
    
    fig1 = plt.figure(os.path.basename( rep_str ), figsize=(11, 5))
    plt.title("Fonction de transfert gauche",fontsize=police)
    
    h_Plot = h[1000:int(len(h)*0.5)]
    # h_L_Plot *= 1/np.max(np.abs(h_L_Plot))
    
    x = np.linspace(0,freqEch/2,len(h_Plot))
    y = 20*np.log10(np.abs(h_Plot)**2)
    yhat = savgol_filter(y, 11, 3)
    
    yhat *= np.abs(1/np.max(yhat))
    
    plt.plot(x, yhat)
    plt.xscale('log')
    plt.xlim(50,20000)
    plt.ylim([-18,0])
    plt.xlabel('Fréquence (Hz)',fontsize=police)
    plt.ylabel('Amplitude (log)',fontsize=police)
    
    plt.xticks(fontsize=police)
    plt.yticks(fontsize=police)
    plt.tight_layout()
    fig1.savefig( 'figures/transfert/'+os.path.basename( rep_str )+'_fctrans'+'.pdf', transparent=True, pad_inches=0.0 )   
    
    ri = np.real(np.fft.ifft(h)) # reponse impulsionnelle
    
    norm = np.max([np.max(np.abs(ri))])

    ri *= 1/norm  # on normalise !
        
    return ri


def calcule_RI_classic_stereo(stim_str, rep_str) :
    """ Calcule la réponse impulsionnelle en prenant en entree un stimulus mono
    et la reponse en stereo
    
    Parameters
    ----------
    stim : STR
        repertoire du fichier .wav de la stimulation
    rep : STR
        repertoire du fichier .wav de la reponse enregistree

    Returns
    -------
    (ri_L, ri_R) : TUPLE (float64)
            reponse gauche et droite en PCM
    """
    
    sfStim = SoundFile(stim_str)
    sfRep = SoundFile(rep_str)
    
    print("Ouverture de {}, fe={}Hz, canals={}, type={}bits".format(
        stim_str, sfStim.samplerate, sfStim.channels, sfStim.subtype))
    print("Ouverture de {}, fe={}Hz, canals={}, type={}bits".format(
        rep_str, sfRep.samplerate, sfRep.channels, sfRep.subtype))  
    
    if sfStim.samplerate != sfRep.samplerate :
        raise ValueError(
            'La frequence du stimulus : {}Hz ne correspond pas a celle de la reponse : {}Hz'.format(
            sfStim.samplerate,sfRep.samplerate))
        
    if sfRep.channels != 2 :
        raise ValueError(
            "Le fichier de la reponse doit etre stereo. \n channels={} or il faut channels=2.".format(
                sfRep.channels))
        
    stim = sfStim.read()
    rep = sfRep.read()
    
    freqEch = sfStim.samplerate
    
    sfStim.close(); sfRep.close()
    
    repL = rep[:,0] #gauche
    repR = rep[:,1] #droite
    
    # ========================================================================
    #     fade in et out sur la reponse de la salle
    # ========================================================================

    fadeLen = int(0.005 * freqEch) # 5ms
    
    fadeIn = np.linspace(0,1,fadeLen)
    fadeOut = np.linspace(1,0,fadeLen)
    
    repL[0:fadeLen] *= fadeIn
    repR[0:fadeLen] *= fadeIn
    repL[-fadeLen:] *= fadeOut 
    repR[-fadeLen:] *= fadeOut   
    
    # ========================================================================
    #     calcul des fft
    # ========================================================================
  
    stimFft = np.fft.fft(stim,len(rep))
    
    repL_fft = np.fft.fft(repL)
    repR_fft = np.fft.fft(repR)
    
    h_L = repL_fft/stimFft #fonction de transfert
    h_R = repR_fft/stimFft
    
    police = 23 # 21 ok
    
    fig1 = plt.figure(os.path.basename( rep_str ), figsize=(11, 5))
    plt.title("Fonction de transfert gauche",fontsize=police)
    
    h_L_Plot = h_L[1000:int(len(h_L)*0.5)]
    # h_L_Plot *= 1/np.max(np.abs(h_L_Plot))
    
    x = np.linspace(0,freqEch/2,len(h_L_Plot))
    y = 20*np.log10(np.abs(h_L_Plot)**2)
    yhat = savgol_filter(y, 11, 3)
    
    yhat *= np.abs(1/np.max(yhat))
    
    plt.plot(x, yhat)
    plt.xscale('log')
    plt.xlim(50,20000)
    plt.ylim([-18,0])
    plt.xlabel('Fréquence (Hz)',fontsize=police)
    plt.ylabel('Amplitude (log)',fontsize=police)
    
    plt.xticks(fontsize=police)
    plt.yticks(fontsize=police)
    plt.tight_layout()
    fig1.savefig( 'figures/transfert/'+os.path.basename( rep_str )+'_fctrans'+'.pdf', transparent=True, pad_inches=0.0 )   

    
    
    ri_L = np.real(np.fft.ifft(h_L)) # reponse impulsionnelle
    ri_R = np.real(np.fft.ifft(h_R))
    
    norm = np.max([np.max(np.abs(ri_L)), np.max(np.abs(ri_R))])

    ri_L *= 1/norm  # on normalise !
    ri_R *= 1/norm 
        
    return ri_L, ri_R

# ============================================================================
# ============================================================================

# plotter les fonctions de transfert

if __name__ == '__main__':
    
    
    stim = 'DATA/STIMULI/SW3.wav'
    rep = 'DATA/REC_NEF_RI/OMNI_SW3_NEAR.wav'
    
    # stim = 'DATA_SUPPLEMENTAIRE/STIMULI/SWEEP.wav'
    # rep = 'DATA_SUPPLEMENTAIRE/REC_LL_AMBI/SWEEP_4.wav'
    
    # ri = calcule_RI_classic_mono(stim, rep)
    
    # ir = np.array(ri)
    
    # len_fade = len(ir)//2
    
    ri_L, ri_R = calcule_RI_classic_stereo(stim, rep)
    
    ir_stereo = np.array([np.array([ri_L[i], ri_R[i]]) for i in range(len(ri_L))])
    
    # ir_stereo = ir_stereo[0:int(len(ir_stereo)//4),:] # si on veut raccourir la RI ...
    
    len_fade = len(ir_stereo)//2
    
    x = np.linspace(np.pi/2,np.pi,len_fade)
    fade = np.cos(x) + 1
    
    # plt.figure()
    # plt.plot(ir_stereo)
    
    ir_stereo[len_fade:-1,0] *= fade
    ir_stereo[len_fade:-1,1] *= fade
    
    # plt.figure()
    # plt.plot(ir_stereo[:,0])
    
    # plt.figure()
    # plt.plot(ir_stereo[:,1])
    
    # sf.write('RI_4.wav', ir, 44100, 'PCM_24')
    
    sf.write('testRI1.wav', ir_stereo, 44100, 'PCM_24')