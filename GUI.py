'''
Created on Sep 22, 2016

@author: Alphacore Engineer 1
'''

from PyQt4 import QtGui, QtCore
import sys
from FPGA_Communication import initFPGA
from MessageTexts import *
from Utils import MBox, FDialog, Conversions
from ep_addresses import *

class FPGA_Comm_UI(QtGui.QWidget):
    def __init__(self):
        super(FPGA_Comm_UI, self).__init__()
        
        
        
        self.connectionStatus = "Not Connected"
        self.currentExposureTime = '0'
        #self.tabFrame()
        #self.genericFrame()
        self.testFrame()
        
    def genericFrame(self):
        
        QtGui.QToolTip.setFont(QtGui.QFont('SansSerif', 10))
        
        btn = QtGui.QPushButton('Connect', self)
        btn.setToolTip('Press to attempt FPGA connection.')
        btn.resize(btn.sizeHint())
        btn.move(50, 50) 
        
        qbtn = QtGui.QPushButton('Quit', self)
        qbtn.clicked.connect(QtCore.QCoreApplication.instance().quit)
        qbtn.resize(qbtn.sizeHint())
        qbtn.move(100, 100) 
        
        self.setGeometry(300, 300, 250, 150)
        
        self.show()
        
    def tabFrame(self):
        tabs = QtGui.QTabWidget(self)
        tab1 = QtGui.QWidget()
        tab2 = QtGui.QWidget()
        tab3 = QtGui.QWidget()
        tab4 = QtGui.QWidget()
        
        
        vBoxlayout = QtGui.QVBoxLayout()
        pushButton1 = QtGui.QPushButton("Start")
        pushButton2 = QtGui.QPushButton("Settings")
        pushButton3 = QtGui.QPushButton("Stop")
        vBoxlayout.addWidget(pushButton1)
        vBoxlayout.addWidget(pushButton2)
        vBoxlayout.addWidget(pushButton3)
        tab1.setLayout(vBoxlayout)
        
        tabs.addTab(tab1, "Tab 1")
        tabs.addTab(tab2,"Tab 2")
        tabs.addTab(tab3,"Tab 3")
        tabs.addTab(tab4,"Tab 4") 
        
        self.setGeometry(300, 300, 250, 150)
        self.show()
        
    
    def testFrame(self):
        
        mainTestFrame = QtGui.QVBoxLayout()
        mainTestFrame.addWidget(self.connectToFPGAFrame())
        mainTestFrame.addWidget(self.exposureTimeFrame())
        self.setLayout(mainTestFrame)
        self.show()
    
    def connectToFPGAFrame(self):
        
        frame = QtGui.QWidget()
        connectButton = QtGui.QPushButton("Connect to FPGA")
        connectButton.clicked.connect(self._connectToFPGA)
        self.statusLabel = QtGui.QLabel(self.connectionStatus)
        frameLayout = QtGui.QVBoxLayout()
        frameLayout.addWidget(connectButton)
        frameLayout.addWidget(self.statusLabel)
        frame.setLayout(frameLayout)
        
        return frame
    
    def _connectToFPGA(self):
        
        self.xem = initFPGA(exitOnFailure=False)
        if self.xem == None:
            self.connectionStatus = "Not Connected"
        else:
            self.connectionStatus = "Connected"
        
        self.statusLabel.setText(self.connectionStatus)
        
        
    def exposureTimeFrame(self):
        frame = QtGui.QWidget()
        
        expTimeLabel = QtGui.QLabel('Current Exposure Time')
        self.currExpTimeLabel = QtGui.QLabel(self.currentExposureTime)
        self.expTimeLineEdit = QtGui.QLineEdit()
        self.expTimeLineEdit.returnPressed.connect(self._updateExposureTime)
        expTimeButton = QtGui.QPushButton('Update')
        expTimeButton.clicked.connect(self._updateExposureTime)
        frameLayout = QtGui.QVBoxLayout()
        frameLayout.addWidget(expTimeLabel)
        frameLayout.addWidget(self.currExpTimeLabel)
        frameLayout.addWidget(self.expTimeLineEdit)
        frameLayout.addWidget(expTimeButton)
        frame.setLayout(frameLayout)
        
        return frame
        
    def _updateExposureTime(self):
        temp = self.expTimeLineEdit.text()
        # Do some checking here to make sure temp is an
        # appropriate value to set the exposure time to
        self.currentExposureTime = temp
        self.currExpTimeLabel.setText(self.currentExposureTime)
        pass
        

def main():
    app = QtGui.QApplication(sys.argv)
    ex = FPGA_Comm_UI()
    sys.exit(app.exec_())



if __name__ == "__main__":
    main()
