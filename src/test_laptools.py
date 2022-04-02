import json
import laptools

def test_compute_average():
    assert False

def test_compute_averages():
    assert False

def test_compute_median():
    assert False

def test_evaluate_drivers():
    assert False

def test_select_events():
    assert False

def test_noted_incidents():
    assert False

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
    assert False
