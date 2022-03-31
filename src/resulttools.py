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

def build_name_table(results):
    """
    Constructs a table associating a customer id and the name of the driver.
    Requires a result table as input.
    """
    drivers = []
    for driver in results["session_results"][len(results["session_results"])-1]["results"]:
        dvr = {"cust_id":driver["cust_id"], "display_name":driver["display_name"]}
        drivers.append(dvr)
    return drivers

def find_name_in_table(name_table, cust_id):
    """
    Finds the name corresponding to an id in a name table
    """
    for entry in name_table:
        if entry["cust_id"] == cust_id:
            return entry["display_name"]
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
        - incidents_per_lap: Average number of incidents per lap.
        - progression: Gained/Lost positions during the race.
    """
    race = []
    for session in results["session_results"]:
        if session["simsession_name"] == "RACE":
            for entry in session["results"]:
                infos = ({
                    "cust_id": entry["cust_id"],
                    "finish_position": entry["finish_position"],
                    "laps_complete": entry["laps_complete"],
                    "starting_position": entry["starting_position"],
                    "incidents": entry["incidents"]})
                if infos["laps_complete"] > 0:
                    infos["incidents_per_lap"] = infos["incidents"] / infos["laps_complete"]
                else:
                    infos["incidents_per_lap"] = -1
                infos["progression"] = infos["starting_position"] - infos["finish_position"]
                race.append(infos)
    return race
