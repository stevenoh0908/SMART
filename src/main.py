#############################################
# main.py
#############################################
# - The main driver module of SMART Model
# - 14 May 2024, Yooshin Oh (stevenoh0908@snu.ac.kr)
#############################################

from common.constants import *
from common.datastructures import *
from common.save import *
import fdm.main as fdm
import load.main as loader
import rt.main as rt
import sys, os

class Driver:

	self.config = None
	self.data = None

	def __init__(self, configyaml_dir="./config.yml"):
		self.config = loader.parseConfig(configyaml_dir)
		self.data = loader.init(self.config)
		loader.loadInitConditions(self.config)
		pass
	def run(self):
		fdm.load(self.data, config=self.config)
		fdm.run()
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
