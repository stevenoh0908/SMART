'''
-----
load/main.py
-----
Created: 2024-05-14 11:49:56
Author: Yooshin Oh (stevenoh0908@snu.ac.kr)
-----
Last Modified: 2024-05-16 06:12:26
Last Modified: 2024-05-16 06:12:26
Modified By: Yooshin Oh (stevenoh0908@snu.ac.kr)
-----
- Main Load Module.
- Loads Various Configuration and Initial Conditions from the given configs.
'''

import sys, os
import numpy as np
sys.path.append('../common')
from common.constants import *
from common.datastructures import *
import yaml

class Loader:

    filePath = None
    fileDescriptor = None

    def setFilePath(self, filePath):
        if (type(filePath) != str):
            raise ValueError("The filepath should be given in string")
            pass
        if (not os.path.isfile(filePath)):
            raise IOError(f"The given filepath: {filePath} is not found")
            pass
        self.filePath = filePath
        pass

    def getFilePath(self):
        return self.filePath
    
    def isActive(self):
        return type(self.fileDescriptor) != type(None)
    
    def open(self, filePath=None):
        if (self.isActive()):
            raise IOError("Close the previous file first!")
            pass
        if (filePath != None):
            self.setFilePath(filePath)
            pass
        self.fileDescriptor = open(self.filePath, "r")
        pass

    def close(self):
        if (not self.isActive()):
            raise IOError("The file is not opened yet")
            pass
        self.fileDescriptor.close()
        self.fileDescriptor = None
        pass

    def readLine(self):
        if (not self.isActive()):
            raise IOError("The file is not opened yet")
            pass
        ret = self.fileDescriptor.readline()
        if not ret:
            return ret.strip()
        else:
            return None
        pass

    def loadInto(self, array):
        if (type(array) != np.ndarray):
            raise ValueError("The load array should be numpy.ndarray")
            pass
        if (not self.isActive()):
            raise IOError("The file is not opened yet")
            pass
        lines = self.fileDescriptor.readlines()
        if (len(lines) != array.shape[0]):
            raise ValueError(f"The Size of the given target array: {array.shape[0]} and the profile txt: {len(lines)} is not matched")
            pass
        for idx, line in enumerate(lines):
            array[idx] = float(line.strip())
            pass
        return
    pass

class Driver:

    modelConfig = None
    modelData = None

    def parseConfig(self, configPath):
        if (type(configPath) != str):
            raise ValueError("Invalid configPath. The configPath must be given as str")
            pass
        if (not os.path.isfile(configPath)):
            raise ValueError("Can't Find the given configPath")
            pass
        modelIOConfig = ModelIOConfig()
        modelStructureConfig = ModelStructureConfig()
        config = None
        with open(configPath, "r") as configFile:
            config = yaml.load(configFile, Loader=yaml.FullLoader)
            pass
        config_io = config['modelIOConfig']
        modelIOConfig.configPath = config_io['configPath']
        modelIOConfig.cPProfilePath = config_io['cPProfilePath']
        modelIOConfig.RProfilePath = config_io['RProfilePath']
        modelIOConfig.aSwProfilePath = config_io['aSwProfilePath']
        modelIOConfig.aLwProfilePath = config_io['aLwProfilePath']
        modelIOConfig.initTProfilePath = config_io['initTProfilePath']
        modelIOConfig.outputPath = config_io['outputPath']
        config_structure = config['modelStructureConfig']
        modelStructureConfig.dz = float(config_structure['dz'])
        modelStructureConfig.dt = float(config_structure['dt'])
        modelStructureConfig.nz = int(config_structure['nz'])
        modelStructureConfig.nt = int(config_structure['nt'])
        modelConfig = ModelConfig()
        modelConfig.modelIOConfig = modelIOConfig
        modelConfig.modelStructureConfig = modelStructureConfig
        self.setConfig(modelConfig)
    
    def setConfig(self, config):
        if (type(config) != ModelConfig):
            raise ValueError("Invalid Config. The Config given in setConfig() must be common.datastructures.ModelConfig")
            pass
        self.modelConfig = config
        pass

    def getConfig(self):
        return self.modelConfig
    
    def makeInitConditions(self):
        if (self.modelConfig == None):
            raise RuntimeError("The Configuration is not ready yet")
            pass
        # Init ModelData Structure
        self.modelData = ModelData()
        self.modelData.temperature = np.zeros((self.modelConfig.modelStructureConfig.nt, self.modelConfig.modelStructureConfig.nz+1), dtype=np.float32)
        self.modelData.cPProfile = np.zeros(self.modelConfig.modelStructureConfig.nz+1, dtype=np.float32)
        self.modelData.RProfile = np.zeros(self.modelConfig.modelStructureConfig.nz+1, dtype=np.float32)
        self.modelData.aSwProfile = np.zeros(self.modelConfig.modelStructureConfig.nz+1, dtype=np.float32)
        self.modelData.aLwProfile = np.zeros(self.modelConfig.modelStructureConfig.nz+1, dtype=np.float32)
        loader = Loader()
        # Load InitTemp
        loader.open(self.modelConfig.modelIOConfig.initTProfilePath)
        loader.loadInto(self.modelData.temperature[0,:])
        loader.close()
        # Load cP Profile
        loader.open(self.modelConfig.modelIOConfig.cPProfilePath)
        loader.loadInto(self.modelData.cPProfile[1:])
        loader.close()
        self.modelData.cPProfile[0] = FILL_VALUE
        # Load R Profile
        loader.open(self.modelConfig.modelIOConfig.RProfilePath)
        loader.loadInto(self.modelData.RProfile[1:])
        self.modelData.RProfile[0] = FILL_VALUE
        loader.close()
        # Load aSw Profile
        loader.open(self.modelConfig.modelIOConfig.aSwProfilePath)
        loader.loadInto(self.modelData.aSwProfile[1:])
        self.modelData.aSwProfile[0] = FILL_VALUE
        loader.close()
        # Load aLw Profile
        loader.open(self.modelConfig.modelIOConfig.aLwProfilePath)
        loader.loadInto(self.modelData.aLwProfile[1:])
        self.modelData.aLwProfile[0] = FILL_VALUE
        loader.close()
        # commit changes and return
        return self.modelData

    def init(self, configyaml_dir):
        if (type(configyaml_dir) != str):
            raise ValueError("Invalid Config Path. configyaml_dir must be given in str")
            pass
        self.parseConfig(configyaml_dir)
        self.makeInitConditions()
        return self.modelConfig, self.modelData
    pass

if __name__ != '__main__':
    driver = Driver()
    pass

