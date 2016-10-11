'''
Created on Sep 22, 2016

@author: Alphacore Engineer 1
'''

from PyQt4 import QtGui, QtCore
import sys

class FPGA_Comm_UI(QtGui.QWidget):
    def __init__(self):
        super(FPGA_Comm_UI, self).__init__()
        
        
        self.tabFrame()
        #self.genericFrame()
        
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
        
        

def main():
    app = QtGui.QApplication(sys.argv)
    ex = FPGA_Comm_UI()
    sys.exit(app.exec_())



if __name__ == "__main__":
    main()
