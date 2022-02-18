"""
Plot LTU telemetry from the database
"""

from queries_data import conn, retrieve_from_db, collect_for_plot
from data_plots import plot_telemetry

# Group db column names to get and plot specific data
brd_plot = ["cutime", "brd_lt1", "brd_lt2", "brd_lt3", "brd_lt4"]
ldd_lt_plot = ["cutime", "ldd_lt1", "ldd_lt2", "ldd_lt3"]
ldd_rt_plot = ["cutime", "ldd_rt1", "ldd_rt2", "ldd_rt3"]
ldd_volt_plot = ["cutime", "ldd_hv1", "ldd_ldout1"]
pls_hv_plot = ["cutime", "pls_hvr1", "pls_hvr2", "pls_hvf1", "pls_hvr2"]
pls_ld_plot = ["cutime", "pls_ldr1", "pls_ldr2", "pls_ldf1", "pls_ldf2"]
pls_cur_plot = ["cutime", "pls_i1", "pls_i2", "pls_i3"]
chg_cur_plot = ["cutime", "chg_vtcur1", "chg_vscur"]
chg_volt_plot = ["cutime", "chg_vsdiv", "chg_vtdiv1"]


brd_cursor = retrieve_from_db(conn, brd_plot, "LTU1_1")
ldd_lt_cursor = retrieve_from_db(conn, ldd_lt_plot, "LTU1_1")
ldd_rt_cursor = retrieve_from_db(conn, ldd_rt_plot, "LTU1_1")
ldd_volt_cursor = retrieve_from_db(conn, ldd_volt_plot, "LTU1_1")
pls_hv_cursor = retrieve_from_db(conn, pls_hv_plot, "LTU1_1")
pls_ld_cursor = retrieve_from_db(conn, pls_ld_plot, "LTU1_1")
pls_cur_cursor = retrieve_from_db(conn, pls_cur_plot, "LTU1_1")
chg_cur_cursor = retrieve_from_db(conn, chg_cur_plot, "LTU1_1")
chg_volt_cursor = retrieve_from_db(conn, chg_volt_plot, "LTU1_1")

brd_lt_params = collect_for_plot(brd_cursor)
ldd_lt_params = collect_for_plot(ldd_lt_cursor)
ldd_rt_params = collect_for_plot(ldd_rt_cursor)
ldd_volt_params = collect_for_plot(ldd_volt_cursor)
pls_hv_params = collect_for_plot(pls_hv_cursor)
pls_ld_params = collect_for_plot(pls_ld_cursor)
pls_cur_params = collect_for_plot(pls_cur_cursor)
chg_cur_params = collect_for_plot(chg_cur_cursor)
chg_volt_params = collect_for_plot(chg_volt_cursor)

plot_telemetry(1, brd_lt_params, brd_plot)
plot_telemetry(2, ldd_lt_params, ldd_lt_plot)
plot_telemetry(3, ldd_rt_params, ldd_rt_plot)
plot_telemetry(4, ldd_volt_params, ldd_volt_plot)
plot_telemetry(5, pls_hv_params, pls_hv_plot)
plot_telemetry(6, pls_ld_params, pls_ld_plot)
plot_telemetry(7, pls_cur_params, pls_cur_plot)
plot_telemetry(8, chg_cur_params, chg_cur_plot)
plot_telemetry(9, chg_volt_params, chg_volt_plot)
