"""
Plot settings
"""

from typing import List
from datetime import datetime
import matplotlib.dates as md  # type: ignore
import matplotlib.pyplot as plt  # type: ignore


def plot_telemetry(
    params_list: List[List], plot_list: List[str], title: str = "LTU1_1"
) -> None:
    """
    Create a plot
    """

    fig = plt.figure()
    plt.tick_params(axis="both", which="major", labelsize=10)
    plt.minorticks_on()
    plt.grid(which="minor", linewidth=0.5, linestyle="--")
    plt.grid(which="major", color="grey", linewidth=1)
    plt.title(f"{title} telemetry", fontsize=16)
    plt.xlabel("Time", fontsize=16)
    params_list[0] = [md.date2num(datetime.fromtimestamp(i)) for i in params_list[0]]
    axes = plt.gca()
    fig.autofmt_xdate()
    xfmt = md.DateFormatter("%Y-%m-%d")
    axes.xaxis.set_major_formatter(xfmt)
    for param in params_list[1:]:
        plt.plot(params_list[0], param)

    plt.ylabel(get_labels(plot_list), fontsize=16)

    # Shows colored parameter names labels on a plot
    plt.legend(plot_list[1:], loc="best", prop={"size": 10})

    plt.show()


def get_labels(plot_list: List[str]) -> str:
    """
    Get plots labels depending on data
    """

    if "brd_lt1" in plot_list:
        name = "BRD Temperature"
    elif "ldd_lt1" in plot_list:
        name = "LDD LT Temperature"
    elif "ldd_rt1" in plot_list:
        name = "LDD RT Temperature"
    elif "ldd_hv1" in plot_list:
        name = "LDD Voltage"
    elif "pls_hvr1" in plot_list:
        name = "PLS HV Voltage"
    elif "pld_ldr1" in plot_list:
        name = "PLS LD Voltage"
    elif "pls_i1" in plot_list:
        name = "PLS Current"
    elif "chg_vscur" in plot_list:
        name = "CHG Current"
    else:
        name = "CHG Voltage"
    return name
