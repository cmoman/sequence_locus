#!/usr/bin/env python
#coding:utf-8
# Author:   --<>
# Purpose: 
# Created: 24/10/14

import sys
import unittest
import numpy as np
import cmath

from PyQt4 import QtCore, QtGui, QtSvg

from PyQt4.QtCore import pyqtSignal, pyqtSlot

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
from matplotlib.figure import Figure

from sequence_calc import SequenceCalcs



class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow,self).__init__(parent)
        
        widget = MainWidget()
        self.setCentralWidget(widget)
        self.setWindowTitle('Calculations')
        
        bar = self.statusBar()
        
class MplCanvas(FigureCanvas):
    def __init__(self,nplots):
        self.fig = Figure()
        super(MplCanvas, self).__init__(self.fig)
        if nplots ==1:
            self.ax1 = self.fig.add_subplot(111)
        elif nplots ==2:
            self.ax1 = self.fig.add_subplot(1,2,1)
            self.ax2 = self.fig.add_subplot(1,2,2) 
        elif nplots ==4:
            self.ax1 = self.fig.add_subplot(2,2,1)
            self.ax2 = self.fig.add_subplot(2,2,2)
            self.ax3 = self.fig.add_subplot(2,2,3)
            self.ax4 = self.fig.add_subplot(2,2,4)
        elif nplots ==6:
            self.ax1 = self.fig.add_subplot(3,2,1)
            self.ax2 = self.fig.add_subplot(3,2,2, projection = 'polar')
            self.ax3 = self.fig.add_subplot(3,2,3)
            self.ax4 = self.fig.add_subplot(3,2,4, projection = 'polar')        
            self.ax5 = self.fig.add_subplot(3,2,5)
            self.ax6 = self.fig.add_subplot(3,2,6, projection = 'polar')      
            
        elif nplots ==10:
            self.z2_flt = self.fig.add_subplot(2,5,1)    
            self.z0_flt = self.fig.add_subplot(2,5,2) 
            self.V2V0_flt = self.fig.add_subplot(2,5,3, projection = 'polar')
            self.I2I0_flt = self.fig.add_subplot(2,5,4, projection = 'polar')   
            self.thresh_flt = self.fig.add_subplot(2,5,5)
            
            self.z2_adj= self.fig.add_subplot(2,5,6)
            self.z0_adj = self.fig.add_subplot(2,5,7)
            self.V2V0_adj= self.fig.add_subplot(2,5,8, projection = 'polar') 
            self.I2I0_adj = self.fig.add_subplot(2,5,9, projection = 'polar')
            self.thresh_adj = self.fig.add_subplot(2,5,10)   
            
            
def adjust_spines(ax):
    ax.spines['left'].set_position('zero')
    ax.spines['right'].set_color('none')
    ax.spines['bottom'].set_position('zero')
    ax.spines['top'].set_color('none')
    ax.spines['left'].set_smart_bounds(True)
    ax.spines['bottom'].set_smart_bounds(True)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.grid(True)
            
            
class MplWidget(QtGui.QWidget):
    def __init__(self,nplots):
        super(MplWidget, self).__init__()
        
        self.canvas = MplCanvas(nplots)
        self.vbl = QtGui.QVBoxLayout()
        self.vbl.addWidget(self.canvas)
        
        self.ntp = NavigationToolbar(self.canvas,self)
        self.vbl.addWidget(self.ntp)        
        
        self.setLayout(self.vbl)
        
class ControlDial(QtGui.QDial):
    '''This was/is experimental.  It may still have a role to play in the formatting of the dials'''
    def __init__(self, parent, size):
        super(ControlDial, self).__init__()
        self.setMaximumSize(size)

        
class InputDial(QtGui.QWidget):
    
    valueChanged =pyqtSignal()
    
    def __init__(self, name, tooltip=None, min=0, max=100, radioB = False):
        super(InputDial, self).__init__()
        self.setToolTip(tooltip)
        self.objectName=name
        self.layout = QtGui.QVBoxLayout()
        self.label = QtGui.QLabel(name)
        
        self.dial = ControlDial(self, QtCore.QSize(50,50))
        #self.dial = QtGui.QDial()
        self.dial.setMinimum(min)
        self.dial.setMaximum(max)
        
        self.spinBox = QtGui.QSpinBox()
        self.spinBox.setMinimum(min)
        self.spinBox.setMaximum(max)
        self.spinBox.setValue(1)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.dial)
        self.layout.addWidget(self.spinBox)
        self.connect(self.dial, QtCore.SIGNAL('valueChanged(int)'), self.spinBox, QtCore.SLOT('setValue(int)'))
        
        self.connect(self.spinBox, QtCore.SIGNAL('valueChanged(int)'), self.valueChange)
        
        if radioB == True:
            self.radioButton = QtGui.QRadioButton('select to fix')
            self.layout.addWidget(self.radioButton)
        
        self.setLayout(self.layout)
        
        self.setFixedSize(150,150) # this works
        
        self.setMaximumSize(150,150) # this 
        
    def value(self):
        return self.dial.value()
    
    def setValue(self, value):
        self.spinBox.setValue(value)
        
        
        
    def valueChange(self):
        
        #print('emit signal')

        self.valueChanged.emit()

    

        

        
        
        
