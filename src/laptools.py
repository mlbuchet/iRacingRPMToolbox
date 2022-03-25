def get_best_laps(array_laps, cust_id):
    for laps in array_laps:
        if laps["cust_id"] == cust_id and len(laps["laps"]) > 0:
            minlap = laps["laps"][0]
            for lap in laps["laps"]:
                if lap["lap_time"] <= minlap["lap_time"] and lap["lap_events"] == []:
                    minlap = lap
    return minlap
