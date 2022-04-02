import json
import laptools
import resulttools
import leaguetools

"""
File containing the exporting functions for use in graphics and interfaces.
"""

def export_to_json(output_file, drivers_db, results, array_laps):
    """
    Exports the driver list with useful informations for display.
    """
    qualifying_table = resulttools.get_qualifying_results(results)
    race_table = resulttools.get_race_results(results, drivers_db)
    drivers_statistics = merge_tables(race_table, qualifying_table)
    laps_statistics = laptools.get_lap_statistics(array_laps)
    drivers_statistics = merge_tables(drivers_statistics, laps_statistics)
    drivers_statistics = introduce_drivers_info(drivers_db, export)
    export = resulttools.get_race_infos(results)
    export["drivers_statistics"] = drivers_statistics
    fw = open(output_file,"w")
    fw.write(json.dumps(export))
    fw.close()

def introduce_drivers_info(drivers_db, array):
    """
    Adds league specific information to the entries in the array.
    The following fields are added: name, number, class.
    """
    export = []
    for entry in array:
        aux = entry.copy()
        driver = resulttools.find_driver(drivers_db, entry["cust_id"])
        aux["name"] = driver["name"]
        aux["car_number"] = driver["car_number"]
        aux["class"] = driver["class"]
        export.append(aux)
    return export

def merge_tables(table1, table2):
    """
    Merge two array of dictionary by merging dictionaries with same cust_id entry.
    If two fields are shared, the entry in table 1 overwrites the entry in table 2.
    """
    merged = []
    for entry1 in table1:
        for entry2 in table2:
            if entry2["cust_id"] == entry1["cust_id"]:
                entry = entry2 | entry1
        merged.append(entry)
    return merged
