import cx_Oracle
import os
import csv
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

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

# for handler in handler_list:
#     for week in
weeks = [
    1,
    2,
    3,
    4,
    5,
    6,
    7,
    8,
    9,
    10,
    11,
    12,
    13,
    14,
    15,
    16,
    17,
    18,
    19,
    20,
    21,
    22,
    23,
    24,
    25,
    26,
]

week_count = pd.DataFrame(columns=weeks)
fig, ax = plt.subplots(figsize=(15, 8.5))
fig.canvas.set_window_title("MTX Jam Stats")
colormap = plt.get_cmap("hsv")
colors = [colormap(i) for i in np.linspace(0, 1, len(handler_list))]


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
    ax.plot(weeks, Y, label=handler, color=colors[i])

plt.title("Alarms On Handlers Each Week")
plt.ylabel("Count")
plt.xlabel("Work Week")
ax.set_xticks(np.arange(min(weeks), max(weeks) + 1, 1.0))
box = ax.get_position()
ax.set_position([box.x0, box.y0 + box.height * 0.1, box.width, box.height * 0.8])
ax.legend(
    loc="upper center", bbox_to_anchor=(0.5, -0.1), fancybox=True, shadow=True, ncol=5
)
# plt.show()
print(week_count)
