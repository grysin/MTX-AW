# Report plot 1
# Past 6 weeks, get pareto of alarms

import enum
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

# END OF IMPORTS #

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

# SETTING UP FIGURE 1

fig, ax = plt.subplots(figsize=(10, 6))
fig.canvas.manager.set_window_title("MTX Jam Stat Plot 1")
colormap = plt.get_cmap("tab20")
colors = [colormap(i) for i in np.linspace(0, 1, len(Unique_Group))]

# CREATING GROUP COUNT DATABASE #

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

# REORDERING PLOT 1
# SO WORST HANDLER IS FIRST
new_handler_order = group_count_data.sum().sort_values(ascending=False)
new_handler_order_counts = list(new_handler_order)
new_handler_order = list(new_handler_order.keys())
plot_x_labels = list()
table_x_labels = list()

# CREATING X LABELS FOR PLOT 1
for index, value in enumerate(new_handler_order):
    plot_x_label = value.strip("MTX") + "\n" + str(new_handler_order_counts[index])
    plot_x_labels.append(plot_x_label)
    table_x_label = value.strip("MTX")
    table_x_labels.append(table_x_label)

# CREATING THE REORDERED DATABASE FOR PLOT 1

# print(group_count_data)
reordered_data = group_count_data[new_handler_order]
# print(reordered_data)

# CREATING PLOT 1
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


print("No ALARMTEXT ALIDs: \n", no_desc_alid, "\n")
# print(reordered_data, "\n")
ax.tick_params(axis="x", labelsize=8)
plt.title("Past 6 Week Summary \n Handler Focus")
plt.ylabel("Count")
plt.rcParams.update({"font.sans-serif": "Garamond"})
ax.legend(fancybox=True, shadow=True, ncol=4)
# plt.show()
plt.savefig("Plot1.png", format="png", bbox_inches="tight", dpi=400)

# SETTING UP PLOT 2
# fig size is width by height
fig2, ax2 = plt.subplots(figsize=(10.5, 6))
fig2.canvas.manager.set_window_title("MTX Jam Stat Plot 2")
colormap2 = plt.get_cmap("tab20")
colors2 = [colormap2(i) for i in np.linspace(0, 1, len(Handlers))]
plot2_database = group_count_data.T

# REORDERING PLOT 2 DATA
# SO THAT WORST GROUP IS FIRST
new_plot2_order = plot2_database.sum().sort_values(ascending=False)
new_plot2_order_counts = list(new_plot2_order)
new_plot2_order = list(new_plot2_order.keys())
plot2_x_labels = list()
for index, value in enumerate(new_plot2_order):
    plot2_x_label = value + "\n" + str(new_plot2_order_counts[index])
    plot2_x_labels.append(plot2_x_label)

plot2_new_order_df = plot2_database[new_plot2_order]

for index, handler in enumerate(Handlers):
    Y = list(plot2_new_order_df.loc[handler])
    if index == 0:
        ax2.bar(plot2_x_labels, Y, label=handler, color=colors2[index])
        Old_Y = Y
    else:
        ax2.bar(plot2_x_labels, Y, label=handler, color=colors2[index], bottom=Old_Y)
        Old_Y = [x + y for x, y in zip(Old_Y, Y)]

ax2.tick_params(axis="x", labelsize=8)
plt.title("Past 6 Week Summary \n Jam Focus")
plt.ylabel("Count")
plt.rcParams.update({"font.sans-serif": "Garamond"})
ax2.legend(fancybox=True, shadow=True, ncol=5)
plt.savefig("Plot2.png", format="png", bbox_inches="tight", dpi=400)

# figsize is width by height
fig3, ax3 = plt.subplots(figsize=(10, 6))
# hides plot lines
fig3.patch.set_visible(False)
ax3.axis("off")
ax3.axis("tight")
fig3.canvas.manager.set_window_title("MTX Jam Stat Table")
table = ax3.table(
    cellText=reordered_data.values,
    colLabels=table_x_labels,
    rowLabels=reordered_data.index,
    loc="center",
    cellLoc="center",
)
table.auto_set_font_size(False)
table.set_fontsize(10)
plt.savefig("Table1.png", format="png", bbox_inches="tight", dpi=400)


pdf = FPDF()
pdf_width = 210
pdf_height = 297
pdf.add_font("Garamond", "", r"C:\Windows\Fonts\GARA.TTF", uni=True)
pdf.add_page()
pdf.set_font("Garamond", style="", size=12)
pdf.image(name="Plot1.png", x=10, y=10, w=170, h=110, type="png")
pdf.image(name="Plot2.png", x=10, y=120, w=170, h=110, type="png")
pdf.image(name="Table1.png", x=10, y=210, w=170, h=110, type="png")
pdf.output("test.pdf", "F")
print("Completed")
