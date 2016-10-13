'''
Created on Oct 6, 2016

@author: Max Ruiz
'''


""" 
=================================
=== PRE-TESTING / DEBUGGING =====
=================================
""" 
ADC_DATA_ADDR = 0xA0
ADC_DATA_ADDR_MASK = 0x3FF
FIFO_DATA_COUNT_ADDR = 0xA1
FIFO_DATA_COUNT_ADDR_MASK = 0xFFF
FIFO_EMPTY_ADDR = 0x20 # bit [0]
FIFO_EMPTY_ADDR_MASK = 0x01
#DEBUG_ADDR = 0x20 # bit [1]
RESET_ADDR = 0x00 # bit [0]
RESET_ADDR_MASK = 0x01


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
SET_MASK = 0x0F

# Read Wire

# Read Pipe


"""
----------- Phase II: Individual Pixel Testing -----------
"""
# Write Wire
PIX_OUT_CTRL = 0x02 # [0]
PIX_OUT_CTRL_MASK = 0x01

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
NEXT_ROW_MASK = 0x01

"""
----------- Phase IV: PGA + ADC setup -----------
"""
# Write Wire


# Read Wire


# Read Pipe
ADC_0 = 0xA4 # [9:0]
ADC_0_MASK = 0x3FF
ADC_1 = 0xA5
ADC_1_MASK = 0x3FF
ADC_2 = 0xA6
ADC_2_MASK = 0x3FF
ADC_3 = 0xA7
ADC_3_MASK = 0x3FF

"""
----------- Phase V: Complete system testing -----------
"""
# Write Wire


# Read Wire


# Read Pipe

