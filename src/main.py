'''
-----
src/main.py
-----
Created: 2024-05-14 09:52:09
Author: Yooshin Oh (stevenoh0908@snu.ac.kr)
-----
Last Modified: 2024-05-14 11:47:24
Modified By: Yooshin Oh (stevenoh0908@snu.ac.kr)
-----
- Main Driver Module of SMART Model.
'''

from common.constants import *
from common.datastructures import *
import common.save
import fdm.main as fdm
import load.main as loader
import rt.main as rt
import sys, os

class Driver:

	config = None
	data = None

	def __init__(self, configyaml_dir="./config.yml"):
		self.config = loader.driver.parseConfig(configyaml_dir)
		self.data = loader.driver.init(self.config) # Return Type: common.datastructures.ModelData
		loader.driver.loadInitConditions(self.config)
		pass
	def run(self):
		fdm.driver.load(self.data, config=self.config)
		fdm.driver.run()
		pass
	def result(self):
		common.save.run(self.data)
		pass
	pass

if __name__ == '__init__':
	configyaml_dir = "./config.yml"
	if len(sys.argv) > 1 and os.path.isfile(sys.argv[1]):
		configyaml_dir = sys.argv[1]
		pass
	driver = Driver(configyaml_dir)
	driver.run()
	driver.result()
	pass
