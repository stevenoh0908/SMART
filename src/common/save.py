'''
-----
common/save.py
-----
Created: 2024-05-14 11:16:38
Author: Yooshin Oh (stevenoh0908@snu.ac.kr)
-----
Last Modified: 2024-05-21 07:01:22
Modified By: Yooshin Oh (stevenoh0908@snu.ac.kr)
-----
- Result Save Functions
'''

import os, sys, datetime, pickle
import xarray as xr
import numpy as np
sys.path.append('../common')
from common.datastructures import *

def getTimestamp():
    return datetime.datetime.now().strftime("%T%m%dT%H%M%S")

def saveResult(modelData, modelConfig):
    if (type(modelData) != ModelData):
        raise TypeError("modelData should be in common.datastructures.ModelData")
        pass
    if (type(modelConfig) != ModelConfig):
        raise TypeError("modelConfig sholud be in common.datastructures.ModelConfig")
        pass

    # If the outputPath does not exist, make one
    if (not os.path.exists(modelConfig.modelIOConfig.outputPath)):
        os.mkdir(modelConfig.modelIOConfig.outputPath)
        pass

    timestamp = getTimestamp()
    modelResultPath = os.path.join(modelConfig.modelIOConfig.outputPath, f'result_modelResult_{timestamp}.pkl')
    temperaturePath = os.path.join(modelConfig.modelIOConfig.outputPath, f'result_temperature_{timestamp}.nc')

    # First, Save ModelResult Structure with python pickle
    modelResult = ModelResult()
    modelResult.modelData = modelData
    modelResult.modelConfig = modelConfig
    with open(modelResultPath, 'wb') as file:
        pickle.dump(modelResult, file)
        pass

    # Second, Save Temperature Profile at Each Timestep as Xarray Dataset -> export as NetCDF4
    times = np.arange(0, modelConfig.modelStructureConfig.dt * modelConfig.modelStructureConfig.nt, modelConfig.modelStructureConfig.dt)
    heights = np.arange(0, modelConfig.modelStructureConfig.nz * modelConfig.modelStructureConfig.dz, modelConfig.modelStructureConfig.dz)
    ds = xr.Dataset(
        data_vars=dict(
            temperature=(["time", "height"], modelData.temperature)
        ),
        coords=dict(
            time=("time", times),
            height=("height", heights)
        ),
        attrs=dict(
            description="Model Temperature Output of SMART Model"
        )
    )
    ds.to_netcdf(path=temperaturePath, mode='w', format="NETCDF4")
    return
