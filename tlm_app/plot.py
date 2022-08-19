"""
Plot settings
"""

from datetime import datetime
import matplotlib.dates as md  # type: ignore
import matplotlib.pyplot as plt  # type: ignore


def plot_telemetry(
    filename: str, columns: list[list], plot_list: list[str], title: str = "LTU1_1"
) -> None:
    """
    Create a plot
    """

    fig = plt.figure()
    plt.tick_params(axis="both", which="major", labelsize=10)
    plt.minorticks_on()
    plt.grid(which="minor", linewidth=0.5, linestyle="--")
    plt.grid(which="major", color="grey", linewidth=1)
    y_name, title_name = get_labels(plot_list)
    plt.ylabel(y_name, fontsize=16)
    plt.title(f"{title} {title_name}", fontsize=16)
    plt.xlabel("Time", fontsize=16)
    columns[0] = [md.date2num(datetime.fromtimestamp(i)) for i in columns[0]]
    axes = plt.gca()
    fig.autofmt_xdate()
    xfmt = md.DateFormatter("%Y-%m-%d")
    axes.xaxis.set_major_formatter(xfmt)
    for param in columns[1:]:
        plt.plot(columns[0], param)

    # Shows colored parameter names labels on a plot
    plt.legend(plot_list[1:], loc="best", prop={"size": 10})

    plt.savefig(filename)


def get_labels(plot_list: list[str]) -> tuple[str, str]:
    """
    Get plots labels depending on data
    """

    if "brd_lt1" in plot_list:
        names = ("Temperature", "BRD temperature")
    elif "ldd_lt1" in plot_list:
        names = ("Temperature", "LDD temperature")
    elif "ldd_rt1" in plot_list:
        names = ("Temperature", "LDD temperature")
    elif "ldd_hv1" in plot_list:
        names = ("Voltage", "LDD voltage")
    elif "pls_hvr1" in plot_list:
        names = ("Voltage", "PLS HV voltage")
    elif "pls_ldr1" in plot_list:
        names = ("Voltage", "PLS LD voltage")
    elif "pls_i1" in plot_list:
        names = ("Current", "PLS current")
    elif "chg_vscur" in plot_list:
        names = ("Current", "CHG current")
    else:
        names = ("Voltage", "CHG voltage")
    return names
