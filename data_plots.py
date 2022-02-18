"""
Plot settings
"""

from typing import List
from datetime import datetime
import matplotlib.dates as md  # type: ignore
import matplotlib.pyplot as plt  # type: ignore


def plot_telemetry(
    fig_number: int, params_list: List[List], plot_list: List[str]
) -> None:
    """
    Create a plot
    """

    fig = plt.figure(fig_number)
    plt.tick_params(axis="both", which="major", labelsize=10)
    plt.minorticks_on()
    plt.grid(which="minor", linewidth=0.5, linestyle="--")
    plt.grid(which="major", color="grey", linewidth=1)
    plt.title("LTU Telemetry", fontsize=16)
    plt.xlabel("Time", fontsize=16)
    params_list[0] = [md.date2num(datetime.fromtimestamp(i)) for i in params_list[0]]
    axes = plt.gca()
    fig.autofmt_xdate()
    xfmt = md.DateFormatter("%Y-%m-%d")
    axes.xaxis.set_major_formatter(xfmt)
    for param in params_list[1:]:
        plt.scatter(params_list[0], param)

    # Shows colored parameter names labels on a plot
    plt.legend(plot_list[1:], loc="best", prop={"size": 10})
    ylabels = {
        1: "BRD Temperature",
        2: "LDD LT Temperature",
        3: "LDD RT Temperature",
        4: "LDD Voltage",
        5: "PLS HV Voltage",
        6: "PLS LD Voltage",
        7: "PLS Current",
        8: "CHG Current",
        9: "CHG Voltage",
    }

    plt.ylabel(ylabels[fig_number], fontsize=16)
    plt.show()
