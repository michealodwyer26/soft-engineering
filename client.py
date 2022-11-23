import requests
from colony_client.visualiser import *

cc = CoreController()
vis = Visualiser(cc)
response = requests.get("http://65.108.214.180/api/v1/colony/Naphscolony")
json = response.json()
print(json)

for i in json['bots'].keys():
    vis.addBot()
vis.run()