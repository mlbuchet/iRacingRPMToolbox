"""
File containing the functions working on laps and array of laps.
"""

def compute_average(laps, top = None):
    '''
    Computes the average time of the best laps of an array.
    top indicates the number of laps to be considered.
    If top is not provided then it computes the average of all laps.
    If there are not enough lap then the function returns None.
    Requires a clean array of laps without untimed laps.
    '''
    if top == None:
        top = len(laps)
    if top == 0 or top > len(laps):
        return None
    laps.sort(key=lambda x: int(x["lap_time"]))
    interest = laps[:top]
    sum = 0
    for lap in interest:
        sum += lap["lap_time"]
    return int(sum/top)

def compute_averages(array_laps, top = None):
    '''
    Computes the average time of the best laps for each driver.
    top indicates the number of laps to be considered.
    If top is not provided then it computes the average of all laps.
    If the driver has no lap time, or less laps than top, then the functions associate None to the driver.
    Requires a clean array of laps without untimed laps.
    '''
    averages = []
    for laps in array_laps:
        averages.append({"cust_id":laps["cust_id"], "average":compute_average(laps["laps"], top)})
    return averages

def evaluate_drivers(array_laps, fraction = .5, gold_threshold = 1.007, silver_threshold = 1.01):
    '''
    Assigns a grade depending on the results from a race.
    fraction: fraction of the number of laps completed by the leader and taking into account in the computation.
        If a driver has completed less than the required number of laps, it is not evaluated.
    gold_threshold: percentage of the winner's average lap time to be classed as a gold driver.
    silver_threshold: percentage of the winner's average lap time to be classed as a silver driver.
    '''
    clean = remove_untimed_laps(array_laps)
    top = int(len(clean[0]["laps"]) * fraction)
    averages = compute_averages(clean, top)
    winner = averages[0]["average"]
    grades = []
    for avg in averages:
        if avg["average"] == None:
            grades.append({"cust_id":avg["cust_id"], "grade":None})
        elif avg["average"] <= gold_threshold * winner:
            grades.append({"cust_id":avg["cust_id"], "grade":"Gold"})
        elif avg["average"] <= silver_threshold * winner:
            grades.append({"cust_id":avg["cust_id"], "grade":"Silver"})
        else:
            grades.append({"cust_id":avg["cust_id"], "grade":"Bronze"})
    return grades

def select_events(array_laps, event):
    '''
    Extract the list of all laps where a given event has happened.
    '''
    eventful = []
    for laps in array_laps:
        for lap in laps["laps"]:
            for evt in lap["lap_events"]:
                if evt == event :
                    lap["cust_id"] = laps["cust_id"]
                    eventful.append(lap)
    return eventful

def remove_untimed_laps(array_laps):
    '''
    Takes an array of laps and return a cleaned version of the array with untimed laps removed.
    '''
    clean = []
    for laps in array_laps:
        laps_driver = {"cust_id":laps["cust_id"], "laps":[]}
        for lap in laps["laps"]:
            if lap["lap_time"] > 0:
                laps_driver["laps"].append(lap)
        clean.append(laps_driver)
    return clean

def clean_for_statistics(laps, flags):
    '''
    Prepares a list of laps for statistical treatment.
    Removes all untimed laps, the first lap and the laps with the selected flags.
    '''
    clean = []
    for lap in laps:
        if lap["lap_time"] > 0 and lap["lap_number"] > 1:
            valid = True
            for flg in flags:
                if flg in lap["lap_events"]:
                    valid = False
            if valid:
                clean.append(lap)
    return clean

def get_lap_statistics(array_laps, flags = ["pitted","lost control"]):
    '''
    Combines statistical informations on the array of laps.
    Ignores lap which contain one of the flags.
    '''
    statistics = []
    for laps in array_laps:
        driver = {"cust_id": laps["cust_id"]}
        clean = clean_for_statistics(laps["laps"], flags)
        clean.sort(key=lambda x: int(x["lap_time"]))
        if len(clean) > 0:
            driver["best_lap"] = clean[0]["lap_time"]
            driver["quartile_1_lap"] = clean[int(len(clean)/4)-1]["lap_time"]
            driver["quartile_3_lap"] = clean[int(3*len(clean)/4)-1]["lap_time"]
            driver["worst_lap"] = clean[len(clean)-1]["lap_time"]
            total = 0
            for lap in clean:
                total += lap["lap_time"]
            driver["average_lap"] = int(total/len(clean))
        else:
            driver["best_lap"] = None
            driver["quartile_1_lap"] = None
            driver["average_lap"] = None
            driver["quartile_3_lap"] = None
            driver["worst_lap"] = None
        statistics.append(driver)
    return statistics
