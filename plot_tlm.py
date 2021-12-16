"""
Plot telemetry of LTU database
"""

import sqlite3
from datetime import datetime
import matplotlib.dates as md
import matplotlib.pyplot as plt

conn = sqlite3.connect("ltu-tel.sqlite")
cur = conn.cursor()

cur.execute(
    """SELECT cutime, brd_lt1, brd_lt2, brd_lt3, brd_lt4,
        ldd_lt1, ldd_lt2, ldd_lt3, ldd_rt1, ldd_rt2, ldd_rt3 FROM telemetry_ltu11"""
)

dates = []
brd_lt1_temps, brd_lt2_temps, brd_lt3_temps, brd_lt4_temps = [], [], [], []
ldd_lt1_temps, ldd_lt2_temps, ldd_lt3_temps = [], [], []
ldd_rt1_temps, ldd_rt2_temps, ldd_rt3_temps = [], [], []

for row in cur:
    datenums = md.date2num(datetime.fromtimestamp(row[0]))
    dates.append(datenums)

    brd_lt1 = float(row[1])
    brd_lt1_temps.append(brd_lt1)

    brd_lt2 = float(row[2])
    brd_lt2_temps.append(brd_lt2)

    brd_lt3 = float(row[3])
    brd_lt3_temps.append(brd_lt3)

    brd_lt4 = float(row[4])
    brd_lt4_temps.append(brd_lt4)

    ldd_lt1 = float(row[5])
    ldd_lt1_temps.append(ldd_lt1)

    ldd_lt2 = float(row[6])
    ldd_lt2_temps.append(ldd_lt2)

    ldd_lt3 = float(row[7])
    ldd_lt3_temps.append(ldd_lt3)

    ldd_rt1 = float(row[8])
    ldd_rt1_temps.append(ldd_rt1)

    ldd_rt2 = float(row[9])
    ldd_rt2_temps.append(ldd_rt2)

    ldd_rt3 = float(row[10])
    ldd_rt3_temps.append(ldd_rt3)

fig = plt.figure()
plt.plot([], [])
# Plot the LTU telemetry temperatures data
plt.plot(dates, brd_lt1_temps, label="brd_lt1")
plt.plot(dates, brd_lt2_temps, label="brd_lt2")
plt.plot(dates, brd_lt3_temps, label="brd_lt3")
plt.plot(dates, brd_lt4_temps, label="brd_lt4")
plt.scatter(dates, ldd_lt1_temps, label="ldd_lt1", s=3)
plt.scatter(dates, ldd_lt2_temps, label="ldd_lt2", s=3)
plt.scatter(dates, ldd_lt3_temps, label="ldd_lt3", s=3)
plt.scatter(dates, ldd_rt1_temps, label="ldd_rt1", s=3)
plt.scatter(dates, ldd_rt2_temps, label="ldd_rt2", s=3)
plt.scatter(dates, ldd_rt3_temps, label="ldd_rt3", s=3)
ax = plt.gca()
fig.autofmt_xdate()
xfmt = md.DateFormatter("%Y-%m-%d")
ax.xaxis.set_major_formatter(xfmt)

plt.title("LTU Telemetry - Temperatures", fontsize=26)
plt.xlabel("Time", fontsize=16)
plt.ylabel("LTU Temperature", fontsize=16)
plt.legend(loc="best", prop={"size": 10})
plt.tick_params(axis="both", which="major", labelsize=10)
plt.minorticks_on()
plt.grid(which="minor", linewidth=0.5, linestyle="--")
plt.grid(which="major", color="grey", linewidth=1)

plt.show()
