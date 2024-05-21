'''
-----
common/datastructures.py
-----
Created: 2024-05-14 11:16:31
Author: Yooshin Oh (stevenoh0908@snu.ac.kr)
-----
Last Modified: 2024-05-21 07:01:11
Modified By: Yooshin Oh (stevenoh0908@snu.ac.kr)
-----
- Defines and Manages Common Data Structures Among the Whole Model.
'''

# Ref: https://ihp001.tistory.com/43
from dataclasses import dataclass
import numpy as np

# Model Configurations
@dataclass
class ModelIOConfig:
    configPath: str = "./config.yml"
    cPProfilePath: str = "./data/cp_profile.txt"
    RProfilePath: str = "./data/R_profile.txt"
    aSwProfilePath: str = "./data/a_sw_profile.txt"
    aLwProfilePath: str = "./data/a_lw_profile.txT"
    initTProfilePath: str = "./data/init_T_profile.txt"
    densityProfilePath: str = "./data/density_profile.txt"
    outputPath: str = "../output"
    pass

@dataclass
class ModelStructureConfig:
    dz: float = 100. # m
    dt: float = 600. # sec
    dx: float = 100. # m
    dy: float = 100. # m
    nz: int = 21
    nt: int = 360
    Csua: float = 100. # J/K m^2
    pass

@dataclass
class ModelConfig:
    modelIOConfig: ModelIOConfig = ModelIOConfig()
    modelStructureConfig: ModelStructureConfig = ModelStructureConfig()
    pass

@dataclass
class ModelData:
    temperature: np.ndarray = np.zeros(1)
    cPProfile: np.ndarray = np.zeros(1)
    RProfile: np.ndarray = np.zeros(1)
    aSwProfile: np.ndarray = np.zeros(1)
    aLwProfile: np.ndarray = np.zeros(1)
    densityProfile: np.ndarray = np.zeros(1)
    pass

@dataclass
class ModelResult:
    modelData: ModelData = ModelData()
    modelConfig: ModelConfig = ModelConfig()
    pass
