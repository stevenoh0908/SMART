'''
-----
src/main.py
-----
Created: 2024-05-14 09:52:09
Author: Yooshin Oh (stevenoh0908@snu.ac.kr)
-----
Last Modified: 2024-05-17 03:35:53
Modified By: Yooshin Oh (stevenoh0908@snu.ac.kr)
-----
- Main Driver Module of SMART Model.
'''

from common.constants import *
from common.datastructures import *
import common.save
import fdm.main
import load.main
import rt.main
import sys, os

class Driver:

	config = None
	data = None

	def __init__(self, configyaml_dir="./config.yml"):
		loader = load.main.Driver()
		self.config, self.data = loader.init(configyaml_dir) # Return Type: common.datastructures.ModelConfig, common.datastructures.ModelData
		pass
	def run(self):
		driver = fdm.main.Driver()
		atmoF = rt.main.atmoForcingFunc
		surfF = rt.main.surfForcingFunc
		driver.load(self.data, self.config, atmoF, surfF)
		driver.run()
		pass
	def result(self):
		common.save.run(self.data)
		pass
	pass

def run():
	configyaml_dir = "./config.yml"
	if len(sys.argv) > 1 and os.path.isfile(sys.argv[1]):
		configyaml_dir = sys.argv[1]
		pass
	driver = Driver(configyaml_dir)
	driver.run()
	# driver.result()
	return driver
	pass

if __name__ == '__init__':
	result = run()
	pass
