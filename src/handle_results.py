"""
Script taking a subsession id from the RPM league as input and exporting the json with the collected information in the second argument.
Syntax: handle_results.py subsession_id output_file
"""

import sys
from lapdata import irLapData
from dataclient import irDataClient
import credentials
import laptools
import resulttools
import leaguetools
import jsonexport

subsession_id = sys.argv[1]
cred = credentials.get_credentials()
client = irDataClient(cred["user"], cred["pwd"])
lpd = irLapData(client)
results = client.get_result(subsession_id)
# laps = lpd.get_laps(subsession_id)
league = client.get_league(results["league_id"])
db = leaguetools.build_drivers_database(league)
jsonexport.export_to_json(argv[2], db, results, laps)
