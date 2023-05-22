"""
File containing function to export data in formats other than json.
"""

import leaguetools

"""
Export to CSV
"""

"""
Export to text files
"""
def export_noted_laps(file, noted_laps, drivers_db):
    '''
    Export a list of laps numbers associated with the driver's name.
    '''
    fw = open(file, "w")
    noted_laps.sort(key=lambda x: int(x["lap_number"]))
    for lap in noted_laps:
        fw.write(str(lap["lap_number"]) +'\t' + leaguetools.find_driver(drivers_db, lap["cust_id"])["name"] + "\n")
    fw.close()
