from dataclient import irDataClient
import json

"""
Encapsulates the low level interface to the API for functions that need multiple requests.
"""

class irLapData:

    def __init__(self, client):
        '''
        Initialise the client retrieving data from the iRacing servers.
        '''
        self.client = client

    def get_laps(self, subsession_id, simsession_number = 0):
        '''
        Returns all the laps completed in a given subsession.
        Contains all laps, including invalid laps.
        '''
        results = self.client.get_result(subsession_id)
        drivers = results["session_results"][len(results["session_results"])-1]["results"]

        exploited_laps = []

        for driver in drivers:
            print(driver)
            if driver["laps_complete"] > 0:
                laps = self.client.get_result_lap_data(subsession_id, simsession_number, driver["cust_id"])
            else:
                laps = []
            laps_driver = {"cust_id":driver["cust_id"], "laps":[]}
            for lap in laps:
                laps_driver["laps"].append({
                    "lap_number":lap["lap_number"],
                    "lap_time":lap["lap_time"],
                    "lap_events":lap["lap_events"]})
            exploited_laps.append(laps_driver)
        return exploited_laps
