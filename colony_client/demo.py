# The demo application for a core controller.
import requests

from colony_client.bot import Bot
from colony_client.core_controller import CoreController
from colony_client.visualiser import Visualiser

testCoreController = CoreController("demo")
vis = Visualiser(testCoreController)
testCoreController.createBot("demoCoin1")
testCoreController.createBot("demoCoin2")

response = requests.get("http://65.108.214.180/api/v1/colony/demo")
json = response.json()
print(json)

for i in json['bots'].keys():
    vis.addBot()
vis.run()
