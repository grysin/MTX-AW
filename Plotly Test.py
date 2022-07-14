# Plotly Test

# Report plot 1
# Past 6 weeks, get pareto of alarms

import enum
from unicodedata import category
import cx_Oracle
import os
import csv
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
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

pd.options.plotting.backend = "plotly"
fig = group_count_data.T.plot.bar()
fig.update_xaxes(categoryorder="total descending")
# fig.show()

fig2 = group_count_data.plot.bar()
fig2.update_xaxes(categoryorder="total descending")
# fig2.show()

fig3 = go.Figure(
    data=[
        go.Table(
            header={
                "values": group_count_data.reset_index().columns,
                "font": {"size": 10},
                "align": "left",
            },
            cells={"values": group_count_data.reset_index().T, "align": "left"},
        )
    ]
)
fig3.show()
