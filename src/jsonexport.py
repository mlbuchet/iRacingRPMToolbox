import json
import laptools
import resulttools

"""
File containing the exporting functions for use in graphics and interfaces.
"""

def export_to_json(output_file, drivers_db, results, array_laps):
    """
    Exports the driver list with useful informations for display.
    """
    qualifying_table = resulttools.get_qualifying_results(results)
    race_table = resulttools.get_race_results(results, drivers_db)
    export = merge_tables(race_table, qualifying_table)
    laps_table = laptools.get_lap_statistics(array_laps, ["pitted","invalid","lost control"]) # The second argument represents the flag that gets laps to be ignored.
    export = merge_tables(race_table, laps_table)
    export = introduce_drivers_info(drivers_db, export)
    fw = open(output_file,"w")
    fw.write(json.dumps(export))
    fw.close()

def introduce_drivers_info(drivers_db, array):
    """
    Adds league specific information to the entries in the array.
    The following fields are added: name, number, class.
    """
    for entry in array:
        for driver in drivers_db:
            if driver["cust_id"] == entry["cust_id"]:
                entry["name"] = driver["name"]
                entry["car_number"] = driver["car_number"]
                entry["class"] = driver["class"]
    return array

def merge_tables(table1, table2):
    """
    Merge two array of dictionary by merging dictionaries with same cust_id entry.
    If two fields are shared, the entry in table 1 overwrites the entry in table 2.
    """
    for entry1 in table1:
        for entry2 in table2:
            if entry2["cust_id"] == entry1["cust_id"]:
                entry1 = entry2 | entry1
    return table1
