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
fig, ax = plt.subplots(figsize=(10, 6))
fig.canvas.manager.set_window_title("MTX Jam Stats Plot 3")
colormap = plt.get_cmap("hsv")
colors = [colormap(i) for i in np.linspace(0, 1, len(Handlers))]

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
    ax.plot(weeks, Y, label=handler, color=colors[index])

plt.title("Past 6 Week Summary \n Each Week Sum")
plt.ylabel("Count")
plt.xlabel("Work Week")
ax.set_xticks(np.arange(min(weeks), max(weeks) + 1, 1.0))
box = ax.get_position()
ax.set_position([box.x0, box.y0 + box.height * 0.1, box.width, box.height * 0.8])
ax.legend(
    loc="upper center", bbox_to_anchor=(0.5, -0.1), fancybox=True, shadow=True, ncol=5
)
plt.show()
