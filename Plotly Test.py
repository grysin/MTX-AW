# Plotly Test

# Report plot 1
# Past 6 weeks, get pareto of alarms

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
import dash
from dash import dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

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

current_week = date.today().isocalendar()[1]

selected_duration = 6
start_week = current_week - selected_duration
weeks = list(np.arange(start=start_week, stop=current_week + 1, step=1))


statement = "SELECT MTX_JAM_STAT_DATA.ALID, MTX_JAM_STAT_DATA.HANDLERNAME, MTX_JAM_STAT_GROUPINGS.GROUPID, COUNT(MTX_JAM_STAT_DATA.ALID) AS COUNT FROM MTX_JAM_STAT_DATA LEFT JOIN MTX_JAM_STAT_GROUPINGS ON MTX_JAM_STAT_GROUPINGS.ALID = MTX_JAM_STAT_DATA.ALID WHERE MTX_JAM_STAT_DATA.WEEK > "
statement = statement + str(start_week)
statement = (
    statement
    + " GROUP BY MTX_JAM_STAT_DATA.ALID, MTX_JAM_STAT_DATA.HANDLERNAME,MTX_JAM_STAT_GROUPINGS.GROUPID ORDER BY COUNT DESC"
)

sql_query = pd.read_sql_query(statement, conn)
df = pd.DataFrame(sql_query, columns=["ALID", "HANDLERNAME", "GROUPID", "COUNT"])

Unique_Group = df["GROUPID"].sort_values(ascending=True).unique()

# Dataframe that plot will be generated from
no_group_alids = list()
for i, row in df.iterrows():
    alid = row[0]
    handler = row[1]
    group = row[2]
    count = row[3]
    if not group:
        no_group_explain = handler + ":" + str(alid) + ", " + str(count)
        no_group_alids.append(no_group_explain)
print("No Group ALIDs (Group is null): \n", no_group_alids)
no_desc_alid = list()


group_count_data = pd.DataFrame(columns=Handlers)

# SETTING UP FIGURE 1
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

print("No Desc ALIDs (Group is NO_DESC): \n", no_desc_alid)
pd.options.plotting.backend = "plotly"


def Plot1():

    fig = group_count_data.T.plot.bar(
        labels={"value": "Count", "index": "Handler"},
        title="Past 6 Week Alarm Summary: Handler Focus",
    )
    fig.update_xaxes(categoryorder="total descending")
    fig.update_layout(legend_title_text="Alarm Type")
    fig.show()
    return


def Plot2():
    fig2 = group_count_data.plot.bar(
        labels={"value": "Count", "index": "Alarm Type"},
        title="Past 6 Week Alarm Summary: Alarm Group Focus",
    )
    fig2.update_xaxes(categoryorder="total descending")
    fig2.update_layout(legend_title_text="Handler")
    fig2.show()
    return


def Plot3():
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
    return


# WEEK COUNT
def Plot4():
    statement2 = "SELECT MTX_JAM_STAT_DATA.HANDLERNAME, MTX_JAM_STAT_DATA.WEEK, COUNT(MTX_JAM_STAT_DATA.ALID) AS COUNT FROM MTX_JAM_STAT_DATA WHERE WEEK >= "
    statement2 = statement2 + str(start_week)
    statement2 = statement2 + " AND WEEK <= "
    statement2 = statement2 + str(current_week)
    statement2 = statement2 + " GROUP BY HANDLERNAME, WEEK ORDER BY HANDLERNAME DESC"

    sql_query2 = pd.read_sql_query(statement2, conn)
    df2 = pd.DataFrame(sql_query2, columns=["HANDLERNAME", "WEEK", "COUNT"])

    handler_week_count = pd.DataFrame(columns=weeks)

    for index, handler in enumerate(Handlers):
        Y = list()
        for week in weeks:
            handler_match = df2["HANDLERNAME"] == handler
            week_match = df2["WEEK"] == week
            count = df2["COUNT"][handler_match & week_match]
            count = list(count)
            try:
                count = count[0]
            except IndexError:
                count = 0
            Y.append(count)
        handler_week_count.loc[handler] = Y

    fig4 = handler_week_count.T.plot(
        labels={"value": "Count", "index": "Work Week"},
        title="Number of Alarms on Each Handler Past 6 Weeks",
    )
    fig4.update_layout(legend_title_text="Handler")
    fig4.show()
    return


def Plot5():
    statement3 = "SELECT MTX_JAM_STAT_DATA.ALID, MTX_JAM_STAT_DATA.WEEK, MTX_JAM_STAT_DATA.HANDLERNAME, MTX_JAM_STAT_GROUPINGS.GROUPID, COUNT(MTX_JAM_STAT_DATA.ALID) AS COUNT FROM MTX_JAM_STAT_DATA LEFT JOIN MTX_JAM_STAT_GROUPINGS ON MTX_JAM_STAT_GROUPINGS.ALID = MTX_JAM_STAT_DATA.ALID WHERE MTX_JAM_STAT_DATA.WEEK >= "
    statement3 = statement3 + str(start_week)
    statement3 = statement3 + " AND MTX_JAM_STAT_DATA.WEEK <= "
    statement3 = statement3 + str(current_week)
    statement3 = (
        statement3
        + "GROUP BY MTX_JAM_STAT_DATA.ALID, MTX_JAM_STAT_DATA.WEEK, MTX_JAM_STAT_DATA.HANDLERNAME, MTX_JAM_STAT_GROUPINGS.GROUPID"
    )

    sql_query3 = pd.read_sql_query(statement3, conn)
    df3 = pd.DataFrame(
        sql_query3, columns=["ALID", "WEEK", "HANDLERNAME", "GROUPID", "COUNT"]
    )

    alarmgroup_week_count = pd.DataFrame(columns=weeks)

    for index, group in enumerate(Unique_Group):
        if group is None:
            continue
        Y = list()
        for week in weeks:
            handler_match = df3["GROUPID"] == group
            week_match = df3["WEEK"] == week
            count = df3["COUNT"][handler_match & week_match]
            sumation = count.sum()
            Y.append(sumation)
        alarmgroup_week_count.loc[group] = Y

    fig5 = alarmgroup_week_count.T.plot(
        labels={"value": "Count", "index": "Work Week"},
        title="Number of Alarms for each Alarm Group Past 6 Weeks",
    )
    fig5.update_layout(legend_title_text="Alarm Type")
    fig5.show()
    return
