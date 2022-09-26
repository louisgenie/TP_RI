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

directory = repertoires['stimulis']


for fichier_son in os.listdir(directory):
    f = os.path.join(directory, fichier_son)
    if os.path.isfile(f) & (f[-4:]=='.wav'):
        
        stim_str = f
        ri_str = repertoires['ri'] + '/' + ''
        
        rep_str = repertoires['reponses'] + '/' + 'OMNI_' + f[13:-4] + '_NEAR' + '.wav'
             
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
        
# =============================================================================
#         CONVO
# =============================================================================

# work in progress

        # gauche, droite = calcule_convol_mono_to_stereo(stim_str, 'RI.wav')
        
        # norme = np.max([np.max(np.abs(gauche)), np.max(np.abs(droite)) ])
        # gauche *= 1/norme
        # droite *= 1/norme
        
        # fichier_stereo = np.array([np.array([gauche[i], droite[i]]) for i in range(len(gauche))])
        
        # sf.write(repertoires['conv'] + '/' + 'CONVOLUED_'+ stim_str[13:-4] +'.wav', fichier_stereo, 44100, 'PCM_24')
        
        




    
