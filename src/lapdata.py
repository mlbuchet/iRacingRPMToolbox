from dataclient import irDataClient
import json

class irLapData:

    def __init__(self, client):
        self.client = client

    def get_laps(self, subsession_id, simsession_number = 0):
        results = self.client.get_result(subsession_id)
        drivers = results["session_results"][len(results["session_results"])-1]["results"]
#        f = open("results.json","r")
#        f.write(json.dumps(drivers))
#        drivers = json.loads(f.read())
#        print(drivers)

        exploited_laps = []

        for driver in drivers:
            laps = self.client.get_result_lap_data(subsession_id, simsession_number, driver["cust_id"])
            laps_driver = {"cust_id":driver["cust_id"], "laps":[]}
            for lap in laps:
                if lap["lap_time"] > 0:
                    laps_driver["laps"].append({
                        "lap_number":lap["lap_number"],
                        "lap_time":lap["lap_time"],
                        "lap_events":lap["lap_events"]})
            exploited_laps.append(laps_driver)
        return exploited_laps
