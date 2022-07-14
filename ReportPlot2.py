# Report plot 1
# Past 6 weeks

from cProfile import label
import cx_Oracle
import os
import csv
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import handler_kit_Tsense_calibrate_config as config
from datetime import date
from datetime import datetime
from fpdf import FPDF

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

current_week = date.today().isocalendar()[1]
six_weeks_back = current_week - 6
weeks = list(np.arange(start=six_weeks_back, stop=current_week + 1, step=1))

statement = "SELECT MTX_JAM_STAT_DATA.HANDLERNAME, MTX_JAM_STAT_DATA.WEEK, COUNT(MTX_JAM_STAT_DATA.ALID) AS COUNT FROM MTX_JAM_STAT_DATA WHERE WEEK >= "
statement = statement + str(six_weeks_back)
statement = statement + " AND WEEK <= "
statement = statement + str(current_week)
statement = statement + " GROUP BY HANDLERNAME, WEEK ORDER BY HANDLERNAME DESC"

sql_query = pd.read_sql_query(statement, conn)
df = pd.DataFrame(sql_query, columns=["HANDLERNAME", "WEEK", "COUNT"])


try:
    Handlers = config.handler_list
except AttributeError:
    Handlers = [
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

week_count = pd.DataFrame(columns=weeks)
# figsize is width by height

num_handlers = len(Handlers)
half_point_handlers = round(num_handlers / 2)


fig, (ax, ax2) = plt.subplots(figsize=(10, 6), ncols=1, nrows=2, sharex=True)
fig.canvas.manager.set_window_title("MTX Jam Stats Plot 3")
colormap = plt.get_cmap("hsv")
colors = [colormap(i) for i in np.linspace(0, 1, len(Handlers))]
half_colors = [colormap(i) for i in np.linspace(0, 1, half_point_handlers)]

for index, handler in enumerate(Handlers):
    Y = list()
    for week in weeks:
        handler_match = df["HANDLERNAME"] == handler
        week_match = df["WEEK"] == week
        count = df["COUNT"][handler_match & week_match]
        count = list(count)
        try:
            count = count[0]
        except IndexError:
            count = 0
        Y.append(count)
    week_count.loc[handler] = Y
    if (index + 1) <= half_point_handlers:
        ax.plot(weeks, Y, label=handler, color=half_colors[index])
    else:
        ax2.plot(
            weeks, Y, label=handler, color=half_colors[index - half_point_handlers]
        )
plt.rcParams.update({"font.sans-serif": "Garamond"})
plt.suptitle("Past 6 Week Summary \n Each Week Sum")
plt.ylabel("Count")
plt.xlabel("Work Week")
ax.set_xticks(np.arange(min(weeks), max(weeks) + 1, 1.0))
ax.legend()
ax2.legend()
plt.show()
