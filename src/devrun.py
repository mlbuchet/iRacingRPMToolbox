import os
from lapdata import irLapData
from dataclient import irDataClient
import credentials

cred = credentials.get_credentials()
client = irDataClient(cred["user"], cred["pwd"])
lpd = irLapData(client)
print(lpd.get_laps(45043469))
