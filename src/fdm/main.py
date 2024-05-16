'''
-----
fdm/main.py
-----
Created: 2024-05-16 06:14:14
Author: Yooshin Oh (stevenoh0908@snu.ac.kr)
-----
Last Modified: 2024-05-16 11:59:25
Modified By: Yooshin Oh (stevenoh0908@snu.ac.kr)
-----
- Finite Difference Method Main Module
'''

import sys
sys.path.append('../common')
from common.datastructures import *
import numpy as np
import util

class Driver:
    
    modelData = None
    modelConfig = None
    atmoForcingFunc = None
    surfForcingFunc = None

    '''
    [Policy]
    * Use Forward Euler for the first-timestep.
    * Otherwise, use Trapezoidal.
    '''

    def setModelData(self, modelData):
        if (type(modelData) != ModelData):
            raise TypeError("The modelData must be in common.datastructures.ModelData-typed")
            pass
        self.modelData = modelData
        pass

    def getModelData(self):
        return self.modelData
    
    def setModelConfig(self, modelConfig):
        if (type(modelConfig) != ModelConfig):
            raise TypeError("The modelConfig must be in common.datastructures.ModelConfig-typed")
            pass
        self.modelConfig = modelConfig
        pass

    def setAtmoForcingFunc(self, func):
        if (type(func) != function):
            raise TypeError("The atmoForcingFunc must be a function")
            pass
        self.atmoForcingFunc = func
        pass

    def getAtmoForcingFunc(self):
        return self.atmoForcingFunc
    
    def setSurfForcingFunc(self, func):
        if (type(func) != function):
            raise TypeError("The surfForcingFunc must be a function")
            pass
        self.surfForcingFunc = func
        pass

    def getSurfForcingFunc(self, func):
        return self.surfForcingFunc

    def getModelConfig(self):
        return self.modelConfig

    def load(self, modelData, modelConfig, atmoForcingFunc, surfForcingFunc):
        self.setModelConfig(modelConfig)
        self.setModelData(modelData)
        self.setAtmoForcingFunc(atmoForcingFunc)
        self.setSurfForcingFunc(surfForcingFunc)
        pass

    def run(self):
        '''
        [Policy]
        * Use Forward Euler for the first-timestep.
        * Otherwise, use Trapezoidal.
        '''
        nt = self.modelConfig.modelStructureConfig.nt
        # Forward-Euler for the first-timestep
        # DEBUG MESSAGE
        print(f"Processing: 1/{nt-1}")
        util.fdm_time_forward_euler(self.modelData, self.modelConfig, targetStep=1, atmoForcingFunc=self.atmoForcingFunc, surfForcingFunc=self.surfForcingFunc)
        # For Other-timesteps, use trapezoidal
        for timestep in range(1, nt):
            # DEBUG MESSAGE
            print(f"Processing: {timestep}/{nt-1}")
            util.fdm_time_trapezoidal(self.modelData, self.modelConfig, targetStep=timestep, atmoForcingFunc=self.atmoForcingFunc, surfForcingFunc=self.surfForcingFunc)
            pass
        # DEBUG MESAGE
        print("DONE!")
        pass
    pass    
    