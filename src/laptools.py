'''
Returns the fastest lap of a driver from an array of laps.
If no id is provided for the driver, it returns the fastest lap of the race augmented with the id of the driver having done it.
Only clean laps are counted.

WARNING: Calling this function without customer id will modified the returned lap with an extra field of data.
'''
def get_best_lap(array_laps, cust_id = None):
    # Looking for the fastest overall lap
    if cust_id == None:
        minlap = array_laps[0]["laps"][0]
        fastest_id = array_laps[0]["cust_id"]
        for laps in array_laps:
            for lap in laps["laps"]:
                if lap["lap_time"] <= minlap["lap_time"] and lap["lap_events"] == []:
                    minlap = lap
                    fastest_id = laps["cust_id"]
        minlap["cust_id"] = fastest_id
    # Looking for the fastest lap from a given driver
    else:
        for laps in array_laps:
            if laps["cust_id"] == cust_id and len(laps["laps"]) > 0:
                minlap = laps["laps"][0]
                for lap in laps["laps"]:
                    if lap["lap_time"] <= minlap["lap_time"] and lap["lap_events"] == []:
                        minlap = lap

    return minlap

"""
Sorts an array of laps and return the sorted array.
"""
def sort_laps(laps):
    aux = []
    for lap in laps:
        aux.append((lap["lap_time"], lap))
    aux.sort(reverse = True)
    sorted = []
    while aux:
        sorted.append(aux.pop()[1])
    return sorted
