'''
-----
fdm/util.py
-----
Created: 2024-05-16 06:14:31
Author: Yooshin Oh (stevenoh0908@snu.ac.kr)
-----
Last Modified: 2024-05-16 06:27:29
Modified By: Yooshin Oh (stevenoh0908@snu.ac.kr)
-----
- Finite Difference Method Utility Functions
'''

import numpy as np
from common.datastructures import *

def fdm_time_forward_euler(modelData, targetStep=1, forcingFunc=None, dt=None):
    if (type(modelData) != ModelData):
        raise TypeError("The First Argument must be given as common.datastructures.ModelData")
        pass
    if (type(forcingFunc) != function):
        raise TypeError("The forcingFunc must be given as a function")
        pass
    if (type(dt) == float):
        raise TypeError("The dt must be given as float")
        pass
    # Calculate Atmospheric Temperature
    modelData.temperature[targetStep,:1] = (dt / (modelData.cPProfile[:] + modelData.RProfile[:])) * forcingFunc(modelData, timestep=targetStep-1) + modelData.temperature[targetStep-1,:]
    # Calculate Surface Temperature
    # TBC
    return 

def fdm_time_backward_euler(modelData, targetStep=1, forcingFunc=None, dt=None):
    if (type(modelData) != ModelData):
        raise TypeError("The First Argument must be given as common.datastructures.ModelData")
        pass
    if (type(forcingFunc) != function):
        raise TypeError("The forcingFunc must be given as a function")
        pass
    if (type(dt) == float):
        raise TypeError("The dt must be given as float")
        pass
    # Calculate Atmospheric Temperature
    modelData.temperature[targetStep,:1] = (dt / (modelData.cPProfile[:] + modelData.RProfile[:])) * forcingFunc(modelData, timestep=targetStep) + modelData.temperature[targetStep-1,:]
    # Calculate Surface Temperature
    # TBC
    return 

def fdm_time_trapezoidal(modelData, targetStep=1, forcingFunc=None, dt=None):
    if (type(modelData) != ModelData):
        raise TypeError("The First Argument must be given as common.datastructures.ModelData")
        pass
    if (type(forcingFunc) != function):
        raise TypeError("The forcingFunc must be given as a function")
        pass
    if (type(dt) == float):
        raise TypeError("The dt must be given as float")
        pass
    # Calculate Atmospheric Temperature
    modelData.temperature[targetStep,:1] = ((2*dt) / (modelData.cPProfile[:] + modelData.RProfile[:])) * forcingFunc(modelData, timestep=targetStep-1) + modelData.temperature[targetStep-2,:]
    # Calculate Surface Temperature
    # TBC
    return 