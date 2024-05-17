'''
-----
fdm/util.py
-----
Created: 2024-05-16 06:14:31
Author: Yooshin Oh (stevenoh0908@snu.ac.kr)
-----
Last Modified: 2024-05-18 12:25:59
Modified By: Yooshin Oh (stevenoh0908@snu.ac.kr)
-----
- Finite Difference Method Utility Functions
'''

import numpy as np
from common.datastructures import *

def fdm_time_forward_euler(modelData, modelConfig, targetStep=1, atmoForcingFunc=None, surfForcingFunc=None):
    if (type(modelData) != ModelData):
        raise TypeError("The First Argument must be given as common.datastructures.ModelData")
        pass
    if (not callable(atmoForcingFunc)):
        raise TypeError("The atmoForcingFunc must be given as a function")
        pass
    if (not callable(surfForcingFunc)):
        raise TypeError("The surfForcingFunc must be given as a function")
        pass
    dt = modelConfig.modelStructureConfig.dt
    dx = modelConfig.modelStructureConfig.dx
    dy = modelConfig.modelStructureConfig.dy
    Csua = modelConfig.modelStructureConfig.Csua
    # Calculate Atmospheric Temperature
    modelData.temperature[targetStep,1:] = (dt / (modelData.cPProfile[:] + modelData.RProfile[:])) * atmoForcingFunc(modelData, modelConfig, timestep=targetStep-1) + modelData.temperature[targetStep-1,1:]
    # Calculate Surface Temperature
    modelData.temperature[targetStep,0] = (dt / (Csua * dx * dy)) * surfForcingFunc(modelData, modelConfig, timestep=targetStep-1) + modelData.temperature[targetStep-1,0]
    return 

def fdm_time_backward_euler(modelData, modelConfig, targetStep=1, atmoForcingFunc=None, surfForcingFunc=None):
    # Can't use backward euler for the time if we always predict to forward (future). But ignore this here.
    if (type(modelData) != ModelData):
        raise TypeError("The First Argument must be given as common.datastructures.ModelData")
        pass
    if (not callable(atmoForcingFunc)):
        raise TypeError("The atmoForcingFunc must be given as a function")
        pass
    if (not callable(surfForcingFunc)):
        raise TypeError("The surfForcingFunc must be given as a function")
        pass
    dt = modelConfig.modelStructureConfig.dt
    dx = modelConfig.modelStructureConfig.dx
    dy = modelConfig.modelStructureConfig.dy
    Csua = modelConfig.modelStructureConfig.Csua
    # Calculate Atmospheric Temperature
    modelData.temperature[targetStep,1:] = (dt / (modelData.cPProfile[:] + modelData.RProfile[:])) * atmoForcingFunc(modelData, modelConfig, timestep=targetStep) + modelData.temperature[targetStep-1,1:]
    # Calculate Surface Temperature
    modelData.temperature[targetStep,0] = (dt / (Csua * dx * dy)) * surfForcingFunc(modelData, modelConfig, timestep=targetStep) + modelData.temperature[targetStep-1,0]
    return 

def fdm_time_trapezoidal(modelData, modelConfig, targetStep=1, atmoForcingFunc=None, surfForcingFunc=None):
    # Trapezoidal euler for the first can't be made.
    if (targetStep < 2):
        raise ValueError("Use Trapezoidal Method for the targetStep >= 2")
        pass
    if (type(modelData) != ModelData):
        raise TypeError("The First Argument must be given as common.datastructures.ModelData")
        pass
    if (not callable(atmoForcingFunc)):
        raise TypeError("The atmoForcingFunc must be given as a function")
        pass
    if (not callable(surfForcingFunc)):
        raise TypeError("The surfForcingFunc must be given as a function")
        pass
    dt = modelConfig.modelStructureConfig.dt
    dx = modelConfig.modelStructureConfig.dx
    dy = modelConfig.modelStructureConfig.dy
    Csua = modelConfig.modelStructureConfig.Csua
    # Calculate Atmospheric Temperature
    modelData.temperature[targetStep,1:] = ((2*dt) / (modelData.cPProfile[:] + modelData.RProfile[:])) * atmoForcingFunc(modelData, modelConfig, timestep=targetStep-1) + modelData.temperature[targetStep-2,1:]
    # Calculate Surface Temperature
    modelData.temperature[targetStep,0] = ((2*dt) / (Csua*dx*dy)) * surfForcingFunc(modelData, modelConfig, timestep=targetStep-1) + modelData.temperature[targetStep-2,0]
    return 

# Prevent Model-exploding - Temperature Min Filter
def min_temp_filter(modelData, modelConfig, targetStep=1):
    # if there's a less-than-zero record, change it to zero
    modelData.temperature[targetStep] = modelData.temperature[targetStep].clip(min=0)
    return