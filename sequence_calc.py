#!/usr/bin/env python
#coding:utf-8
# Author:   --<>
# Purpose: 
# Created: 24/10/14

import numpy as np
import math
import cmath

def parallel(x,y):
    
    if abs(x)==0 or abs(y)==0:
        #print('x =0')
        z = 0
    elif (1/x+1/y)==0:
        #print ('Bigger number')
        #print(x,y)
        z= 1000000
    else:
        #print( 'results')
        #print x , y
        z = 1/(1/x+1/y)
    return z

def parallelm(x):
    sum = 0
    for i in x:
        if abs(i)==0:
            z =0
            sum =1
            break
        j = 1.0/i
        sum += j
        
    if sum ==0:
        z = 1000000
    elif sum !=0:
        z= 1.0/(sum)
        
    return z
        

def series(x,y):
    z = x + y
    return z

def seriesm(x):
    sum = 0
    for i in x:
        j = i
        sum += j
    return sum

def c_to_ohms(pf):
    
    if pf ==0:
        return 1000000000000
    else:
        print (pf)
        omega = 2 * math.pi * 50
        z = 1/((pf/1000000000.0) * omega * 1j)
        return z
    
def mva_to_ohms(mva,volts):
    
    #print ('mva', mva)
    
    if mva ==0:
        return 10000
    
    else:
        imp = math.pow(volts,2)/(mva*1000000*3.0)
        phi = math.radians(85)
        
        print(cmath.rect(imp, phi))
        return cmath.rect(imp, phi)        
        
        



class Relay(object):
    def __init__(self):
        self.I1 = 1 + 0j
        self.I2 = 1 +0j
        self.I0 = 1 + 0j
        
        self.V1=0+0j
        self.V2=0+0j
        self.V0=0+0j

        #need to check what the defaults are - confirmed as is.
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
    
    def qualRatios(self):
        a = [self.a0(), self.a2(), self.k2()]
        
       #print('updating ratios')
       #print a
       #print self.I0
        return a
    
    
    
    
    

class Threshold(object):
    def __init__(self):
        pass
    




class SequenceCalcs(object):
    def __init__(self):
        
        self.pv = 33000
        
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
        
        self.testCase()
        
        
        
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
        

    def plotV2(self):
        return cmath.polar(self.relay_flt.V2)
    
    def plotI2(self):
        return cmath.polar(self.relay_flt.I2) 
    
    def plotV0(self):
        return cmath.polar(self.relay_flt.V0)
    
    def plotI0(self):
        return cmath.polar(self.relay_flt.I0)   
    
    def plotV2adj(self):
        return cmath.polar(self.relay_adj.V2)
    
    def plotI2adj(self):
        return cmath.polar(self.relay_adj.I2) 
    
    def plotV0adj(self):
        return cmath.polar(self.relay_adj.V0)
    
    def plotI0adj(self):
        return cmath.polar(self.relay_adj.V0)     
    
   
    def z2_locus(self):
        return (self.relay_flt.z2().real,self.relay_flt.z2().imag)
    
    def z0_locus(self):
        return (self.relay_flt.z0().real,self.relay_flt.z0().imag) 
    
    def z2_locus_adj(self):
        return (self.relay_adj.z2().real,self.relay_adj.z2().imag)
    
    def z0_locus_adj(self):
        return (self.relay_adj.z0().real,self.relay_adj.z0().imag)     
    
    def z2_thresholds(self):
        return [5,2,1],[1,2,5],[-5,-2,-1],[-1,-2,-5]
    
    def z0_thresholds(self):
        return [5,2,1],[1,2,5],[-5,-2,-1],[-1,-2,-5]    
    
    def qualRatio(self):
        return self.relay_flt.qualRatios()
    
    def qualRatio_adj(self):
        return self.relay_adj.qualRatios()    
    
    def updateCalc(self, para, **kwargs):
        
        
        self.R_fault = para["Rf"]
        self.R_NER = para["R_NER"]
        self.cap_line = c_to_ohms(para["CapFaultCct"])
        self.cap_line_adj = c_to_ohms(para["CapAdjacent"])
        
        #Todo
        '''need to resolve that these do not return zero to the calculation below'''
        
        self.z1_load = mva_to_ohms(para["load_flt"],self.pv)
        self.z2_load = mva_to_ohms(para["load_flt"],self.pv)
        
        self.z1_load_adj = mva_to_ohms(para["load_adj"],self.pv)
        self.z2_load_adj = mva_to_ohms(para["load_adj"],self.pv)

        self.calcBranches(self.calcIf())

    def calcIf(self):
        
        print('calcIf called')
        
        self.z1 = parallel((self.z1_src+self.tx1),self.z1_load)
        self.z2 = parallel((self.z2_src+self.tx2),self.z2_load)
        self.z0 = parallel((self.tx0+3*self.R_NER), self.cap_line_adj)
        
        #print(self.tx0,self.R_NER,self.cap_line_adj)
        
        #test

        
        
        If = (self.pv/math.sqrt(3))/(self.z1+self.z2+self.z0+self.R_fault)
        
        #print('If =', str(If))
        
        return If
    
    
    
    def calcBranches(self,If ):
        
        self.relay_flt.V1 = self.z1 * If
        self.relay_flt.V2 = self.z2 * If
        self.relay_flt.V0 = self.z0 * If
        
       #print('If =', str(If))
        
       #print (self.z1, self.z2, self.z0)
        
        
        
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
    
   #print ('app created')
    
    app= SequenceCalcs()
    
    ###populate with dummy variable
    
    app.testCase()
    iIF = app.calcIf()
    app.calcBranches(iIF)
    
    
    
   #print ('debug break point')
    
    


    
    
