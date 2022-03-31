"""
File containing the function working on the league table.
"""

def build_drivers_database(league):
    db = []
    for driver in league["roster"]:
        entry = {"cust_id":driver["cust_id"], "car_number":driver["car_number"]}
        nick = driver["nick_name"]
        entry["name"] = nick[0:len(nick)-4]
        cls = nick[len(nick)-2]
        if cls == 'G':
            entry["class"] = "Gold"
        elif cls == "S":
            entry["class"] = "Silver"
        elif cls == "B":
            entry["class"] = "Bronze"
        db.append(entry)
    return db
