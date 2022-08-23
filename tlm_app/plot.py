"""
Plot settings
"""

from datetime import datetime
from sqlite3 import Cursor
import matplotlib # type: ignore
import matplotlib.dates as md  # type: ignore
import matplotlib.pyplot as plt  # type: ignore

matplotlib.use("Agg")


def collect_for_plot(cursor_obj: Cursor) -> list[list]:
    """
    Gather data into multiple lists
    """

    params_list: list[list] = []
    for _ in cursor_obj.description:
        params_list.append([])
    for row in cursor_obj:
        for index, elem in enumerate(row):
            params_list[index].append(elem)
    return params_list


def plot_telemetry(
    filename: str, params_list: list[list], columns: list[str], title: str = "LTU1_1"
) -> None:
    """
    Create a plot
    """

    fig = plt.figure(dpi=150)
    plt.tick_params(axis="both", which="major", labelsize=10)
    plt.minorticks_on()
    plt.grid(which="minor", linewidth=0.5, linestyle="--")
    plt.grid(which="major", color="grey", linewidth=1)
    y_name, title_name = get_labels(columns)
    plt.ylabel(y_name, fontsize=16)
    plt.title(f"{title} {title_name}", fontsize=16)
    plt.xlabel("Time", fontsize=16)
    params_list[0] = [md.date2num(datetime.fromtimestamp(i)) for i in params_list[0]]
    axes = plt.gca()
    fig.autofmt_xdate()
    xfmt = md.DateFormatter("%Y-%m-%d")
    axes.xaxis.set_major_formatter(xfmt)
    for param in params_list[1:]:
        plt.plot(params_list[0], param)

    # Shows colored parameter names labels on a plot
    plt.legend(columns[1:], loc="best", prop={"size": 10})

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
