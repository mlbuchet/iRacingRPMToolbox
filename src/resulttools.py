"""
File containing the function working on the result table.
"""

def get_qualifying_results(results):
    """
    Returns the result from qualifying.
    """
    qualify = []
    for session in results["session_results"]:
        if session["simsession_name"] == "QUALIFY":
            for entry in session["results"]:
                qualify.append({
                    "cust_id": entry["cust_id"],
                    "best_qual_lap_time": entry["best_qual_lap_time"],
                    "starting_position": entry["finish_position"]})
    return qualify

def find_driver(drivers_db, cust_id):
    """
    Finds the name corresponding to an id in a name table
    """
    for entry in drivers_db:
        if entry["cust_id"] == cust_id:
            return entry
    return None

def get_race_results(results, drivers_db):
    """
    Returns relevant information stored in the results tab of the results table.
    Infos currently exported:
        - cust_id: Customer id.
        - finish_position: Finishing postion after the race.
        - laps_complete: Number of laps completed in the race.
        - starting_position: Starting position in the race.
        - incidents: Number of incidents points during the race.
        - finish_position_in_class: Finishing position within its class.
    """
    race = []
    for session in results["session_results"]:
        if session["simsession_name"] == "RACE":
            gpos = 0
            spos = 0
            bpos = 0
            for entry in session["results"]:
                # Basic information already in the original results table from iRacing
                infos = ({
                    "cust_id": entry["cust_id"],
                    "finish_position": entry["finish_position"],
                    "laps_complete": entry["laps_complete"],
                    "starting_position": entry["starting_position"],
                    "incidents": entry["incidents"],
                    "car_id": entry["car_id"]})
                # Rank in class
                cls = find_driver(drivers_db,infos["cust_id"])["class"]
                if cls == "Gold":
                    infos["finish_position_in_class"] = gpos
                    gpos += 1
                elif cls == "Silver":
                    infos["finish_position_in_class"] = spos
                    spos += 1
                elif cls == "Bronze":
                    infos["finish_position_in_class"] = bpos
                    bpos += 1
                # Writing in the array
                race.append(infos)
    return race
