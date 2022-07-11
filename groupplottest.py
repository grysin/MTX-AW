import cx_Oracle
import os
import csv
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from IPython.display import display
from datetime import date
from datetime import datetime

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

statement = "SELECT MTX_JAM_STAT_DATA.HANDLERNAME, MTX_JAM_STAT_GROUPINGS.GROUPID, COUNT(MTX_JAM_STAT_DATA.ALID) AS COUNT FROM MTX_JAM_STAT_DATA LEFT JOIN MTX_JAM_STAT_GROUPINGS ON MTX_JAM_STAT_GROUPINGS.ALID = MTX_JAM_STAT_DATA.ALID GROUP BY MTX_JAM_STAT_GROUPINGS.GROUPID, MTX_JAM_STAT_DATA.HANDLERNAME ORDER BY COUNT DESC"

sql_query = pd.read_sql_query(statement, conn)
df = pd.DataFrame(sql_query, columns=["HANDLERNAME", "GROUPID", "COUNT"])

Handlers = df["HANDLERNAME"].sort_values(ascending=True).unique()
Unique_Group = df["GROUPID"].sort_values(ascending=True).unique()

group_count_data = pd.DataFrame(columns=Handlers)

week = date.today().isocalendar()[1]
six_weeks_back = week - 6
print(six_weeks_back)

for i, group in enumerate(Unique_Group):
    if not group:
        print("triggered")
        group = "Other"
    Y = list()
    for handler in Handlers:
        if group == "Other":
            print("Other")
            statement = "SELECT NVL(COUNT(MTX_JAM_STAT_DATA.ALID),0) AS COUNT FROM MTX_JAM_STAT_DATA, MTX_JAM_STAT_GROUPINGS WHERE HANDLERNAME = '" + handler + "' AND WEEK = '" + six_weeks_back+ "'NOT EXISTS (SELECT null FROM MTX_JAM_STAT_GROUPINGS WHERE MTX_JAM_STAT_DATA.ALID = MTX_JAM_STAT_GROUPINGS.ALID)"
            print(statement)
        else:
            statement = "SELECT NVL(COUNT(MTX_JAM_STAT_DATA.ALID),0) AS COUNT FROM MTX_JAM_STAT_DATA, MTX_JAM_STAT_GROUPINGS WHERE MTX_JAM_STAT_DATA.ALID = MTX_JAM_STAT_GROUPINGS.ALID AND HANDLERNAME ='" + handler + "' AND WEEK > '" + six_weeks_back + "' AND MTX_JAM_STAT_GROUPINGS.GROUPID = '" + group}' "
            print(statement)

        # print("statement: \n", statement)
        cursor.execute(statement)
        result = cursor.fetchall()
        # print("result of statement: \n", result)
        count = result[0][0]
        Y.append(count)
    # print("Y", Y)
    group_count_data.loc[group] = Y

print(group_count_data.sum().sort_values(ascending=False))
print(group_count_data)

# fig size = width by hieght
fig, ax = plt.subplots(figsize=(15, 8.5))
fig.canvas.set_window_title("MTX Jam Stats")
colormap = plt.get_cmap("Set3_r")
colors = [colormap(i) for i in np.linspace(0, 1, len(Unique_Group))]

for Y in group_count_data:
    ax.bar(Handlers, Y, label=group, color=colors[i])
print(group_count_data)
duration_data = group_count_data.style.highlight_max()
display(group_count_data)


plt.title("Count of Alarm Groups")
plt.ylabel("Count")
box = ax.get_position()
ax.set_position([box.x0, box.y0 + box.height * 0.1, box.width, box.height * 0.9])
ax.legend(
    loc="upper center", bbox_to_anchor=(0.5, -0.05), fancybox=True, shadow=True, ncol=5
)
plt.show()
