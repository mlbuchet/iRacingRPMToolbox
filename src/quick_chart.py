import sys
from lapdata import irLapData
from dataclient import irDataClient
import credentials
import laptools
import leaguetools
import jsonexport
import argparse

cred = credentials.get_credentials()
client = irDataClient(cred["user"], cred["pwd"])
lpd = irLapData(client)

league_sessions = {"season":2, "races":
                [{"race":1, "subsession_id":45043469},
                 {"race":2, "subsession_id":45166697},
                 {"race":3, "subsession_id":45289872},
                 {"race":4, "subsession_id":45412594},
                 {"race":5, "subsession_id":45537036},
                 {"race":6, "subsession_id":45661734},
                 {"race":7, "subsession_id":45783826},
                 {"race":8, "subsession_id":45904709},
                 {"race":9, "subsession_id":46025634}]}

league = client.get_league(7826)
db = leaguetools.build_drivers_database(league)
db.append({"cust_id":374266, "name":"Mat Monestier", "class":"Gold", "car_number":"1"})
db.append({"cust_id":402390, "name":"Zeff Cosemans", "class":"Bronze", "car_number":"84"})
db.append({"cust_id":130889, "name":"Marcus Spry", "class":"Gold", "car_number":"69"})
db.append({"cust_id":482943, "name":"Mohammad Alhussien", "class":"Gold", "car_number":"974"})
print("League database initialised")
data = []

for race in league_sessions["races"]:
    print("Handling Race", race["race"])
    results = client.get_result(race["subsession_id"])
    print("Results retrieved")
    laps = lpd.get_laps(race["subsession_id"])
    print("Lapdata retrieved")
    data.append(jsonexport.compute_informations(db,  results, laps))

grades = []
for driver in db:
    gd = driver
    gd["grades"] = []
    for eval in data:
        grade = ""
        for res in eval["drivers_statistics"]:
            if res["cust_id"] == gd["cust_id"]:
                grade = res["grade"]
        gd["grades"].append(grade)
    grades.append(gd)

file = open("grades.csv", "w")
for entry in grades:
    file.write(entry["class"]+";"+entry["name"]+";")
    for grade in entry["grades"]:
        file.write(grade+";")
    file.write("\n")
file.close()
