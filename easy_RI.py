#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 15 08:02:13 2022

@author: louisgenieyspoux
"""

import soundfile as sf
from soundfile import SoundFile
import numpy as np
import os

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
    
    print("\n... Ouverture de " + stim_str + "\n")
    print("\t",os.path.basename( stim_str ), ":")
    print("\t\t\tfe={}Hz,\n \t\t\tcanals={},\n \t\t\ttype={}bits".format(
         sfStim.samplerate, sfStim.channels, sfStim.subtype))

    print("\n... Ouverture de " + rep_str + "\n")
    print("\t",os.path.basename( rep_str ), ":")
    print("\t\t\tfe={}Hz,\n \t\t\tcanals={},\n \t\t\ttype={}bits".format(
         sfRep.samplerate, sfRep.channels, sfRep.subtype))  
    
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
    import sys

    stim = sys.argv[1]
    rep = sys.argv[2]
    
    ri_L, ri_R = calcule_RI_classic_stereo(stim, rep)
    
    ir_stereo = np.array([np.array([ri_L[i], ri_R[i]]) for i in range(len(ri_L))])
    
    # ir_stereo = ir_stereo[0:int(len(ir_stereo)//4),:] # si on veut raccourir la RI ...
    
    len_fade = len(ir_stereo)//2
    
    x = np.linspace(np.pi/2,np.pi,len_fade)
    fade = np.cos(x) + 1
    
    ir_stereo[len_fade:-1,0] *= fade
    ir_stereo[len_fade:-1,1] *= fade
    
    sf.write(os.path.basename(rep[:-4])+"_IR.wav", ir_stereo, 44100, 'PCM_24')
    print("\n ", os.path.basename(rep[:-4])+"_IR.wav", " écrit !\n")