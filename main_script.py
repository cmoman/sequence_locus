#!/usr/bin/env python
#coding:utf-8
# Author:   --<>
# Purpose: 
# Created: 24/10/14

import sys
import unittest
import numpy as np

from PyQt4 import QtCore, QtGui, QtSvg

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
from matplotlib.figure import Figure

from sequential_clearance import SequentialClearance



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
            self.z2_if = self.fig.add_subplot(2,5,1)
            self.z2_bh= self.fig.add_subplot(2,5,2)
            self.V2I2_if = self.fig.add_subplot(2,5,3, projection = 'polar')
            self.V2I2_bh= self.fig.add_subplot(2,5,4, projection = 'polar')        
            self.V2thresh = self.fig.add_subplot(2,5,5)
            self.zo_if = self.fig.add_subplot(2,5,6) 
            self.z0_bh = self.fig.add_subplot(2,5,7)
            self.V0I2_if = self.fig.add_subplot(2,5,8, projection = 'polar')        
            self.V0I2_bh = self.fig.add_subplot(2,5,9, projection = 'polar')
            self.V0thresh = self.fig.add_subplot(2,5,10)    
            
               
            
            
class MplWidget(QtGui.QWidget):
    def __init__(self,nplots):
        super(MplWidget, self).__init__()
        
        self.canvas = MplCanvas(nplots)
        self.vbl = QtGui.QVBoxLayout()
        self.vbl.addWidget(self.canvas)
        
        self.ntp = NavigationToolbar(self.canvas,self)
        self.vbl.addWidget(self.ntp)        
        
        self.setLayout(self.vbl)
        
class InputDial(QtGui.QWidget):
    def __init__(self, name, tooltip=None, min=0, max=100, radioB = False):
        super(InputDial, self).__init__()
        self.setToolTip(tooltip)
        self.layout = QtGui.QVBoxLayout()
        self.label = QtGui.QLabel(name)
        self.dial = QtGui.QDial()
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
        
        if radioB == True:
            self.radioButton = QtGui.QRadioButton('select to fix')
            self.layout.addWidget(self.radioButton)
        
        self.setLayout(self.layout)
        
    def value(self):
        return self.dial.value()
    
    def setValue(self, value):
        self.spinBox.setValue(value)
        
        
        
class MainWidget(QtGui.QWidget):
    def __init__(self):
        super(MainWidget, self).__init__()
        
        self.calculation = SequentialClearance()

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
        self.R_NER = InputDial('NER', 'Neutral Earthing Resistor in ohms', 0, 50)
        self.CapFaultCct = InputDial('Cap Fault CCT', 'circuit capacitance in microfarads', 0, 500)
        self.CapAdjacent = InputDial('Cap adjacent', 'Sum of adjacent circuits capacitance in microfarads', 0, 500)
        self.relayInFront = InputDial('3I0 current Relay In Front', 'Current seen by relay in front of fault', 0, 10000, True)
        self.relayBehind= InputDial('3I0 current Relay Behind', 'Current seen by relay in front of fault', 0, 10000, True)
        
        layoutdials.addWidget(self.Rf)
        layoutdials.addWidget(self.R_NER)
        layoutdials.addWidget(self.CapFaultCct)
        layoutdials.addWidget(self.CapAdjacent)
        layoutdials.addWidget(self.relayInFront)
        layoutdials.addWidget(self.relayBehind)
        
        self.layout.addLayout(layoutdials)
        
        
        
        #self.layout.addWidget(self.paramter)


        self.setLayout(self.layout)
        
        self.pushButton.clicked.connect(self.clearGraph)
        self.pushButton2.clicked.connect(self.doCalculation)
        
        
    def clearGraph(self):
        self.widget1.canvas.clear()
        self.widget1.canvas.draw()

        
    def doCalculation(self):
        #self.clearGraph()
        self.calculation.calc(self.Rf.value(),self.R_NER.value())
        
        
        self.widget1.canvas.z2_if.clear()
        print (self.calculation.result2()[0], self.calculation.result2()[1])
        self.widget1.canvas.z2_if.plot(self.calculation.result2()[0],self.calculation.result2()[1])
        
        self.widget1.canvas.z2_bh.clear()
        self.widget1.canvas.z2_bh.plot(self.calculation.result1()[0], self.calculation.result1()[1])
        
        self.widget1.canvas.V2thresh.bar([1,2,3],[2,3,5])
        self.widget1.canvas.V2thresh.set_xticks(np.arange(3),('a2','k2','a0'))
        self.widget1.canvas.V2thresh.set_xlabel('xlable')
        #self.widget1.canvas.V2thresh.set_xticklabels(('a','b','c'))
        
        self.widget1.canvas.draw()
        
        
        
        



if __name__=='__main__':
    app = QtGui.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())
    #unittest.main()
