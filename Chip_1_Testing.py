'''
Created on Oct 11, 2016

@author: Alphacore Engineer 1
'''

from FPGA_Communication import initFPGA
from MessageTexts import *
from Utils import MBox, FDialog, Conversions
from ep_address import *

class Chip_1_Testing():
    
    def __init__(self, fileName=None):
        xem = initFPGA(fileName)
        MB = MBox()
        FD = FDialog()
        CV = Conversions()
    
    def phaseI(self):
        pass
    
    def phaseII(self):
        pass
    
    def phaseIII(self):
        pass
    
    def phaseVI(self):
        pass
    
    def phaseV(self):
        pass
