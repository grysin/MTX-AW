import cx_Oracle
import os
import csv
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import date

cx_Oracle.init_oracle_client(
    lib_dir=r"C:\Program Files (x86)\Oracle\instantclient_21_3"
)
# connection string
connect_string = (
    "gntcaadm/gntcaadm01@OHNTWEBDB_VCS.am.freescale.net:1522/OHNTWEB.AM.FREESCALE.NET"
)
# connect to oracle
conn = cx_Oracle.connect(connect_string)
cursor = conn.cursor()

handler_list = [
    "MTX04",
    "MTX06",
    "MTX07",
    "MTXA01",
    "MTXA02",
    "MTXA03",
    "MTXA04",
    "MTXA05",
    "MTXA06",
    "MTXA07",
    "MTXA08",
    "MTXA09",
    "MTXA11",
    "MTXA12",
    "MTXA13",
]

week = date.today().isocalendar()[1]
weeks = [week - 2, week - 1, week]

week_count = pd.DataFrame(columns=weeks)
fig, (ax1, ax2) = plt.subplots(figsize=(10, 6), nrows=2, ncols=1)
fig.canvas.set_window_title("MTX Jam Stats")
colormap = plt.get_cmap("Set1")
if (len(handler_list) % 2) == 0:
    num_hanlders = len(handler_list)
else:
    num_hanlders = len(handler_list) + 1

num_colors = int(num_hanlders / 2) + 1
colors = [colormap(i) for i in np.linspace(0, 1, num_colors)]
# get the date to get the week in order to get two weeks back

for i, handler in enumerate(handler_list):
    Y = []
    for week in weeks:
        statement = (
            "SELECT COUNT(ALID) FROM MTX_JAM_STAT_DATA WHERE HANDLERNAME = '"
            + handler
            + "' AND WEEK ='"
            + str(week)
            + "' GROUP BY HANDLERNAME"
        )
        cursor.execute(statement)
        result = cursor.fetchall()
        try:
            count = result[0][0]
        except IndexError:
            count = 0
        Y.append(count)
    week_count.loc[handler] = Y

    if i <= num_hanlders / 2:
        ax1.scatter(weeks, Y, label=handler, color=colors[i])

    if i > num_hanlders / 2:
        j = i - (num_hanlders / 2)
        j = int(j)
        ax2.scatter(weeks, Y, label=handler, color=colors[j])

plt.ylabel("Count")
plt.xlabel("Work Week")

ax1.set_xticks(np.arange(min(weeks), max(weeks) + 1, 1.0))
ax1.set_yticks(np.arange(0, max(week_count), 2))
ax2.set_xticks(np.arange(min(weeks), max(weeks) + 1, 1))
ax2.set_yticks(np.arange(0, max(week_count), 2))


plt.show()
print(week_count)
