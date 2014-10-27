#!/usr/bin/env python
#coding:utf-8
# Author:   --<>
# Purpose: 
# Created: 24/10/14

import numpy as np


class SequentialClearance(object):
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
