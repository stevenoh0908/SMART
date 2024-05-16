'''
-----
common/datastructures.py
-----
Created: 2024-05-14 11:16:31
Author: Yooshin Oh (stevenoh0908@snu.ac.kr)
-----
Last Modified: 2024-05-16 05:15:36
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
    outputPath: str = "./output"
    pass

@dataclass
class ModelStructureConfig:
    dz: float = 100 # m
    dt: float = 600 # sec
    nz: int = 21
    nt: int = 360
    pass

@dataclass
class ModelConfig:
    modelIOConfig: ModelIOConfig = ModelIOConfig()
    modelStructureConfig: ModelStructureConfig = ModelStructureConfig()
    pass

@dataclass
class ModelData:
    temperature: np.ndarray
    cPProfile: np.ndarray
    RProfile: np.ndarray
    aSwProfile: np.ndarray
    aLwProfile: np.ndarray
    initTProfile: np.ndarray
    pass