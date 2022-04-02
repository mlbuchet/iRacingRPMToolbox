"""
Script taking a subsession id from the RPM league as input and exporting a text file with all laps where incidents should be reviewed.
Syntax: nots_incidents.py subsession_id output_file
"""

import sys
from lapdata import irLapData
from dataclient import irDataClient
import credentials
import leaguetools
import laptools
import iotools
import argparse


parser = argparse.ArgumentParser(description='Notes laps with incidents to be reviewed.')
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
noted = laptools.select_events(laps, "car contact")
iotools.export_noted_laps(args.output_file, noted, db)
