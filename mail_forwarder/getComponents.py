import json
import requests
import pprint

getComponentsURL = "https://api.statuspage.io/v1/pages/DUMMYPAGE/components"
headers = {"Authorization": "OAuth dummyPage"}


def getComponent():

    r = requests.get(url=getComponentsURL, headers=headers)
    data = r.json()
    components = {}
    for obj in data:
        components[obj["name"]] = obj["id"]

    return components

#pprint.pprint(getComponent())
