"""
File containing the operations on the lap chart data.
"""

def compute_overtakes(chart, excluded=["pitted, lost control"]):
    """
    Computes the number of overtakes for each driver.
    The excluded field corresponds to the type of events that would lead a lap to not be considered for counting overtakes.
    """
    laps = []
    overtakes = []
    potentials = []
    for crossing in chart:
        # Initialisation if the crossing corresponds to the leader.
        if crossing["lap_position"] == 1:
            laps.append([])
            potentials.append([])
        # Finds all potential overtakes.
        current_lap = crossing["lap_number"]
        if current_lap == 0:
            overtakes.append({"cust_id":crossing["cust_id"], "overtakes":0})
        if current_lap != 0:
            if is_valid(crossing, excluded):
                for pot in potentials[current_lap]:
                    if pot["loss"] == crossing["cust_id"]:
                        overtakes = add_overtake(overtakes, pot["gain"])
            pots = find_overtakes(laps[current_lap-1], laps[current_lap], crossing["cust_id"])
            if len(pots) > 0:
                for pot in pots:
                    potentials[current_lap].append(pot)
        laps[current_lap].append(crossing["cust_id"])
    return overtakes

def find_overtakes(prev, next, cust_id):
    """
    Finds all overtakes done by the driver cust_id during the lap next.
    Prev contains positional information about the previous lap.
    """
    pindex = 0
    overtakes = []
    while prev[pindex] != cust_id:
        overtaken = True
        nindex = 0
        while nindex < len(next) and next[nindex] != cust_id:
            if prev[pindex] == next[nindex]:
                overtaken = False
            nindex = nindex + 1
        if overtaken:
            overtakes.append({"gain":cust_id, "loss":prev[pindex]})
        pindex = pindex + 1
    return overtakes

def add_overtake(overtakes, cust_id):
    """
    Registered a new overtake for the driver referred by cust_id
    """
    for entry in overtakes:
        if entry["cust_id"] == cust_id:
            entry["overtakes"] = entry["overtakes"] + 1
    return overtakes

def is_valid(lap, excluded):
    """
    Returns true if the lap is not affected by any of the events in "excluded".
    """
    for event in excluded:
        if event in lap["lap_events"]:
            return False
    return True
