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
    export = qualifying_table
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
    return entry
