import json
import requests
import pprint

getComponentsURL = "https://api.statuspage.io/v1/pages/n814cl79vp6c/components"
headers = {"Authorization": "OAuth bbc29e89-6274-4b68-9fa6-e10389a28685"}


def getComponent():

    r = requests.get(url=getComponentsURL, headers=headers)
    data = r.json()
    components = {}
    for obj in data:
        components[obj["name"]] = obj["id"]

    return components

#pprint.pprint(getComponent())
