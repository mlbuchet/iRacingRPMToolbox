import os
import argparse
import json

from irapiclient import irApiClient
import stats.incidents as incidents
import stats.qualy as qualy
import stats.fastest_laps as fastest_laps
import stats.boxplot as boxplot

charts = {
    "incidents": incidents,
    "qualy": qualy,
    "fastest-laps": fastest_laps,
    "boxplot": boxplot
}

# Args
parser = argparse.ArgumentParser(description="Generate session stats")
parser.add_argument("subsession_id", type=int, help="Subsession ID")
args = parser.parse_args()

# API client
iac = irApiClient(os.getenv("IRAPI_USR"), os.getenv("IRAPI_PWD"))

# Common data
results = iac.request("results/get", subsession_id=args.subsession_id)
league = iac.request("league/get", league_id=results["league_id"])

# Let's go!
for key, chart in charts.items():
    df = chart.get_dataframe(league, results, client=iac)
    plot = chart.get_plot(df)
    plot.savefig(str(args.subsession_id) + "-" + key + ".png", bbox_inches="tight")
