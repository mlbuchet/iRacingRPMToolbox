import pandas as pd
import matplotlib.pylab as plt
import seaborn as sns

import stats.mappings as mappings
import helpers.plot as helpers

def get_dataframe(league, results, client=None):
    fastest_result = []
    for SessionResult in results["session_results"]:
        if SessionResult["simsession_type"] == 6:
            simsession = []
            simsession.append(SessionResult["simsession_type"])
            simsessionID = SessionResult["simsession_number"]

            for driver in SessionResult["results"]:
                if driver["finish_position"] <99  and driver["laps_complete"] > 0:
                    for nickname in league["roster"]:
                        if driver["cust_id"] == nickname["cust_id"]:
                            clas = mappings.class_to_text[nickname["nick_name"][-3:]]

                    inc_per_lap = driver["incidents"] / driver["laps_complete"]
                    fastest_detail = []
                    fastest_detail = []
                    fastest_detail.append(driver["display_name"])
                    fastest_detail.append(driver["incidents"])
                    fastest_detail.append(clas)
                    fastest_detail.append(inc_per_lap)
                    fastest_result.append(fastest_detail)

    df = pd.DataFrame(fastest_result)
    df.columns = ["name", "incidents", "class", "inc_per_lap"]
    df = df.sort_values("incidents")

    return df

def get_plot(df):
    # Defaults
    helpers.set_seaborn_defaults(sns)

    # Plot it!
    g = sns.catplot(
        y="name",
        x="incidents",
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
    helpers.set_axes_labels(plt, "Incidents", "Drivers")

    # Remove grid lines
    helpers.remove_grid_lines(g)

    # Add value labels
    helpers.add_value_labels(g.axes.flat, "%.0f")

    # Add legend
    helpers.add_legend(plt, g)

    # Incident limit lines
    plt.axvline(15, color="y", ls="--", linewidth=2, zorder=0)
    plt.axvline(20, color="orange", ls="--", linewidth=3, zorder=0)
    plt.axvline(25, color="r", ls="-", linewidth=4, zorder=0)

    return plt
