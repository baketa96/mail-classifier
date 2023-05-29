import json
import requests
import pprint


postIncidentURL = "https://api.statuspage.io/v1/pages/DummyPage/incidents/xyq8pv87rjd6"
headers = {"Authorization": "OAuth DummyOne"}



r = requests.delete(url=postIncidentURL, headers=headers)

pprint.pprint(r.json())
