# Report plot 1
# Past 6 weeks, get pareto of alarms

import cx_Oracle
import os
import csv
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from IPython.display import display
import handler_kit_Tsense_calibrate_config as config
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

week = date.today().isocalendar()[1]
six_weeks_back = week - 6

statement = "SELECT MTX_JAM_STAT_DATA.ALID, MTX_JAM_STAT_DATA.HANDLERNAME, MTX_JAM_STAT_GROUPINGS.GROUPID, COUNT(MTX_JAM_STAT_DATA.ALID) AS COUNT FROM MTX_JAM_STAT_DATA LEFT JOIN MTX_JAM_STAT_GROUPINGS ON MTX_JAM_STAT_GROUPINGS.ALID = MTX_JAM_STAT_DATA.ALID WHERE MTX_JAM_STAT_DATA.WEEK > "
statement = statement + str(six_weeks_back)
statement = (
    statement
    + " GROUP BY MTX_JAM_STAT_DATA.ALID, MTX_JAM_STAT_DATA.HANDLERNAME,MTX_JAM_STAT_GROUPINGS.GROUPID ORDER BY COUNT DESC"
)

sql_query = pd.read_sql_query(statement, conn)
df = pd.DataFrame(sql_query, columns=["ALID", "HANDLERNAME", "GROUPID", "COUNT"])


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

Unique_Group = df["GROUPID"].sort_values(ascending=True).unique()

# Dataframe that plot will be generated from
group_count_data = pd.DataFrame(columns=Handlers)

# Find which codes don't have groups
# list to store alids with no group
no_group_alids = list()

for i, row in df.iterrows():
    alid = row[0]
    handler = row[1]
    group = row[2]
    count = row[3]
    if not group:
        no_group_explain = handler + ":" + str(alid) + ", " + str(count)
        no_group_alids.append(no_group_explain)
print("No Group ALIDs: \n", no_group_alids)

no_desc_alid = list()
fig, ax = plt.subplots(figsize=(15, 8.5))
fig.canvas.set_window_title("MTX Jam Stats")
colormap = plt.get_cmap("tab20")
colors = [colormap(i) for i in np.linspace(0, 1, len(Unique_Group))]

for i, group in enumerate(Unique_Group):
    if group is None:
        continue
    Y = list()
    for handler in Handlers:
        is_group = df["GROUPID"] == group
        is_handler = df["HANDLERNAME"] == handler
        sorted_df = df[is_group & is_handler]
        if group == "NO_DESC":
            if sorted_df.empty:
                pass
            else:
                for index, row in sorted_df.iterrows():
                    alid = row["ALID"]
                    count = row["COUNT"]
                    no_desc_explain = handler + ":" + str(alid) + ", " + str(count)
                    no_desc_alid.append(no_desc_explain)

        if sorted_df.empty:
            count = 0
        else:
            count = sorted_df["COUNT"].sum()
        Y.append(count)
    group_count_data.loc[group] = Y

# re order plot
new_handler_order = group_count_data.sum().sort_values(ascending=False)
new_handler_order = list(new_handler_order.keys())

reordered_data = group_count_data[new_handler_order]

for index, group in enumerate(Unique_Group):
    if group is None:
        continue
    Y = reordered_data.loc[group]
    ax.bar(x=new_handler_order, height=Y, label=group, color=colors[index])

print("No Desc ALIDs: \n", no_desc_alid, "\n")
print(reordered_data, "\n")
plt.title("Past 6 Week Summary")
plt.ylabel("Count")
box = ax.get_position()
ax.set_position([box.x0, box.y0 + box.height * 0.1, box.width, box.height * 0.9])
ax.legend(
    loc="upper center", bbox_to_anchor=(0.5, -0.05), fancybox=True, shadow=True, ncol=4
)
plt.show()
