#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 16 00:49:44 2022

@author: andromede
"""

import numpy as np
import soundfile as sf
from soundfile import SoundFile
from scipy import signal
import os


def calcule_convol_mono_to_stereo(son_str, ri_str):
    """Convolue un son avec un RI
    
        Parameters
    ----------
    son : STR
        repertoire du fichier son .wav
    ri : STR
        repertoire du fichier ri .wav

    Returns
    -------
    (res_L, res_R) : TUPLE (float64)
            resultat de la convolution gauche et droite en PCM
    """
        
    sf_son = SoundFile(son_str)
    sf_ri = SoundFile(ri_str)
    
    print("Ouverture de {}, fe={}Hz, canals={}, type={}bits".format(
        son_str, sf_son.samplerate, sf_son.channels, sf_son.subtype))
    print("Ouverture de {}, fe={}Hz, canals={}, type={}bits".format(
        ri_str, sf_ri.samplerate, sf_ri.channels, sf_ri.subtype))  
    
    if sf_son.samplerate != sf_ri.samplerate :
        raise ValueError(
            'La frequence du son: {}Hz ne correspond pas a celle de la ri : {}Hz'.format(
            sf_son.samplerate,sf_ri.samplerate))
    if sf_ri.channels != 2 : 
        raise ValueError(
            "Le fichier de la ri doit etre stereo. \n channels={} or il faut channels=2.".format(
                sf_ri.channels))

    son = sf_son.read()
    ri = sf_ri.read()
    
    # freq_ech = sf_ri.samplerate
    
    sf_son.close(); sf_ri.close()
    ri_L = ri[:,0]
    ri_R= ri[:,1]
    
    if (len(son) < len(ri[:,0])):
        son = np.pad(son, (0,(len(ri[:,0])-len(son))), 'constant')
    else :
        ri_L = np.pad(ri[:,0], (0,len(son)-len(ri[:,0])))
        ri_R = np.pad(ri[:,1], (0,len(son)-len(ri[:,1])))
        
    res_L = signal.fftconvolve(son, ri_L)
    res_R = signal.fftconvolve(son, ri_R)
    
    return res_L, res_R

# ============================================================================
# ============================================================================

if __name__ == '__main__':
    
    son_a_convo = 'SONS_A_CONVOLUER/kickSnare.wav'
    
    gauche, droite = calcule_convol_mono_to_stereo(
        son_a_convo,
        'RI_OBTENUES/RI_SW15.wav')
    
    norme = np.max([np.max(np.abs(gauche)), np.max(np.abs(droite)) ])
    gauche *= 1/norme
    droite *= 1/norme
    
    fichier_stereo = np.array([np.array(
        [gauche[i], droite[i]]) for i in range(len(gauche))])

    sf.write('SONS_CONVOLUES/'+os.path.basename(son_a_convo),
             fichier_stereo, 44100, 'PCM_24')