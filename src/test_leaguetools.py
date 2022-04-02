import json
import leaguetools

def test_build_drivers_database():
    fl = open("../test/data/league_7826.json","r")
    league = json.loads(fl.read())
    fl.close()
    assert league["league_id"] == 7826
    db = leaguetools.build_drivers_database(league)
    assert len(db) == len(league["roster"])
    assert db[0]["cust_id"] == 491843
    assert db[0]["name"] == "Mickaël Buchet"
    assert db[0]["car_number"] == '33'
    assert db[0]["class"] == "Gold"
    assert db[1]["class"] == "Silver"
    assert db[3]["class"] == "Bronze"
