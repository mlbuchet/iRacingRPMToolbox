"""
Script taking a subsession id from the RPM league as input and exporting the json with the collected information in the second argument.
Syntax: handle_results.py subsession_id output_file
"""

import sys
from lapdata import irLapData
from dataclient import irDataClient
import credentials
import laptools
import leaguetools
import jsonexport
import argparse
import charttools

parser = argparse.ArgumentParser(description='Computes statistics for a race.')
parser.add_argument('subsession_id', type=int, help="Session ID of the race.")
parser.add_argument('output_file', help="Name of the file to be written.")
args = parser.parse_args()

cred = credentials.get_credentials()
client = irDataClient(cred["user"], cred["pwd"])
lpd = irLapData(client)
results = client.get_result(args.subsession_id)
print("Results retrieved")
laps = lpd.get_laps(args.subsession_id)
print("Lapdata retrieved")
league = client.get_league(results["league_id"])
print("League retrieved")
db = leaguetools.build_drivers_database(league)
jsonexport.export_to_json(args.output_file, db, results, laps)
chart = client.get_result_lap_chart_data(args.subsession_id)
print(charttools.compute_overtakes(chart))
