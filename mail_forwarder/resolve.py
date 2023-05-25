import json
import requests
import pprint


postIncidentURL = "https://api.statuspage.io/v1/pages/n814cl79vp6c/incidents/jxfyhk2sdv8x"
headers = {"Authorization": "OAuth bbc29e89-6274-4b68-9fa6-e10389a28685"}



r = requests.delete(url=postIncidentURL, headers=headers)

pprint.pprint(r.json())
