"""
Plot settings
"""

from typing import Sequence
import matplotlib  # type: ignore
import matplotlib.dates as md  # type: ignore
import matplotlib.pyplot as plt  # type: ignore
from .database import db
from .models import Channel, Telemetry
from .subsets import sets

matplotlib.use("Agg")


def collect_data(tlm_set: str, channel: str) -> tuple[list[tuple], list[str]]:
    """
    Collect telemetry data for the specific LTU set and channel.
    """

    # pylint: disable=no-member

    stmt = db.select(Channel.id).where(Channel.name == channel)
    channel_id = db.session.execute(stmt).fetchone()[0]

    columns = [db.column(x) for x in sets[tlm_set]]
    stmt = (
        db.select(columns)
        .select_from(Telemetry)
        .where(Telemetry.channel_id == channel_id)
    )
    result = db.session.execute(stmt)
    return list(result), list(result.keys())


def collect_for_plot(rows: list[tuple], columns: list[str]) -> list[list]:
    """
    Gather data into multiple lists.
    """

    params_list: list[list] = []
    for _ in columns:
        params_list.append([])

    for row in rows:
        for index, elem in enumerate(row):
            params_list[index].append(elem)
    return params_list


def plot_telemetry(
    filename: str, params_list: list[list], columns: Sequence[str], title: str
) -> None:
    """
    Create a plot.
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
    print(md.date2num(params_list[0]))
    axes = plt.gca()
    fig.autofmt_xdate()
    xfmt = md.DateFormatter("%Y-%m-%d")
    axes.xaxis.set_major_formatter(xfmt)
    for param in params_list[1:]:
        plt.plot(md.date2num(params_list[0]), param)

    # Shows colored parameter names labels on a plot
    plt.legend(columns[1:], loc="best", prop={"size": 10})

    plt.savefig(filename)


def get_labels(plot_list: Sequence[str]) -> tuple[str, str]:
    """
    Get plots labels depending on data.
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
