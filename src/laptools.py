'''
Returns the fastest lap of a driver from an array of laps.
If no id is provided for the driver, it returns the fastest lap of the race augmented with the id of the driver having done it.
Only clean laps are counted.

WARNING: Calling this function without customer id will modifiy the returned lap with an extra field of data.
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

"""
Computes the average time of the best laps of an array.
top indicates the number of laps to be considered.
If top is not provided then it computes the average of all laps.
"""
def compute_average(laps, top = None):
    if top == None:
        top = len(laps)
    sorted = sort_laps(laps)
    index = 0
    sum = 0
    while index < top:
        sum += sorted.pop(0)["lap_time"]
        index += 1
    return sum/top

"""
Computes the average time of the best laps for each driver.
top indicates the number of laps to be considered.
If top is not provided then it computes the average of all laps.
"""
def compute_averages(array_laps, top = None):
    averages = []
    for laps in array_laps:
        if top == None or len(laps["laps"]) >= top:
            averages.append({"cust_id":laps["cust_id"], "average":compute_average(laps["laps"], top)})
    return averages

"""
Computes the median of an array of averages.
"""
def compute_median(averages):
    sorted = []
    for avg in averages:
        sorted.append((int(avg["average"]), avg["average"]))
    sorted.sort()
    return sorted[int(len(sorted)/2)][1]

"""
Assigns a grade depending on the results from a race.
fraction: fraction of the number of laps completed by the leader and taking into account in the computation.
    If a driver has completed less than the required number of laps, it is not evaluated.
gold_threshold: percentage of the median average lap time to be classed as a gold driver.
silver_threshold: percentage of the median average lap time to be classed as a silver driver.
"""
def evaluate_drivers(array_laps, fraction = .5, gold_threshold = .99, silver_threshold = .998):
    top = len(array_laps[0]["laps"]) * fraction
    averages = compute_averages(array_laps, top)
    median = compute_median(averages)
    grades = []
    for avg in averages:
        if avg["average"] <= gold_threshold * median:
            grades.append({"cust_id":avg["cust_id"], "grade":"Gold"})
        elif avg["average"] <= silver_threshold * median:
            grades.append({"cust_id":avg["cust_id"], "grade":"Silver"})
        else:
            grades.append({"cust_id":avg["cust_id"], "grade":"Bronze"})
    return grades
