from lapdata import irLapData
from dataclient import irDataClient
import credentials

# This file is for testing purposes. Comment the section that are not needed for your current testing.

# Testing the requests on the server and writing the results in a json file
cred = credentials.get_credentials()
client = irDataClient(cred["user"], cred["pwd"])
lpd = irLapData(client)
results = client.get_result(45043469)
laps = lpd.get_laps(45043469)

# Dumping the results locally
fr.open("test_results.json","w")
fr.write(json.dumps(results))
fr.close()
fd.open("test_laps.json","w")
fd.write(json.dumps(laps))
fd.close()

# Reading the results from the local testing dump
fr.open("test_results.json","r")
fr.write(json.dumps(results))
fr.close()
fd.open("test_laps.json","r")
fd.write(json.dumps(laps))
fd.close()
