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

def parallelm(x):
    sum = 0
    for i in x:
        j = 1.0/i
        sum += j
    return 1.0/(sum)
        

def series(x,y):
    z = x + y
    return z

def seriesm(x):
    sum = 0
    for i in x:
        j = i
        sum += j
    return sum

def c_to_ohms(mf):
    omega = 2 * math.pi * 50
    z = 1/(mf/100000) * omega *1j
    return z

class Relay(object):
    def __init__(self):
        self.I1 = 0 + 0j
        self.I2 = 0 +0j
        self.I0 = 0 + 0j
        
        self.V1=0+0j
        self.V2=0+0j
        self.V0=0+0j

        #need to check what the defaults are
        self.a0_setting = 0.1
        self.a2_setting = 0.2
        self.k2_setting = 0.1
        
        
    def z2(self):
        z = self.V2/self.I2
        return z
    
    def z0(self):
        z=self.V0/self.I0
        return z
    
    def a0(self):
        z = abs(self.I0)/abs(self.I1)
        return z
    
    def a2(self):
        z= abs(self.I2)/abs(self.I1)
        return z
    
    def k2(self):
        z = abs(self.I0)/abs(self.I2)
        return z
    
    
    

class Threshold(object):
    def __init__(self):
        pass
    




class SequenceCalcs(object):
    def __init__(self):
        
        self.R_fault=0
        
        self.z1_src=0+0j
        self.z2_src=0+0j
        
        self.tx1=0+0j
        self.tx2=0+0j
        self.tx0 =0+0j    
        self.R_NER=0+0j 
        
        self.z1_line=0+0j
        self.z2_line=0+0j
        self.z0_line=0+0j
        self.cap_line=0+0j
        self.z1_load=0+0j
        self.z2_load=0+0j

        self.z1_line_adj=0+0j
        self.z2_line_adj=0+0j
        self.z0_line_adj=0+0j
        self.cap_line_adj=0+0j
        self.z1_load_adj=0+0j
        self.z2_load_adj=0+0j
        
        self.relay_flt = Relay()
        self.relay_adj = Relay()
        
        
        
    def testCase(self):
        
        self.R_fault=40
        self.z1_src=0.1+0.5j
        self.z2_src=0.1+0.5j
        
        self.tx1=1+3j
        self.tx2=1+3j
        self.tx0 =1+3j    
        self.R_NER=20+0j 
        
        self.z1_line=1+3j
        self.z2_line=1+3j
        self.z0_line=1+3j
        self.cap_line=0-3700000j
        self.z1_load=10+0j
        self.z2_load=10+0j

        self.z1_line_adj=1+3j
        self.z2_line_adj=1+3j
        self.z0_line_adj=1+3j
        self.cap_line_adj=0.1-1000000j
        self.z1_load_adj=10+0j
        self.z2_load_adj=10+0j        
        

    
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
    
    def calcIf(self,v1):
        
        self.z1 = parallel((self.z1_src+self.tx1),self.z1_load)
        self.z2 = parallel((self.z2_src+self.tx2),self.z2_load)
        self.z0 = parallel((self.tx0+3*self.R_NER), self.cap_line_adj)
        
        If = (v1/math.sqrt(3))/(self.z1+self.z2+self.z0+self.R_fault)
        
        return If
    
    def calcBranches(self,If ):
        
        self.relay_flt.V1 = self.z1 * If
        self.relay_flt.V2 = self.z2 * If
        self.relay_flt.V0 = self.z0 * If
        
        self.relay_flt.I1 = self.relay_flt.V1/(self.z1_src+self.tx1)
        self.relay_flt.I2 = self.relay_flt.V2/(self.z2_src+self.tx2)
        self.relay_flt.I0 = self.relay_flt.V0/(self.tx1+3*self.R_NER)
        
        self.relay_adj.V1 = self.z1 * If
        self.relay_adj.V2 = self.z2 * If
        self.relay_adj.V0 = self.z0 * If      
        
        self.relay_adj.I1 = self.relay_adj.V1/(self.z1_line_adj+parallel(self.z1_load_adj, self.cap_line_adj))
        self.relay_adj.I2 = self.relay_adj.V2/(self.z2_line_adj+parallel(self.z2_load_adj, self.cap_line_adj))
        self.relay_adj.I0 = self.relay_adj.V0/(self.z0_line_adj+self.cap_line_adj)        
    
    
if __name__=='__main__':
    
    print ('app created')
    
    app= SequenceCalcs()
    
    ###populate with dummy variable
    
    app.testCase()
    iIF = app.calcIf(33000)
    app.calcBranches(iIF)
    
    
    
    print ('debug break point')
    
    


    
    
