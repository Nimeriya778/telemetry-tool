"""
Plot LTU telemetry from the database
"""

from typing import List
import sqlite3
from sqlite3 import Connection, Cursor
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

connection = sqlite3.connect("ltu-tel.sqlite")


def retrieve_from_db(conn: Connection, columns: List[str]) -> Cursor:
    """
    Create the query to get specific data
    """

    script = f"SELECT {','.join(columns)} FROM telemetry_ltu11"
    return conn.cursor().execute(script)


brd_cursor = retrieve_from_db(connection, brd_plot_list)
ldd_lt_cursor = retrieve_from_db(connection, ldd_lt_plot_list)
ldd_rt_cursor = retrieve_from_db(connection, ldd_rt_plot_list)
ldd_volt_cursor = retrieve_from_db(connection, ldd_volt_plot_list)
pls_hv_cursor = retrieve_from_db(connection, pls_hv_plot_list)
pls_ld_cursor = retrieve_from_db(connection, pls_ld_plot_list)
pls_cur_cursor = retrieve_from_db(connection, pls_cur_plot_list)


def collect_for_plot(cursor_obj: Cursor) -> List[List]:
    """
    Gather data into multiple lists
    """

    params_list = []
    for _ in cursor_obj.description:
        params_list.append([])
    for row in cursor_obj:
        for index, elem in enumerate(row):
            params_list[index].append(elem)
    # params_list[0] = [md.date2num(datetime.fromtimestamp(i)) for i in params_list[0]]
    return params_list


brd_lt_params = collect_for_plot(brd_cursor)
ldd_lt_params = collect_for_plot(ldd_lt_cursor)
ldd_rt_params = collect_for_plot(ldd_rt_cursor)
ldd_volt_params = collect_for_plot(ldd_volt_cursor)
pls_hv_params = collect_for_plot(pls_hv_cursor)
pls_ld_params = collect_for_plot(pls_ld_cursor)
pls_cur_params = collect_for_plot(pls_cur_cursor)


def plot_telemetry(fig_number: int, params_list: List[List]) -> None:
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
    # plt.legend(loc="best", prop={"size": 10})
    for param in params_list[1:]:
        plt.scatter(params_list[0], param)
    match fig_number:
        case 1:
            plt.ylabel("BRD Temperature", fontsize=16)
        case 2:
            plt.ylabel("LDD LT Temperature", fontsize=16)
        case 3:
            plt.ylabel("LDD RT Temperature", fontsize=16)
        case 4:
            plt.ylabel("LDD Voltage", fontsize=16)
        case 5:
            plt.ylabel("PLS HV Voltage", fontsize=16)
        case 6:
            plt.ylabel("PLS LD Voltage", fontsize=16)
        case 7:
            plt.ylabel("PLS Current", fontsize=16)
    plt.show()


plot_telemetry(1, brd_lt_params)
# plot_telemetry(2, ldd_lt_params)
# plot_telemetry(3, ldd_rt_params)
# plot_telemetry(4, ldd_volt_params)
# plot_telemetry(5, pls_hv_params)
# plot_telemetry(6, pls_ld_params)
# plot_telemetry(7, pls_cur_params)
