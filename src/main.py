'''
-----
src/main.py
-----
Created: 2024-05-14 09:52:09
Author: Yooshin Oh (stevenoh0908@snu.ac.kr)
-----
Last Modified: 2024-05-21 11:17:06
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
		# Info Message
		print(f"Loading Inputs and Settings from: {configyaml_dir}")
		loader = load.main.Driver()
		self.config, self.data = loader.init(configyaml_dir) # Return Type: common.datastructures.ModelConfig, common.datastructures.ModelData
		pass
	def run(self):
		print("Initializing Driver")
		driver = fdm.main.Driver()
		atmoF = rt.main.atmoForcingFunc
		surfF = rt.main.surfForcingFunc
		print("Loading Driver")
		driver.load(self.data, self.config, atmoF, surfF)
		print("Running Driver")
		driver.run()
		print("Driver Finished")
		pass
	def result(self):
		print("Saving Results into outPath")
		common.save.saveResult(self.data, self.config)
		pass
	pass

def run():
	configyaml_dir = "./config.yml"
	if len(sys.argv) > 1 and os.path.isfile(sys.argv[1]):
		configyaml_dir = sys.argv[1]
		pass
	print('''
---
SMART (Single-column Multi-layered Atmospheric Radiative Transfer) Model | v0.1
* ⓒ Yooshin Oh, Yoonsung Lee, Hyeongjoon Byeon, Dongwon Kang / 2024, Seoul National Univ.
* Github Repo: https://github.com/stevenoh0908/SMART
---
	''')
	driver = Driver(configyaml_dir)
	driver.run()
	driver.result()
	print("DONE! Check Output Path for the Result.")
	return driver
	pass

if __name__ == '__main__':
	result = run()
	pass
