import requests
from bs4 import BeautifulSoup
import credentials
import json

r = requests.get("https://xero.gg/api/self/status/", headers={"x-api-access-key-id" : credentials.id, "x-api-secret-access-key": credentials.secret})
doc = BeautifulSoup(r.text, "html.parser")

doc = str(doc)

data = json.loads(doc)

#Dump JSON object into file, for easier condition programming (eg. if online == true)
with open("game_state_json_dumps\\state.json", 'w') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

data = json.dumps(data, indent=4)