import json
import laptools

def test_compute_average():
    fl = open("../test/data/test_lapdata_45166697.json","r")
    array_laps = json.loads(fl.read())
    fl.close()
    assert len(array_laps) == 34
    clean = laptools.clean_for_statistics(array_laps[6]["laps"], [])
    assert laptools.compute_average(clean) == 906466
    assert laptools.compute_average(clean, 1) == 884514
    assert laptools.compute_average(clean, 15) == 886626
    assert laptools.compute_average(clean, 200) == None

def test_compute_averages():
    fl = open("../test/data/test_lapdata_45166697.json","r")
    array_laps = json.loads(fl.read())
    fl.close()
    assert len(array_laps) == 34
    clean = laptools.remove_untimed_laps(array_laps)
    averages = laptools.compute_averages(clean)
    assert averages[6]["cust_id"] == 491843
    assert averages[6]["average"] == 907134
    assert averages[33]["cust_id"] == 165203
    assert averages[33]["average"] == None
    assert averages[32]["cust_id"] == 603137
    assert averages[32]["average"] == 1082076
    averages = laptools.compute_averages(clean, 15)
    assert averages[6]["cust_id"] == 491843
    assert averages[6]["average"] == 886626
    assert averages[33]["cust_id"] == 165203
    assert averages[33]["average"] == None
    assert averages[32]["cust_id"] == 603137
    assert averages[32]["average"] == None

def test_compute_median():
    fl = open("../test/data/test_lapdata_45166697.json","r")
    array_laps = json.loads(fl.read())
    fl.close()
    assert len(array_laps) == 34
    clean = laptools.remove_untimed_laps(array_laps)
    averages = laptools.compute_averages(clean)
    assert len(averages) == 34
    assert laptools.compute_median(averages) == 920302
    averages = laptools.compute_averages(clean, 20)
    assert laptools.compute_median(averages) == 893518
    fr = open("trash.txt", "w")
    for avg in averages:
        fr.write(str(avg["average"])+"\n")
    fr.close()

def test_evaluate_drivers():
    assert False

def test_select_events():
    fl = open("../test/data/test_lapdata_45166697.json","r")
    array_laps = json.loads(fl.read())
    fl.close()
    assert len(array_laps) == 34
    reduced = [array_laps[6]]
    car_contact = laptools.select_events(reduced, "car contact")
    assert len(car_contact) == 1
    assert car_contact[0]["cust_id"] == 491843
    assert car_contact[0]["lap_time"] == -1
    assert "car contact" in car_contact[0]["lap_events"]
    assert car_contact[0]["lap_number"] == 58
    off_track = laptools.select_events(reduced, "off track")
    assert len(off_track) == 12
    car_contact = laptools.select_events(array_laps, "car contact")
    assert len(car_contact) == 21

def test_remove_untimed_laps():
    fl = open("../test/data/test_lapdata_45166697.json","r")
    array_laps = json.loads(fl.read())
    fl.close()
    assert array_laps[0]["laps"][0]["lap_time"] == -1
    assert array_laps[1]["laps"][34]["lap_time"] == -1
    clean = laptools.remove_untimed_laps(array_laps)
    assert clean[0]["laps"][0]["lap_time"] > 0
    assert clean[1]["laps"][32]["lap_time"] > 0
    assert clean[1]["laps"][33]["lap_time"] > 0
    assert clean[1]["laps"][34]["lap_time"] > 0

def test_clean_for_statistics():
    fl = open("../test/data/test_lapdata_45166697.json","r")
    array_laps = json.loads(fl.read())
    fl.close()
    laps = array_laps[1]["laps"]
    assert len(laps) == 62
    clean = laptools.clean_for_statistics(laps, [])
    assert len(laps) == 62
    assert len(clean) == 59
    clean = laptools.clean_for_statistics(laps, ["pitted"])
    assert len(laps) == 62
    assert len(clean) == 57
    laps = array_laps[6]["laps"]
    assert len(laps) == 62
    clean = laptools.clean_for_statistics(laps, ["pitted", "lost control"])
    assert len(laps) == 62
    assert len(clean) == 55

def test_get_lap_statistics():
    fl = open("../test/data/test_lapdata_45166697.json","r")
    array_laps = json.loads(fl.read())
    fl.close()
    assert len(array_laps) == 34
    statistics = laptools.get_lap_statistics(array_laps)
    assert len(statistics) == 34
    driver = statistics[6]
    assert driver["cust_id"] == 491843
    assert driver["best_lap"] == 884514
    assert driver["worst_lap"] == 915774
    assert driver["quartile_1_lap"] == 888007
    assert driver["quartile_3_lap"] == 892617
    assert driver["average_lap"] == 891125
    statistics = laptools.get_lap_statistics(array_laps,[])
    assert len(statistics) == 34
    driver = statistics[6]
    assert driver["cust_id"] == 491843
    assert driver["best_lap"] == 884514
    assert driver["worst_lap"] == 1347494
    assert driver["quartile_1_lap"] == 888026
    assert driver["quartile_3_lap"] == 893045
    assert driver["average_lap"] == 906466
