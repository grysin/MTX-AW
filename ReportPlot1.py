# Report plot 1
# Past 6 weeks, get pareto of alarms

from hashlib import new
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
fig, ax = plt.subplots(figsize=(10, 6))
fig.canvas.set_window_title("MTX Jam Stat Plot")
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
new_handler_order_counts = list(new_handler_order)
new_handler_order = list(new_handler_order.keys())
plot_x_labels = list()
table_x_labels = list()

for index, value in enumerate(new_handler_order):
    plot_x_label = value.strip("MTX") + "\n" + str(new_handler_order_counts[index])
    plot_x_labels.append(plot_x_label)
    table_x_label = value.strip("MTX")
    table_x_labels.append(table_x_label)


# print(group_count_data)
reordered_data = group_count_data[new_handler_order]
# print(reordered_data)

for index, group in enumerate(Unique_Group):
    # print("index:", index)
    # print("group:", group)
    if group is None:
        continue
    Y = list(reordered_data.loc[group])
    # print("Y:", Y)
    if index == 0:
        ax.bar(plot_x_labels, Y, label=group, color=colors[index])
        Old_Y = Y
    else:
        # print("Old Y:", Old_Y)
        ax.bar(plot_x_labels, Y, label=group, color=colors[index], bottom=Old_Y)
        Old_Y = [x + y for x, y in zip(Old_Y, Y)]


print("No Desc ALIDs: \n", no_desc_alid, "\n")
print(reordered_data, "\n")
ax.tick_params(axis="x", labelsize=8)
plt.title("Past 6 Week Summary")
plt.ylabel("Count")
plt.rcParams.update({"font.sans-serif": "Garamond"})
ax.legend(fancybox=True, shadow=True, ncol=4)

# figsize is width by height
fig2, ax2 = plt.subplots(figsize=(10, 6))
# hides plot lines
fig2.patch.set_visible(False)
ax2.axis("off")
ax2.axis("tight")
fig2.canvas.set_window_title("MTX Jam Stat Table")
table = ax2.table(
    cellText=reordered_data.values,
    colLabels=table_x_labels,
    rowLabels=reordered_data.index,
    loc="center",
)
table.auto_set_font_size(False)
table.set_fontsize(10)
plt.show()
