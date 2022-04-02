"""
File containing the function working on the league table.
"""

def build_drivers_database(league):
    '''
    Creates a drivers database from the league information.
    The database contains the following fields:
    cust_id: id of the driver.
    car_nuber: number of the driver.
    name: name of the driver without extra numbers or other artifact.
    class: class in which the driver competes.
    '''
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
