import json
import requests
import pprint

getComponentsURL = "https://api.statuspage.io/v1/pages/n814cl79vp6c/components"
headers = {"Authorization": "OAuth auth token"}


r = requests.get(url=getComponentsURL, headers=headers)
data = r.json()

print(r.json)

components = {}
for obj in data:
    components[obj["name"]] = obj["id"]

# print(components)


# match name from email tokenizer


# would also need to map service provider names in order to match for example BEC, Bankdata and SDC

name = "Swedbank"

componentId = components[name]

postIncidentURL = "https://api.statuspage.io/v1/pages/n814cl79vp6c/incidents"
headers = {"Authorization": "OAuth auth token"}
data = {
    "incident": {
        "name": "Bank Down",
        "status": "investigating",
        "body": "Everythiing is down",
        "component_ids": [componentId],
    }
}


r = requests.post(url=postIncidentURL, json=data, headers=headers)

print(r.text)
