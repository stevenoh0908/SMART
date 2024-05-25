'''
-----
fdm/filter.py
-----
Created: 2024-05-21 09:12:00
Author: Yooshin Oh (stevenoh0908@snu.ac.kr)
-----
Last Modified: 2024-05-22 12:57:39
Modified By: Yooshin Oh (stevenoh0908@snu.ac.kr)
-----
- Preventing FDM Explosion ... Modules
'''

import sys
sys.path.append('..\\common')
from common.datastructures import *
import numpy as np

# Basic Idea of Explosion-Preventing Filter
# - If the temperature of some height is close to equilibrium, the sign of rt term is switched.
# - Therefore, if there's a some-repeated sign-switching. then stop rt-updating, set rt as 0 at that height

# Default Setting Constants (Not a Common Constant!)
TOLERATION_COUNT = 1
# these three constants are not used, but for understanding, leave these in here.
SIGN_ZERO = 0
SIGN_POSITIVE = 1
SIGN_NEGATIVE = -1

# Filter by Temperature Delta Oscillation
# - use this after update temperature at that timestep.
class FilterTemperatureDelta:

    config = None
    toleration_counts = None
    current_temperature_delta_signs = None
    previous_temperature_delta_signs = None
    violation_counts = None

    def __init__(self, modelConfig, tolerationCount=TOLERATION_COUNT):
        if (type(modelConfig) != ModelConfig):
            raise TypeError("modelConfig must given as common.datastructures.ModelConfig")
            pass
        self.config = modelConfig
        self.toleration_counts = tolerationCount
        self.violation_counts = np.zeros(modelConfig.modelStructureConfig.nz, dtype=np.int32)
        self.current_temperature_delta_signs = np.zeros(modelConfig.modelStructureConfig.nz, dtype=np.int8)
        self.previous_temperature_delta_signs = np.zeros(modelConfig.modelStructureConfig.nz, dtype=np.int8)
        self.return_fluxes_buffer = np.zeros(modelConfig.modelStructureConfig.nz, dtype=np.float32)
        pass

    def is_not_on_equilibrium(self):
        return (self.violation_counts <= self.toleration_counts).astype(np.int8)

    def filter(self, modelData, timestep=0):
        if (type(modelData) != ModelData):
            raise TypeError("arg modelData must be given as common.datastructures.ModelData")
            pass
        # calculate deltas
        if (timestep >= 2):
            current_temperature_deltas = modelData.temperature[timestep,:] - modelData.temperature[timestep-1,:]
            self.current_temperature_delta_signs = (current_temperature_deltas > 0).astype(np.int8) - (current_temperature_deltas < 0).astype(np.int8)
        # check the violation, if there is, then increase violation count
        validity_bits = self.current_temperature_delta_signs[:] * self.previous_temperature_delta_signs[:]
        # -> this bits will be only negative one, if the sign is changed.
        validity_bits = validity_bits * -1 # here, same sign -> -1, different sign -> 1, one of the element is zero -> 0
        validity_bits = validity_bits.clip(min=0) # here, diff sign: 1, other: 0
        self.violation_counts[:] += validity_bits[:] # update violation counts
        # move current delta signs to previous delta signs
        self.previous_temperature_delta_signs[:] = self.current_temperature_delta_signs[:]
        # if one of the height reaches equilibrium, then set temperature after the osciliation as the mean
        is_first_equilibrium = self.violation_counts[:] == (self.toleration_counts + 1)
        modelData.temperature[max(0, timestep-self.toleration_counts):timestep+1, is_first_equilibrium] = np.nanmean(modelData.temperature[max(0, timestep-self.toleration_counts):timestep+1, is_first_equilibrium], axis=0)
        return

# Filter by Radiative Sign Osciliation
# - use this within that timestep, before temperature update
class FilterRadiativeSign:

    config = None
    toleration_counts = None
    current_flux_signs = None
    previous_flux_signs = None
    violation_counts = None
    return_fluxes_buffer = None

    def __init__(self, modelConfig, tolerationCount=TOLERATION_COUNT):
        if (type(modelConfig) != ModelConfig):
            raise TypeError("modelConfig must given as common.datastructures.ModelConfig")
            pass
        self.config = modelConfig
        self.toleration_counts = tolerationCount
        self.violation_counts = np.zeros(modelConfig.modelStructureConfig.nz, dtype=np.int32)
        self.current_flux_signs = np.zeros(modelConfig.modelStructureConfig.nz, dtype=np.int8)
        self.previous_flux_signs = np.zeros(modelConfig.modelStructureConfig.nz, dtype=np.int8)
        self.return_fluxes_buffer = np.zeros(modelConfig.modelStructureConfig.nz, dtype=np.float32)
        pass

    def is_not_on_equilibrium(self):
        return (self.violation_counts <= self.toleration_counts).astype(np.int8)

    def filter(self, modelData, atmo_net_fluxes=None, surf_net_flux=None, timestep=0):
        if (type(modelData) != ModelData):
            raise TypeError("arg modelData must be given as common.datastructures.ModelData")
            pass
        if (type(atmo_net_fluxes) == type(None)):
            raise ValueError("arg atmo_net_fluxes is not given")
            pass
        if (type(surf_net_flux) == type(None)):
            raise ValueError("arg surf_net_flux is not given")
            pass
        if (type(atmo_net_fluxes) != np.ndarray):
            raise TypeError("arg atmo_net_fluxes must be given as np.ndarray")
            pass
        if (type(surf_net_flux) != float and type(surf_net_flux) != np.float32 and type(surf_net_flux) != np.float64):
            raise TypeError("arg surf_net_flux must be given in among float, np.float32, np.float64")
            pass
        # calculate sign
        self.current_flux_signs[1:] = (atmo_net_fluxes[:] > 0).astype(np.int8) - (atmo_net_fluxes[:] < 0).astype(np.int8)
        self.current_flux_signs[0] = (1 if surf_net_flux > 0 else 0) - (1 if surf_net_flux < 0 else 0)
        # check the violation, if there is, then increase violation count
        validity_bits = self.current_flux_signs[:] * self.previous_flux_signs[:]
        # -> this bits will be only negative one, if the sign is changed.
        validity_bits = validity_bits * -1 # here, same sign -> -1, different sign -> 1, one of the element is zero -> 0
        validity_bits = validity_bits.clip(min=0) # here, diff sign: 1, other: 0
        self.violation_counts[:] += validity_bits[:] # update violation counts
        # if the violation_count is exceed the toleration count, then mark rt as 0
        is_on_equilibrium = self.violation_counts[:] > self.toleration_counts
        self.return_fluxes_buffer[1:] = atmo_net_fluxes[:]
        self.return_fluxes_buffer[0] = surf_net_flux
        self.return_fluxes_buffer[is_on_equilibrium] = 0.
        # move current flux signs to previous flux signs
        self.previous_flux_signs[:] = self.current_flux_signs[:]
        # if one of the height reaches equilibrium, then set temperature after the osciliation as the mean
        is_first_equilibrium = self.violation_counts[:] == (self.toleration_counts + 1)
        modelData.temperature[max(0, timestep-self.toleration_counts):timestep+1, is_first_equilibrium] = np.nanmean(modelData.temperature[max(0, timestep-self.toleration_counts):timestep+1, is_first_equilibrium], axis=0)
        return self.return_fluxes_buffer[1:], self.return_fluxes_buffer[0]
