'''
-----
rt/util.py
-----
Created: 2024-05-17 12:07:31
Author: Yooshin Oh (stevenoh0908@snu.ac.kr)
-----
Last Modified: 2024-05-26 03:30:52
Modified By: Yooshin Oh (stevenoh0908@snu.ac.kr)
-----
* SMART Radiation Transfer - Utility Functions
'''

import sys
sys.path.append('..\\common')
from common.datastructures import *
import numpy as np

# Constants
TYPE_SW = 0
TYPE_LW = 1

# Methods
# Updated on 22 May 2024, Added Support for Half-Cell-Through Transmittance
# Updated on 26 May 2024, Modified Transmittance Procedure: Dongwon Kang
def transmisttance(modelData, modelConfig, startIdx=0, endIdx=0, type=TYPE_SW):
    if (startIdx % 0.5 != 0):
        raise ValueError("startIdx is not Half-integer")
        pass
    if (endIdx % 0.5 != 0):
        raise ValueError("endIdx is not Half-integer")
        pass
    if (startIdx == endIdx): return 1.
    elif not (0 <= startIdx <= modelConfig.modelStructureConfig.nz): return 0.
    else: # Added Half-Integer Transmittance Support
        profile = modelData.aSwProfile if type == TYPE_SW else modelData.aLwProfile
        if (startIdx%1 == 0 and endIdx%1 == 0): # layer bottom margin to layer top margin
            result1=1
            for a in profile[startIdx:endIdx]: result1*=1-a
            return result1
        elif (startIdx%0.5 == 0 and endIdx%1 == 0): # bottom cell center to layer top margin
            bottom_transmittance = (1-profile[int(startIdx-0.5)])**(0.5)
            result2=1 #result=bottom layer 뺀 나머지 layers의 transmittance
            for a in profile[int(startIdx+0.5):endIdx]: result2*=1-a
            return bottom_transmittance * result2
        elif (startIdx%1 == 0 and endIdx%0.5 == 0): # layer bottom margin to top cell center
            top_transmittance = (1-profile[int(endIdx-0.5)])**(0.5)
            result3=1 #result=top layer 뺀 나머지 layers의 transmittance
            for a in profile[startIdx:int(endIdx-0.5)]: result3*=1-a
            return top_transmittance * result3
        else: # bottom cell center to top cell center
            bottom_transmittance = (1-profile[int(startIdx-0.5)])**(0.5)
            top_transmittance = (1-profile[int(endIdx-0.5)])**(0.5)
            result=1 #result=top,bottom layer 뺀 나머지 layers의 transmittance
            for a in profile[int(startIdx+0.5):int(endIdx-0.5)]: result*=1-a
            return bottom_transmittance * top_transmittance * result
        pass
    pass
