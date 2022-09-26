#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 15 18:18:55 2022

@author: andromede
"""

import os
from soundfile import SoundFile

stimulis = 'DATA/STIMULI'
reponses = 'DATA/REC_NEF_RI'

directory = reponses
 
for fichier_son in os.listdir(directory):
    f = os.path.join(directory, fichier_son)
    if os.path.isfile(f) & (f[-4:]=='.wav'):
        son = SoundFile(f)
        print(f, son.samplerate, son.channels, son.format, son.subtype)
        son.close()
