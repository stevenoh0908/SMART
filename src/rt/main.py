'''
-----
rt/main.py
-----
Created: 2024-05-17 12:01:25
Author: Yooshin Oh (stevenoh0908@snu.ac.kr)
-----
Last Modified: 2024-05-17 01:09:09
Modified By: Yooshin Oh (stevenoh0908@snu.ac.kr)
-----
- Main Radiative Transfer Calculation Module in SMART
'''

import sys
sys.path.append('..\\common')
from common.datastructures import *
import numpy as np
import rt.shortwave_forcing as sw
import rt.longwave_forcing as lw

def atmoForcingFunc(modelData, modelConfig, timestep=1):
    # Calculate Net SW Forcing, invariable from time.
    sw_atmo_forcing = sw.atmo_forcing(modelData, modelConfig, timestep=timestep)
    # Calculate Net LW Forcing
    lw_atmo_forcing = lw.atmo_forcing(modelData, modelConfig, timestep=timestep)
    # Add and Return
    return sw_atmo_forcing + lw_atmo_forcing
    pass

def surfForcingFunc(modelData, modelConfig, timestep=1):
    # Calculate Net SW Forcing
    sw_surf_forcing = sw.surf_forcing(modelData, modelConfig, timestep=timestep)
    # Calculate Net LW Forcing
    lw_surf_forcing = lw.surf_forcing(modelData, modelConfig, timestep=timestep)
    # Add and Return
    return sw_surf_forcing + lw_surf_forcing
    pass
