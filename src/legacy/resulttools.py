"""
File containing the function working on the result table.
"""

import leaguetools

def get_qualifying_results(results):
    '''
    Returns the result from qualifying.
    '''
    qualify = []
    for session in results["session_results"]:
        if session["simsession_name"] == "QUALIFY":
            for entry in session["results"]:
                qualify.append({
                    "cust_id": entry["cust_id"],
                    "best_qual_lap_time": entry["best_qual_lap_time"],
                    "starting_position": entry["finish_position"]})
    return qualify

def get_race_results(results, drivers_db):
    '''
    Returns relevant information stored in the results tab of the results table.
    Infos currently exported:
        - cust_id: Customer id.
        - display_name: Customer display name.
        - driver_class: Driver class.
        - finish_position: Finishing postion after the race.
        - laps_complete: Number of laps completed in the race.
        - starting_position: Starting position in the race.
        - best_lap_time: Best lap time.
        - incidents: Number of incidents points during the race.
        - finish_position_in_class: Finishing position within its class.
    '''
    race = []
    for session in results["session_results"]:
        if session["simsession_name"] == "RACE":
            gpos = 0
            spos = 0
            bpos = 0
            for entry in session["results"]:
                # Rank in class
                cls = leaguetools.find_driver(drivers_db, entry["cust_id"])["class"]

                if cls == "Gold":
                    finish_position_in_class = gpos
                    gpos += 1
                elif cls == "Silver":
                    finish_position_in_class = spos
                    spos += 1
                elif cls == "Bronze":
                    finish_position_in_class = bpos
                    bpos += 1
                else:
                    raise RuntimeError("Unknown driver class: ", cls)

                # Basic information already in the original results table from iRacing
                infos = ({
                    "cust_id": entry["cust_id"],
                    "display_name": entry["display_name"],
                    "driver_class": cls,
                    "finish_position": entry["finish_position"],
                    "finish_position_in_class": finish_position_in_class,
                    "laps_complete": entry["laps_complete"],
                    "starting_position": entry["starting_position"],
                    "best_lap_time": entry["best_lap_time"],
                    "incidents": entry["incidents"],
                    "car_id": entry["car_id"]})

                # Writing in the array
                race.append(infos)
    return race

def get_race_infos(results):
    """
    Returns general information for the race
    """
    race = {}
    race["league_name"] = results["league_name"]
    race["start_time"] = results["start_time"]
    race["track_id"] = results["track"]["track_id"]
    race["track_name"] = results["track"]["track_name"]
    race["config_name"] = results["track"]["config_name"]
    return race
