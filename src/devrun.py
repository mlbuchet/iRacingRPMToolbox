from lapdata import irLapData
from dataclient import irDataClient
import credentials
import json
import laptools
import resulttools
import leaguetools
import jsonexport
import pandas
import charttools

"""
This file is for testing purposes. Comment the section that are not needed for your current testing.
"""

'''
Testing the requests on the server and writing the results in a json file
'''
# cred = credentials.get_credentials()
# client = irDataClient(cred["user"], cred["pwd"])
# lpd = irLapData(client)
# results = client.get_result(45166697)
# laps = lpd.get_laps(45166697)
# lap_chart = client.get_result_lap_chart_data(45166697)
# league = client.get_league(7826)

'''
Dumping the results locally
'''
# fr = open("test_results.json","w")
# fr.write(json.dumps(results))
# fr.close()
# fd = open("test_laps.json","w")
# fd.write(json.dumps(laps))
# fd.close()
# fr = open("test_league.json","w")
# fr.write(json.dumps(league))
# fr.close()
# fc = open("test_lap_chart.json","w")
# fc.write(json.dumps(lap_chart))
# fc.close()

'''
Reading the results from the local testing dump
'''
fr = open("test_results.json","r")
results = json.loads(fr.read())
fr.close()
fd = open("test_laps.json","r")
laps = json.loads(fd.read())
fd.close()
fd = open("test_league.json", "r")
league = json.loads(fd.read())
fd.close()
fc = open("test_lap_chart.json","r")
charts = json.loads(fc.read())
fc.close()

'''
Testing various functions.
'''
# print(laptools.get_best_lap(laps, 491843))
#
# print(laptools.sort_laps(laps[1]["laps"]))
#
# print(laptools.compute_average(laps[1]["laps"],1))
# print(laptools.compute_average(laps[1]["laps"],5))
# print(laptools.compute_average(laps[1]["laps"],20))
# print(laptools.compute_average(laps[1]["laps"]))
#
# print(laptools.compute_averages(laps,20))
#
# print(laptools.evaluate_drivers(laps))

# print(laptools.select_events(laps,"car contact"))

# name_table = laptools.build_name_table(results)
# incidents = laptools.noted_incidents(laps, name_table)
# incidents.sort(key=lambda x: int(x["lap_number"]))
# print(incidents)

# print(resulttools.get_qualifying_results(results))
# db = leaguetools.build_drivers_database(league)
# jsonexport.export_to_json("test_export.json", db, results, laps)
# fr = open("test_statistics.json","w")
# fr.write(json.dumps(laptools.get_lap_statistics(laps,["pitted","invalid","lost control"])))
# fr.close()

print(charttools.compute_overtakes(charts))
