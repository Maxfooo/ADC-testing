'''
Created on Oct 6, 2016

@author: Max Ruiz
'''
ADC_DATA_ADDR = 0xA0
FIFO_DATA_COUNT_ADDR = 0xA1
FIFO_EMPTY_ADDR = 0x20 # bit [0]
#DEBUG_ADDR = 0x20 # bit [1]
RESET_ADDR = 0x00 # bit [0]


""" 
=================================
======== CHIP 1 TESTING =========
=================================
""" 

""" 
++++++++++++ NOTES ++++++++++++++
- Ins and Outs are relative to the host
- Some addresses/Ins/Outs will be used for multiple, Phases 
+++++++++++++++++++++++++++++++++
""" 

"""
----------- Phase I: Shift Register -----------
"""
# Write Wire
SET = 0x01 # [3:0]

# Read Wire

# Read Pipe


"""
----------- Phase II: Individual Pixel Testing -----------
"""
# Write Wire
PIX_OUT_CTRL = 0x02 # [0]

# Read Wire

# Read Pipe



"""
----------- Phase III: Pixel array -----------
"""
# Write Wire


# Read Wire


# Read Pipe

# Trigger To FPGA
NEXT_ROW = 0x52 # [0]

"""
----------- Phase IV: PGA + ADC setup -----------
"""
# Write Wire


# Read Wire


# Read Pipe
ADC_0 = 0xA4 # [9:0]
ADC_1 = 0xA5
ADC_2 = 0xA6
ADC_3 = 0xA7


"""
----------- Phase V: Complete system testing -----------
"""
# Write Wire


# Read Wire


# Read Pipe

