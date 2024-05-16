'''
-----
rt/util.py
-----
Created: 2024-05-17 12:07:31
Author: Yooshin Oh (stevenoh0908@snu.ac.kr)
-----
Last Modified: 2024-05-17 01:07:41
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
def transmisttance(modelData, modelConfig, startIdx=0, endIdx=0, type=TYPE_SW):
    if (startIdx == endIdx): return 1.
    elif not (0 <= startIdx <= modelConfig.modelStructureConfig.nz-1): return 0.
    return np.prod(np.exp(modelData.aSwProfile[startIdx:endIdx-1])) if type == TYPE_SW else np.prod(np.exp(modelData.aLwProfile[startIdx:endIdx-1]))


