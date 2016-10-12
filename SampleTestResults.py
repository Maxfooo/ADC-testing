"""
Sample Test Results Source Code
Max Ruiz

NOTES:
+Requires the file "test_ADC_results.txt"
+Requires matplotlib

EXPLANATION OF PROCESS
The reason the sampled code is seperated at 255 (a total of 256 samples) is
due to the Opal Kelly (OK) Front Panel (FP) USB link transmission limitations. 
Stated in the FP user manual, there is a 256 16-bit word queue which is used to
buffer data being transmitted from the OK board to the host computer. When the
host requests more than 256 words of data, the OK board will transmit 256 words,
flush the queue except for the last word sent, and restart transmission. This results
in another 256 words being transmitted, but starting at the last word being transmitted
for a second time. So the final second transmission begins on 255, where the first transmission
left off (which counts as the first of 256 word transmissions) and ends 255 words later, 
arriving at 255+255=510.

This offset is a constant occurance, thus can be filtered out via software for bulk
transmissions. If requesting 256 or less words, waiting, then requesting another 256 or
less words, than this redundant word transmission is removed. Again, this can
be filtered in software so there is no reason to not do a bulk request.
"""


dataFileName = "test_ADC_results.txt"
c256 = 2**8
c255 = c256-1
sampleCodes = []
with open(dataFileName) as f:
    for line in f:
        sampleCodes.append(float(line))
sampleCodes = [sampleCodes[0:c256], sampleCodes[c256:]]
expectedCodes = [[x for x in range(c256)], [x+255 for x in range(c256)]]
error = [[abs(expectedCodes[0][i] - sampleCodes[0][i]) for i in range(c256)],
         [abs(expectedCodes[1][i] - sampleCodes[1][i]) for i in range(c256)]]


import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
ylwPatch = mpatches.Patch(color='yellow', label='Sampled Codes')
blkPatch = mpatches.Patch(color='k', label='Expected Codes')

plt.figure(1)
# plt.subplot(121) # Horizontal
plt.subplot(211) # Vertical
plt.plot(range(len(sampleCodes[0])), sampleCodes[0], 'ys',
         range(len(expectedCodes[0])), expectedCodes[0], 'k')
plt.title('Plot of Sampled Codes and Expected Codes')
plt.ylabel('Resulting Code')
plt.xlabel('Expected Code')
plt.legend(handles=[ylwPatch, blkPatch])

#plt.subplot(122) # Horizontal
plt.subplot(212) # Vertical
plt.plot(error[0])
plt.title('Error in codes 0 through 255')
plt.ylabel('Error (either 1 or 0)')
plt.xlabel('ADC Code')
plt.show()

#-----
plt.figure(1)
# plt.subplot(121) # Horizontal
plt.subplot(211) # Vertical
plt.plot(range(c255,c255+len(sampleCodes[1])), sampleCodes[1], 'ys',
         range(c255,c255+len(expectedCodes[1])), expectedCodes[1], 'k')
plt.title('Plot of Sampled Codes and Expected Codes')
plt.ylabel('Resulting Code')
plt.xlabel('Expected Code')
plt.legend(handles=[ylwPatch, blkPatch])

#plt.subplot(122) # Horizontal
plt.subplot(212) # Vertical
plt.plot(range(255, 511), error[1])
plt.title('Error in codes 255 through 510')
plt.ylabel('Error (either 1 or 0)')
plt.xlabel('ADC Code')
plt.show()
