'''
-----
rt/util.py
-----
Created: 2024-05-17 12:07:31
Author: Yooshin Oh (stevenoh0908@snu.ac.kr)
-----
Last Modified: 2024-05-22 12:41:50
Modified By: Yooshin Oh (stevenoh0908@snu.ac.kr)
-----
* SMART Radiation Transfer - Utility Functions
'''

import sys
sys.path.append('../common')
from common.datastructures import *
import numpy as np

# Constants
TYPE_SW = 0
TYPE_LW = 1

# Methods
# Updated on 22 May 2024, Added Support for Half-Cell-Through Transmittance
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
            return np.prod(np.exp(profile[startIdx:endIdx]))
        elif (startIdx%0.5 == 0 and endIdx%1 == 0): # bottom cell center to layer top margin
            bottom_transmittance = profile[int(startIdx-0.5)]**(0.5)
            return bottom_transmittance * np.prod(np.exp(profile[int(startIdx+0.5):endIdx]))
        elif (startIdx%1 == 0 and endIdx%0.5 == 0): # layer bottom margin to top cell center
            top_transmittance = profile[int(endIdx-0.5)]**(0.5)
            return top_transmittance * np.prod(np.exp(profile[startIdx:int(endIdx-0.5)]))
        else: # bottom cell center to top cell center
            bottom_transmittance = profile[int(startIdx-0.5)]**(0.5)
            top_transmittance = profile[int(endIdx-0.5)]**(0.5)
            return bottom_transmittance * top_transmittance * np.prod(np.exp(profile[int(startIdx+0.5):int(endIdx-0.5)]))
        pass
    pass
