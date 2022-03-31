def get_best_lap(array_laps, cust_id = None):
    '''
    Returns the fastest lap of a driver from an array of laps.
    Requires an array of laps without untimed laps.
    If no id is provided for the driver, it returns the fastest lap of the race augmented with the id of the driver having done it.
    Only clean laps are counted.

    WARNING: Calling this function without customer id will modifiy the returned lap with an extra field of data.
    '''
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

def sort_laps(laps):
    """
    Sorts an array of laps and return the sorted array.
    """
    aux = []
    for lap in laps:
        aux.append((lap["lap_time"], lap))
    aux.sort(reverse = True)
    sorted = []
    while aux:
        sorted.append(aux.pop()[1])
    return sorted


def compute_average(laps, top = None):
    """
    Computes the average time of the best laps of an array.
    top indicates the number of laps to be considered.
    If top is not provided then it computes the average of all laps.
    Requires a clean array of laps without untimed laps.
    """
    if top == None:
        top = len(laps)
    sorted = sort_laps(laps)
    index = 0
    sum = 0
    while index < top:
        sum += sorted.pop(0)["lap_time"]
        index += 1
    return sum/top


def compute_averages(array_laps, top = None):
    """
    Computes the average time of the best laps for each driver.
    top indicates the number of laps to be considered.
    If top is not provided then it computes the average of all laps.
    Requires a clean array of laps without untimed laps.
    """
    averages = []
    for laps in array_laps:
        if top == None or len(laps["laps"]) >= top:
            averages.append({"cust_id":laps["cust_id"], "average":compute_average(laps["laps"], top)})
    return averages

def compute_median(averages):
    """
    Computes the median of an array of averages.
    Requires a clean array of laps without untimed laps.
    """
    sorted = []
    for avg in averages:
        sorted.append((int(avg["average"]), avg["average"]))
    sorted.sort()
    return sorted[int(len(sorted)/2)][1]

def evaluate_drivers(array_laps, fraction = .5, gold_threshold = .99, silver_threshold = .998):
    """
    Assigns a grade depending on the results from a race.
    fraction: fraction of the number of laps completed by the leader and taking into account in the computation.
        If a driver has completed less than the required number of laps, it is not evaluated.
    gold_threshold: percentage of the median average lap time to be classed as a gold driver.
    silver_threshold: percentage of the median average lap time to be classed as a silver driver.
    Requires a clean array of laps without untimed laps.
    """
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

def select_events(array_laps, event):
    """
    Extract the list of all laps where a given event has happened.

    WARNING: Eventful laps will be modified with an extra field of data containing the customer id.
    """
    eventful = []
    for laps in array_laps:
        for lap in laps["laps"]:
            for evt in lap["lap_events"]:
                if evt == event :
                    lap["cust_id"] = laps["cust_id"]
                    eventful.append(lap)
    return eventful

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

def noted_incidents(array_laps, name_table):
    """
    Builds the list of car contacts in a race
    """
    eventful = select_events(array_laps, "car contact")
    incidents = []
    for evt in eventful:
        exch = {"lap_number": evt["lap_number"], "display_name": find_name_in_table(name_table, evt["cust_id"])}
        incidents.append(exch)
    return incidents

def remove_untimed_laps(array_laps):
    """
    Takes an array of laps and return a cleaned version of the array with untimed laps removed.
    """
    clean = []
    for laps in array_laps:
        laps_driver = {"cust_id":laps["cust_id"], "laps":[]}
        for lap in laps:
            if lap["lap_time"] > 0:
                laps_driver["laps"].append(lap)
        clean.append(laps_driver)
    return clean
