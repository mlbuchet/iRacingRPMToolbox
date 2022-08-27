import stats.mappings as mappings

def set_seaborn_defaults(sns):
    sns.set(rc={
        "axes.facecolor":"#333",
        "figure.facecolor":"#333",
        "xtick.color": "#fff",
        "ytick.color": "#fff",
        "legend.labelcolor": "#fff"
    })

def set_axes_labels(plt, xlabel, ylabel):
    plt.xlabel(xlabel, fontsize=36, color="#fff")
    plt.ylabel(ylabel, fontsize=36, color="#fff")

def remove_grid_lines(g):
    for ax in g.axes.flat:
        ax.grid(False)

def add_value_labels(axes, fmt, labels=None):
    for ax in axes:
        for c in ax.containers:
            ax.bar_label(c, labels=labels, fmt=fmt, color="#fff", fontsize=30)

def add_legend(plt, g):
    handles, _ = g.axes.flat[0].get_legend_handles_labels()
    sorted_handles = [next((y for y in handles if y.get_label() == x), None) for x in mappings.class_to_text.values()]
    legend = plt.legend(sorted_handles, list(mappings.class_to_text.values()), loc="upper right", borderpad=2, facecolor="#555")
    plt.setp(legend.get_texts(), color="w", fontsize=30)
