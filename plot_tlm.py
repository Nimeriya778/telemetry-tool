"""
Plot LTU telemetry from the database
"""

import sqlite3
from datetime import datetime
import matplotlib.dates as md
import matplotlib.pyplot as plt

brd_plot_list = ["cutime", "brd_lt1", "brd_lt2", "brd_lt3", "brd_lt4"]
ldd_lt_plot_list = ["cutime", "ldd_lt1", "ldd_lt2", "ldd_lt3"]
ldd_rt_plot_list = ["cutime", "ldd_rt1", "ldd_rt2", "ldd_rt3"]
ldd_volt_plot_list = ["cutime", "ldd_hv1", "ldd_ldout1"]
pls_hv_plot_list = ["cutime", "pls_hvr1", "pls_hvr2", "pls_hvf1", "pls_hvr2"]
pls_ld_plot_list = ["cutime", "pls_ldr1", "pls_ldr2", "pls_ldf1", "pls_ldf2"]
pls_cur_plot_list = ["cutime", "pls_i1", "pls_i2", "pls_i2", "pls_i3"]

conn = sqlite3.connect("ltu-tel.sqlite")
cur = conn.cursor()


def retrieve_from_db(cursor_obj, list_of_columns):
    """
    Create the query to get specific data
    """

    script = f"SELECT {','.join(list_of_columns)} FROM telemetry_ltu11"
    return cursor_obj.execute(script)


retrieve_from_db(cur, brd_plot_list)

dates = []
brd_lt_list = []

for row in cur:
    datenums = md.date2num(datetime.fromtimestamp(row[0]))
    dates.append(datenums)
    brd_lt1 = float(row[1])
    brd_lt_list.append(brd_lt1)


def plot_telemetry(fig_number, param1, param2):
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
    axes = plt.gca()
    fig.autofmt_xdate()
    xfmt = md.DateFormatter("%Y-%m-%d")
    axes.xaxis.set_major_formatter(xfmt)
    # plt.legend(loc="best", prop={"size": 10})
    plt.scatter(param1, param2)
    # pylint: disable=C0103
    if "lt" or "rt" in param2:
        plt.ylabel("Temperature", fontsize=16)
    elif "hv" or "ld" or "ldout" in param2:
        plt.ylabel("Voltage", fontsize=16)
    else:
        plt.ylabel("Current", fontsize=16)

    plt.show()


brd_figure = plot_telemetry(1, dates, brd_lt_list)
