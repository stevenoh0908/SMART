'''
-----
rt/longwave_forcing.py
-----
Created: 2024-05-17 12:07:43
Author: Yooshin Oh (stevenoh0908@snu.ac.kr)
-----
Last Modified: 2024-05-22 12:38:23
Modified By: Yooshin Oh (stevenoh0908@snu.ac.kr)
-----
- LW Forcing Calculation Methods
'''

import sys
sys.path.append('..\\common')
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
    nt = modelConfig.modelStructureConfig.nt
    if not (0 <= timestep < nt):
        raise ValueError("Timestep Miss: the timestep must be in [0, nt)")
        pass
    dx = modelConfig.modelStructureConfig.dx
    dy = modelConfig.modelStructureConfig.dy
    forcing = np.zeros(nz, dtype=np.float32)
    for iz in range(1, nz):
        mass = dx * dy * modelConfig.modelStructureConfig.dz * modelData.densityProfile[iz-1]
        coef = modelData.aLwProfile[iz-1] * STEFAN_BOLTZMANN_CONST * dx * dy
        upward_arg = 0.
        for k in range(1, iz):
            upward_arg += modelData.aLwProfile[k-1]*(modelData.temperature[timestep,k]**4)*util.transmisttance(modelData, modelConfig, startIdx=k, endIdx=iz-1,type=util.TYPE_LW) #startidx=k-0.5
            pass
        downward_arg = 0.
        for k in range(iz+1, nz):
            downward_arg += modelData.aLwProfile[k-1]*(modelData.temperature[timestep,k]**4)*util.transmisttance(modelData,modelConfig,startIdx=iz,endIdx=k-1,type=util.TYPE_LW) #endidx=k-0.5
            pass
        emission_arg = 2*(modelData.temperature[timestep,iz]**4)
        surf_arg = (modelData.temperature[timestep, 0]**4) * util.transmisttance(modelData, modelConfig, startIdx=0, endIdx=iz-1,type=util.TYPE_LW)
        forcing[iz] = (coef*(upward_arg+downward_arg-emission_arg+surf_arg)) / mass
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
    nt = modelConfig.modelStructureConfig.nt
    if not (0 <= timestep < nt):
        raise ValueError("Timestep Miss: the timestep must be in [0, nt)")
        pass
    dx = modelConfig.modelStructureConfig.dx
    dy = modelConfig.modelStructureConfig.dy
    forcing_down = 0.
    for k in range(1, nz):
        forcing_down += modelData.aLwProfile[k-1]*(modelData.temperature[timestep, k]**4)*util.transmisttance(modelData, modelConfig, startIdx=0, endIdx=k-1, type=util.TYPE_LW) #endidx=k-0.5
        pass
    forcing_down *= STEFAN_BOLTZMANN_CONST * dx * dy
    forcing_up = dx * dy * STEFAN_BOLTZMANN_CONST * (modelData.temperature[timestep, 0]**4)
    forcing = forcing_down - forcing_up
    return forcing
