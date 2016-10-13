'''
Created on Oct 11, 2016

@author: Alphacore Engineer 1
'''

from FPGA_Communication import initFPGA
from MessageTexts import *
from Utils import MBox, FDialog, Conversions
from ep_addresses import *

class Chip_1_Testing():
    
    def __init__(self, fileName=None, testingClass=False):
        self.testingClass = testingClass
        if self.testingClass == False:
            self.xem = initFPGA(fileName)
            self.MB = MBox()
            self.FD = FDialog()
            self.CV = Conversions()
    
    def _cmndShiftReg(self, testingTitle):
        print('\n'+testingTitle)
        print('State      |     Command')
        print('------------------------')
        print('Set[0]     |     \'0\'')
        print('Set[24]    |     \'1\'')
        print('Set[48]    |     \'2\'')
        print('Set[72]    |     \'3\'')
        print('Reset      |     \'r\'')
        print('Exit       |     \'e\'')
        print('\nSelect a State: ')
        
        ans = input()
        if ans == 'e':
            print('Exiting')
            return 'e'
        elif ans == 'r':
            if self.testingClass == False:
                self.xem.writeWire(SET, val=0xF, mask=SET_MASK)
            else:
                print(ans)
        elif ans == '0':
            if self.testingClass == False:
                self.xem.writeWire(SET, val=0xE, mask=SET_MASK)
            else:
                print(ans)
        elif ans == '1':
            if self.testingClass == False:
                self.xem.writeWire(SET, val=0xD, mask=SET_MASK)
            else:
                print(ans)
        elif ans == '2':
            if self.testingClass == False:
                self.xem.writeWire(SET, val=0xB, mask=SET_MASK)
            else:
                print(ans)
        elif ans == '3':
            if self.testingClass == False:
                self.xem.writeWire(SET, val=0x7, mask=SET_MASK)
            else:
                print(ans)
        else:
            print('No Command: {}'.format(ans))
        return ans
    
    def phaseI(self):
        """
        Procedure Proposal
        --------------------
        1) Initially set SET = 1111
        2) Set SET bit to 1110
        3) Observe the output
        4) Repeat with SET = 1101, etc. each time until done
        5) Repeat entire thing for Pixel binning as well
        6) Esko had a frame rate requirement using binning, ask about that
        --------------------
        Looking for
        1) shift_clk & shift_clk_en to go low, then start up
        2) correct number of cycles before seeing output of shift reg
        --------------------
        The results of the shift register could also be evaluated
        entirely on via the FPGA, but it may be a good idea to 
        visually examine the output first.
        """
        if self.testingClass == False:
            self.xem.writeWire(SET, val=0xF, mask=SET_MASK)
        ans = self._cmndShiftReg('Phase I - Shift Register Test')
        while (ans != 'e'):
            ans = self._cmndShiftReg('Phase I - Shift Register Test')
            
        
    
    def phaseII(self, analog=0):
        """
        Procedure Proposal
        --------------------
        ANALOG
        1) initiailly Set SET = 1111
        2) pix_out_ctrl=0
        3) SET = 1110, observe output
        4) Repeat
        """
        if self.testingClass == False:
            self.xem.writeWire(SET, val=0xF, mask=SET_MASK)
            self.xem.writeWire(PIX_OUT_CTRL, 0x0, PIX_OUT_CTRL_MASK)
        ans = self._cmndShiftReg('Phase II - Individual Pixel Test')
        while (ans != 'e'):
            ans = self._cmndShiftReg('Phase II - Individual Pixel Test')
    
    def phaseIII(self):
        """
        Procedure Proposal
        --------------------
        1) Initially set SET == 1111
        2) Set SET == 1110
        3) Use trigger NEXT_ROW to signify next pixel row select 
            on FPGA shift register until all pixel rows are tested        
        """
        if self.testingClass == False:
            self.xem.writeWire(SET, val=0xF, mask=SET_MASK)
        ans0 = self._cmndShiftReg('Phase III - Pixel Array Test')
        ans1 = None
        triggerCount = 0
        while (ans0 != 'e' and ans1 != 'e'):
            print('State      |     Command')
            print('------------------------')
            print('Shift Row  |     \'0\'')
            print('Exit       |     \'e\'')
            print('\nSelect a State: ')
            ans1 = input()
            if ans1 == 'e':
                print('\nExiting')
                break
            elif ans1 == '0':
                # assert trigger here
                self.xem.writeTrigger(NEXT_ROW, NEXT_ROW_MASK)
                triggerCount += 1
                print('\nTrigger Count: {}\n'.format(triggerCount))
            else:
                print('No Command: {}'.format(ans1))
                continue
                       
        
        
    def phaseVI(self):
        """
        Procedure Proposal
        --------------------
        DIGITAL (Through ADC)
        1) initiailly Set SET = 1111
        2) pix_out_ctrl=1
        3) SET = 1110, observe output
        4) Repeat
        
        **Question
        Do we need to set SET to a different value in this test?
        
        """
        if self.testingClass == False:
            self.xem.writeWire(SET, val=0xF, mask=SET_MASK)
            self.xem.writeWire(PIX_OUT_CTRL, 0x1, PIX_OUT_CTRL_MASK)
    
        ans0 = self._cmndShiftReg('Phase IV - PGA+ADC Test')
        ans1 = None
        triggerCount = 0
        while (ans0 != 'e' and ans1 != 'e'):
            print('State      |     Command')
            print('------------------------')
            print('Shift Row  |     \'0\'')
            print('Exit       |     \'e\'')
            print('\nSelect a State: ')
            ans1 = input()
            if ans1 == 'e':
                print('\nExiting')
                break
            elif ans1 == '0':
                # assert trigger here
                self.xem.writeTrigger(NEXT_ROW, NEXT_ROW_MASK)
                triggerCount += 1
                print('\nTrigger Count: {}\n'.format(triggerCount))
            else:
                print('No Command: {}'.format(ans1))
                continue
            
            
    def phaseV(self):
        pass
    
    
    
    
if __name__ == '__main__':
    fileName = 'adc_testing_top.bit'
    C1_Testing = Chip_1_Testing(fileName, testingClass=True)
    C1_Testing.phaseIII()
