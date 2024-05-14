'''
-----
load/main.py
-----
Created: 2024-05-14 11:49:56
Author: Yooshin Oh (stevenoh0908@snu.ac.kr)
-----
Last Modified: 2024-05-15 12:16:55
Modified By: Yooshin Oh (stevenoh0908@snu.ac.kr)
-----
- Main Load Module.
- Loads Various Configuration and Initial Conditions from the given configs.
'''

import sys, os
sys.path.append('../common')
from common.datastructures import *
import yaml

class Driver:

    modelConfig = None

    def parseConfig(self, configPath):
        if (type(self.modelConfig) != str):
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
        modelIOConfig.betaAProfilePath = config_io['betaAProfilePath']
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
        if (type(self.modelConfig) != ModelConfig):
            raise ValueError("Invalid Config. The Config given in setConfig() must be common.datastructures.ModelConfig")
            pass
        self.modelConfig = config
        pass

    def getConfig(self):
        return self.modelConfig
    
    def init(self, configyaml_dir):
        if (type(configyaml_dir) != str):
            raise ValueError("Invalid Config Path. configyaml_dir must be given in str")
            pass
        
        pass
    # TODO
    # - Add init
    # - Add makeInitConditions
    pass

if __name__ != '__main__':
    driver = Driver()
    pass

