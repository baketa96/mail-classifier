import json
import requests
import pprint
from getComponents import getComponent



components = getComponent()

# match name from email tokenizer


# would also need to map service provider names in order to match for example BEC, Bankdata and SDC

name = "Swedbank"
body = ""

componentId = components[name]

postIncidentURL = "https://api.statuspage.io/v1/pages/n814cl79vp6c/incidents"
headers = {"Authorization": "OAuth bbc29e89-6274-4b68-9fa6-e10389a28685"}
data = {
    "incident": {
        "name": name+" - Bank Down",
        "status": "investigating",
        "body": body,
        "component_ids": [componentId],
    }
}


r = requests.post(url=postIncidentURL, json=data, headers=headers)

#print(r.text)