class MainWidget(QtGui.QWidget):
    def __init__(self):
        super(MainWidget, self).__init__()
        
        #instantiate calculation class
        
        self.calc = SequenceCalcs()
        
        self.calc.testCase()


        self.widget1 = MplWidget(10)
        self.widget2 = MplWidget(10)
        
        self.widget2.hide()
        
        self.layout = QtGui.QVBoxLayout()
        self.layout.addWidget(self.widget1)
        self.layout.addWidget(self.widget2)
        
        self.textbox=QtGui.QTextEdit()
        #self.layout.addWidget(self.textbox)
        
        self.pushButton = QtGui.QPushButton("push to clear")
        self.layout.addWidget(self.pushButton)
        
        self.pushButton2 = QtGui.QPushButton('push to calculate')
        self.layout.addWidget(self.pushButton2)
        
        layoutdials = QtGui.QHBoxLayout()
        
        self.Rf = InputDial('Fault Resistance', 'Ohms', 0, 400)
    
        self.R_NER = InputDial('NER', 'Neutral Earthing Resistor in ohms', 1, 50)
        #self.R_NER.setMaximumSize(150,150)
        self.CapFaultCct = InputDial('Cap Faulted Cct', 'circuit capacitance in microfarads', 1, 500)
        self.CapAdjacent = InputDial('Cap adjacent', 'Sum of adjacent circuits capacitance in microfarads', 1, 500)
        self.relay_flt = InputDial('3I0 current Relay in Fault Cct', 'Current seen by relay of faulted circuit', 1, 10000, True)
        self.relay_adj= InputDial('3I0 current Relay Adjacent', 'Current seen by relay adjacent to faulted circuit', 1, 10000, True)
        
        layoutdials.addWidget(self.Rf)
        layoutdials.addWidget(self.R_NER)
        layoutdials.addWidget(self.CapFaultCct)
        layoutdials.addWidget(self.CapAdjacent)
        layoutdials.addWidget(self.relay_flt)
        layoutdials.addWidget(self.relay_adj)
        
        self.layout.addLayout(layoutdials)

        self.setLayout(self.layout)
        
        self.updateGraphs()

        self.pushButton2.clicked.connect(self.doCalculation)
        
        # It is possible to create a static method or class methods that emits a signal
        # Decorator perhaps.
        
        self.connect(self.R_NER, QtCore.SIGNAL('valueChanged()'), self.doCalculation)
        self.connect(self.Rf, QtCore.SIGNAL('valueChanged()'), self.doCalculation)
        self.connect(self.CapFaultCct, QtCore.SIGNAL('valueChanged()'), self.doCalculation)
        self.connect(self.CapAdjacent, QtCore.SIGNAL('valueChanged()'), self.doCalculation)
        
        

        

    def updateNER(self):
        #self.calc.R_NER= self.R_NER.value()
        
        #print('break point')

        self.doCalculation()

        
    def doCalculation(self):
        
        self.d = {}
        for k in ("R_NER", "Rf", "CapFaultCct", "CapAdjacent", "relay_flt", "relay_adj" ):
            self.d[k] = getattr(self,k).value()       
            
        #self.calc.updateCalc(self.d)
        self.calc.updateCalc(self.d)
        
        self.updateGraphs()
                          
    def updateGraphs(self):
        
        self.widget1.canvas.z2_flt.clear()
        self.widget1.canvas.z0_flt.clear()
        self.widget1.canvas.V2V0_flt.clear()
        self.widget1.canvas.I2I0_flt.clear()
        self.widget1.canvas.thresh_flt.clear()
        
        self.widget1.canvas.z2_adj.clear()
        self.widget1.canvas.z0_adj.clear()
        self.widget1.canvas.V2V0_adj.clear()
        self.widget1.canvas.I2I0_adj.clear()
        self.widget1.canvas.thresh_adj.clear()        

        self.widget1.canvas.z2_flt.set_title('Z2 fault cct')
        self.widget1.canvas.z2_flt.plot(self.calc.z2_locus()[0],self.calc.z2_locus()[1],'ro')
        self.widget1.canvas.z2_flt.plot(self.calc.z2_thresholds()[0], self.calc.z2_thresholds()[1])
        self.widget1.canvas.z2_flt.plot(self.calc.z2_thresholds()[2], self.calc.z2_thresholds()[3])
        
        adjust_spines(self.widget1.canvas.z2_flt)
        
        self.widget1.canvas.z0_flt.set_title('Z0 fault cct')
        self.widget1.canvas.z0_flt.plot(self.calc.z0_locus()[0],self.calc.z0_locus()[1],'ro')
        self.widget1.canvas.z0_flt.plot(self.calc.z0_thresholds()[0], self.calc.z0_thresholds()[1])
        self.widget1.canvas.z0_flt.plot(self.calc.z0_thresholds()[2], self.calc.z0_thresholds()[3])
        adjust_spines(self.widget1.canvas.z0_flt)        

        self.widget1.canvas.V2V0_flt.set_title('V2 V0 fault cct')
        self.widget1.canvas.V2V0_flt.plot([0,self.calc.plotV2()[1]],[0,self.calc.plotV2()[0]],linewidth=1, color='purple')
        self.widget1.canvas.V2V0_flt.plot([0,self.calc.plotV0()[1]],[0,self.calc.plotV0()[0]],linewidth=1, color='green')
        
        self.widget1.canvas.I2I0_flt.set_title('I2 I2 fault cct')
        self.widget1.canvas.I2I0_flt.plot([0,self.calc.plotI2()[1]],[0,self.calc.plotI2()[0]],linewidth=1, color='purple')
        self.widget1.canvas.I2I0_flt.plot([0,self.calc.plotI0()[1]],[0,self.calc.plotI0()[0]],linewidth=1, color='green')         
        
        #print self.calc.plotI2()[0]
        
        

        N = 3
        ind = np.arange(N)  # the x locations for the groups
        width = 0.35
        
        self.widget1.canvas.thresh_flt.bar(ind,self.calc.qualRatio())
        self.widget1.canvas.thresh_flt.set_xticks(ind+width)
        self.widget1.canvas.thresh_flt.set_xticklabels(('a2', 'k2', 'a0'))
        self.widget1.canvas.thresh_flt.set_xlabel('qualifying ratio')
        
        
        ###########Adjacent Circuit Graphs#########
        
        
        self.widget1.canvas.z2_adj.set_title('Z2 adj cct')
        self.widget1.canvas.z2_adj.plot(self.calc.z2_locus_adj()[0],self.calc.z2_locus_adj()[1],'ro')
        k,= self.widget1.canvas.z2_adj.plot(self.calc.z2_thresholds()[0], self.calc.z2_thresholds()[1])
        self.widget1.canvas.z2_adj.plot(self.calc.z0_thresholds()[2], self.calc.z0_thresholds()[3])  
        adjust_spines(self.widget1.canvas.z2_adj) 
        
        self.widget1.canvas.z0_adj.set_title('Z0 adj cct')
        self.widget1.canvas.z0_adj.plot(self.calc.z0_locus_adj()[0],self.calc.z0_locus_adj()[1],'ro')
        k,= self.widget1.canvas.z0_adj.plot(self.calc.z0_thresholds()[0], self.calc.z0_thresholds()[1])
        self.widget1.canvas.z0_adj.plot(self.calc.z0_thresholds()[2], self.calc.z0_thresholds()[3])  
        adjust_spines(self.widget1.canvas.z0_adj)          
        
        self.widget1.canvas.V2V0_adj.set_title('V2 V0 adj cct')
        self.widget1.canvas.V2V0_adj.plot([0,self.calc.plotV2adj()[1]],[0,self.calc.plotV2adj()[0]],linewidth=1, color='purple')
        self.widget1.canvas.V2V0_adj.plot([0,self.calc.plotV0adj()[1]],[0,self.calc.plotV0adj()[0]],linewidth=1, color='green')
        
        self.widget1.canvas.I2I0_adj.set_title('I2 I2 adj cct')
        self.widget1.canvas.I2I0_adj.plot([0,self.calc.plotI2adj()[1]],[0,self.calc.plotI2adj()[0]],linewidth=1, color='purple')
        self.widget1.canvas.I2I0_adj.plot([0,self.calc.plotI0adj()[1]],[0,self.calc.plotI0adj()[0]],linewidth=1, color='green') 

        self.widget1.canvas.thresh_adj.bar(ind,self.calc.qualRatio_adj())
        self.widget1.canvas.thresh_adj.set_xticks(ind+width)
        self.widget1.canvas.thresh_adj.set_xticklabels(('a2', 'k2', 'a0'))
        self.widget1.canvas.thresh_adj.set_xlabel('qualifying ratio')   

        self.widget1.canvas.draw()


if __name__=='__main__':
    app = QtGui.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())
    #unittest.main()
