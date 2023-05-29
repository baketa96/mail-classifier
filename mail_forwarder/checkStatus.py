import json
import requests
import pprint


postIncidentURL = "https://api.statuspage.io/v1/pages/DUMMYPAGE/incidents/unresolved"
headers = {"Authorization": "OAuth dummyOne"}



r = requests.get(url=postIncidentURL, headers=headers)

pprint.pprint(r.json())
