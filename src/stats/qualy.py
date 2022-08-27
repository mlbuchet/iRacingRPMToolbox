import pandas as pd
import matplotlib.pylab as plt
import seaborn as sns
import math

import stats.mappings as mappings
import helpers.plot as helpers
import helpers.lap_times as helpers_laps

def get_dataframe(league, results, client=None):
    fastest_result = []
    for SessionResult in results["session_results"]:
        if SessionResult["simsession_type"] == 5:
            simsession = []
            simsession.append(SessionResult["simsession_type"])
            simsessionID = SessionResult["simsession_number"]

            for driver in SessionResult["results"]:
                if driver["finish_position"] <99  and driver["laps_complete"] > 0 and driver["best_qual_lap_time"] > 0:
                    for nickname in league["roster"]:
                        if driver["cust_id"] == nickname["cust_id"]:
                            clas = mappings.class_to_text[nickname["nick_name"][-3:]]

                    fastest_detail = []
                    fastest_detail = []
                    fastest_detail.append(driver["display_name"])
                    fastest_detail.append(driver["best_qual_lap_time"] / 10000)
                    fastest_detail.append(clas)
                    fastest_result.append(fastest_detail)

    df = pd.DataFrame(fastest_result)
    df.columns = ["name", "lap_time", "class"]
    df = df.sort_values("lap_time")
    return df


def get_plot(df):
    # Defaults
    helpers.set_seaborn_defaults(sns)

    # Plot it!
    g = sns.catplot(
        x="lap_time",
        y="name",
        data=df,
        hue="class",
        palette=mappings.hues,
        kind="bar",
        dodge=False,
        linewidth=0,
        height=20,
        aspect=16/9,
        legend=False
    )

    # Ticks
    plt.xticks(fontsize=30)
    plt.yticks(fontsize=30)

    # Labels
    helpers.set_axes_labels(plt, "Lap times", "Drivers")

    # Remove grid lines
    helpers.remove_grid_lines(g)

    # Add value labels
    helpers.add_value_labels(g.axes.flat, "%.3f", labels=[helpers_laps.to_human_readable(x) for x in df.lap_time])
    g.axes.flat[0].xaxis.set_major_formatter(lambda x, pos: helpers_laps.to_human_readable(x))

    # Limit xaxis
    min_x = math.floor(min(df["lap_time"]))
    max_x = math.ceil(max(df["lap_time"]))
    g.axes.flat[0].set_xlim(min_x, max_x)

    # Add legend
    helpers.add_legend(plt, g)

    return plt
