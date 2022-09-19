import pandas as pd
import matplotlib.pylab as plt
import seaborn as sns
import math

import stats.mappings as mappings
import helpers.plot as helpers
import helpers.lap_times as helpers_laps

def get_dataframe(league, results, client=None):
    plot_results = []
    for SessionResult in results["session_results"]:
        if SessionResult["simsession_type"] == 6:
            simsession = []
            simsession.append(SessionResult["simsession_type"])
            simsessionID = SessionResult["simsession_number"]

            for driver in SessionResult["results"]:
                if driver["finish_position"] <99 and driver["laps_complete"] > 1:
                    for nickname in league["roster"]:
                        if driver["cust_id"] == nickname["cust_id"]:
                            clas = mappings.class_to_text[nickname["nick_name"][-3:]]
                    laps = client.request("results/lap_data", subsession_id=results["subsession_id"], cust_id=driver["cust_id"], simsession_number=0)
                    for lap in laps:
                        laps_event = str(lap["lap_events"])
                        if str.__contains__(laps_event, "pitted") == False and str.__contains__(laps_event,"inval") == False and lap["lap_time"] != -1 and lap["lap_time"] <= driver["best_lap_time"]*1.05    and lap["lap_number"] > 1:
                            plot_detail = []
                            plot_detail.append(lap["display_name"])
                            plot_detail.append(lap["lap_time"]/10000)
                            plot_detail.append(clas)
                            plot_results.append(plot_detail)

    df = pd.DataFrame(plot_results)
    df.columns = ["name", "lap_time", "class"]
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
        kind="box",
        dodge=False,
        height=20,
        aspect=16/9,
        legend=False,
        capprops={
            "color": "#fff"
        },
        flierprops={
            "markerfacecolor": "#fff"
        },
        medianprops={
            "color": "#fff"
        },
        whiskerprops={
            "color": "#fff"
        },
    )

    # Ticks
    plt.xticks(fontsize=30)
    plt.yticks(fontsize=30)

    # Labels
    helpers.set_axes_labels(plt, "Lap times", "Drivers")

    # Remove grid lines
    helpers.remove_grid_lines(g)

    # Format xticks
    g.axes.flat[0].xaxis.set_major_formatter(lambda x, pos: helpers_laps.to_human_readable(x))

    # Add legend
    helpers.add_legend(plt, g)

    return plt
