import json
import leaguetools
import resulttools

def test_get_qualifying_results():
    fr = open("../test/data/result_45043469.json","r")
    results = json.loads(fr.read())
    fr.close()
    qualy = resulttools.get_qualifying_results(results)
    assert len(qualy) == 46
    assert qualy[0]["cust_id"] == 374266
    assert qualy[0]["best_qual_lap_time"] == 1185817
    assert qualy[0]["starting_position"] == 0
    assert qualy[42]["cust_id"] == 345695
    assert qualy[42]["best_qual_lap_time"] == 1242183
    assert qualy[42]["starting_position"] == 42

def test_get_race_results():
    fr = open("../test/data/result_45043469.json","r")
    results = json.loads(fr.read())
    fr.close()
    fl = open("../test/data/league_7826.json","r")
    league = json.loads(fl.read())
    fl.close()
    db = leaguetools.build_drivers_database(league)
    race = resulttools.get_race_results(results, db)
    assert len(race) == 46
    assert race[0]["cust_id"] == 374266
    assert race[0]["finish_position"] == 0
    assert race[0]["laps_complete"] == 45
    assert race[0]["starting_position"] == 0
    assert race[0]["incidents"] == 7
    assert race[0]["finish_position_in_class"] == 0
    assert race[2]["cust_id"] == 533283
    assert race[2]["finish_position"] == 2
    assert race[2]["laps_complete"] == 45
    assert race[2]["starting_position"] == 3
    assert race[2]["incidents"] == 4
    assert race[2]["finish_position_in_class"] == 2
    assert race[7]["cust_id"] == 527397
    assert race[7]["finish_position"] == 7
    assert race[7]["finish_position_in_class"] == 2
    assert race[12]["cust_id"] == 402390
    assert race[12]["finish_position"] == 12
    assert race[12]["finish_position_in_class"] == 1
