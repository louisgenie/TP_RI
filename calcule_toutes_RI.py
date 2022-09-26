#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 16 00:04:57 2022

@author: andromede
"""

import os
from calcule_RI import calcule_RI_classic_stereo
import numpy as np
import soundfile as sf


repertoires = {
    'stimulis' : 'DATA/STIMULI',
    'reponses' : 'DATA/REC_NEF_RI',
    'ri' : 'RI_OBTENUES',
    'conv' : 'SONS_CONVOLUES'}

enceintes = {
    'near' : 'NEAR',
    'far' : 'FAR', 
    }

micros = {
    'omni' : 'OMNI',
    'ambi' : 'AMBI'}

directory = repertoires['stimulis']
enceinte = enceintes['near']
micro = micros['omni']



for fichier_son in os.listdir(directory):
    f = os.path.join(directory, fichier_son)
    if os.path.isfile(f) & (f[-4:]=='.wav'):
        
        stim_str = f
        
        rep_str = repertoires['reponses'] + '/' + micro + '_' + f[13:-4] + '_' + enceinte + '.wav'
             
        ri_L, ri_R = calcule_RI_classic_stereo(stim_str, rep_str)
       
        ir_stereo = np.array([np.array([ri_L[i], ri_R[i]]) for i in range(len(ri_L))])
        
        # =====================================================================
        #         Fading
        # =====================================================================
        len_fade = int(len(ir_stereo)*0.5) - 1
        
        x = np.linspace(np.pi/2,np.pi,len_fade)
        fade = np.cos(x) + 1
        
        ir_stereo[(len(ir_stereo[:,0])-len_fade):,0] *= fade
        ir_stereo[(len(ir_stereo[:,0])-len_fade):,1] *= fade

        # sf.write(repertoires['ri'] + '/' +  'RI_' + stim_str[13:-4] + '_' + micro + '_' + enceinte + '.wav', ir_stereo, 44100, 'PCM_24')
        