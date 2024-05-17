'''
-----
rt/shortwave_forcing.py
-----
Created: 2024-05-17 12:07:37
Author: Yooshin Oh (stevenoh0908@snu.ac.kr)
-----
Last Modified: 2024-05-17 03:22:16
Modified By: Yooshin Oh (stevenoh0908@snu.ac.kr)
-----
- SW Forcing Calculation Methods
'''

import sys
sys.path.append('../common')
from common.constants import *
from common.datastructures import *
import numpy as np
import rt.util as util

def atmo_forcing(modelData, modelConfig, timestep=1):
    if (type(modelData) != ModelData):
        raise TypeError("Type Miss: modelData is not in common.datastructures.ModelData")
        pass
    if (type(modelConfig) != ModelConfig):
        raise TypeError("Type Miss: modelConfig is not in common.datastructures.ModelConfig")
        pass
    nz = modelConfig.modelStructureConfig.nz
    coef = SOLAR_CONSTANT * modelConfig.modelStructureConfig.dx * modelConfig.modelStructureConfig.dy
    forcing = np.zeros(nz, dtype=np.float32)
    for iz in range(1, nz):
        mass = modelConfig.modelStructureConfig.dx * modelConfig.modelStructureConfig.dy * modelConfig.modelStructureConfig.dz * modelData.densityProfile[iz-1]
        first_arg = util.transmisttance(modelData, modelConfig, startIdx=iz, endIdx=nz, type=util.TYPE_SW)-util.transmisttance(modelData, modelConfig, startIdx=iz-1, endIdx=nz, type=util.TYPE_SW)
        second_arg = util.transmisttance(modelData, modelConfig, startIdx=0, endIdx=nz, type=util.TYPE_SW)*(util.transmisttance(modelData, modelConfig, startIdx=0, endIdx=iz-1, type=util.TYPE_SW)-util.transmisttance(modelData, modelConfig, startIdx=0, endIdx=iz, type=util.TYPE_SW))
        forcing[iz] = (coef*(first_arg+second_arg))/mass
        pass
    return forcing[1:]

def surf_forcing(modelData, modelConfig, timestep=1):
    if (type(modelData) != ModelData):
        raise TypeError("Type Miss: modelData is not in common.datastructures.ModelData")
        pass
    if (type(modelConfig) != ModelConfig):
        raise TypeError("Type Miss: modelConfig is not in common.datastructures.ModelConfig")
        pass
    nz = modelConfig.modelStructureConfig.nz
    coef = SOLAR_CONSTANT * modelConfig.modelStructureConfig.dx * modelConfig.modelStructureConfig.dy * (1 - SURFACE_ALBEDO)
    forcing = coef*util.transmisttance(modelData, modelConfig, startIdx=0, endIdx=nz, type=util.TYPE_SW)
    return forcing
