'''
-----
common/constants.py
-----
Created: 2024-05-14 11:16:23
Author: Yooshin Oh (stevenoh0908@snu.ac.kr)
-----
Last Modified: 2024-05-22 01:25:24
Modified By: Yooshin Oh (stevenoh0908@snu.ac.kr)
-----
- Collection of Constants used in this SMART Model.
'''

# Note: ALL CONSTANTS ARE IN SI-STANDARD UNIT.

STEFAN_BOLTZMANN_CONST = 5.670400e-8 # Wm-2K-4, ref from: https://ko.wikipedia.org/wiki/%EC%8A%88%ED%85%8C%ED%8C%90-%EB%B3%BC%EC%B8%A0%EB%A7%8C_%EB%B2%95%EC%B9%99
SOLAR_CONSTANT = 1630 # W/m^2, DEFAULT (Can be Assigned Manually in config.yml)
SOLAR_CONSTANT_INCIDENT = SOLAR_CONSTANT / 4
SURFACE_ALBEDO = 0.3

FILL_VALUE = -9999.0