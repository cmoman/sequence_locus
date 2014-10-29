#!/usr/bin/env python
#coding:utf-8
# Author:   --<>
# Purpose: 
# Created: 24/10/14

import numpy as np
import math
import cmath

def parallel(x,y):
    z = 1/(1/x+1/y)
    return z

def series(x,y):
    z = x + y
    return z

def c_to_ohms(mf):
    omega = 2 * math.pi * 50
    z = 1/(mf/100000) * omega *1j
    return z
    




class SequenceCalcs(object):
    def __init__(self):
        self.x = 0
        self.y = 0

    def calc(self,a,b):
        self.x = np.array([1,3,5,7])*a
        self.y= np.array([2,5,6,7])*b

    def result1(self):
        return self.x,self.y
    
    def result2(self):
        return list(self.y),list(self.x )  
    
    def z2_locus(self):
        return 1,1
    
    def z2_thresholds(self):
        return [5,2,1],[1,2,5],[-5,-2,-1],[-1,-2,-5]
