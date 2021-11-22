# -*- coding: utf-8 -*-
"""
Created on Wed Sep 29 15:18:17 2021

@author: Sylgi
"""

import numpy as np
import matplotlib.pyplot as plt
from itertools import chain, combinations

def moyenne_std_median(liste):
    return np.mean(liste),np.std(liste),np.median(liste)

def histo(liste):
    plt.hist(liste)
    
def powerset(iterable):
    s = list(iterable)
    powersett = chain.from_iterable(combinations(s, r) for r in range(len(s)+1))
    return powersett




