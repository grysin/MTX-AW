# MTX ALARM ANALYSIS

from tracemalloc import start
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
from datetime import timedelta
from fpdf import FPDF
import dash
from dash import dcc
import dash_bootstrap_components as dbc
from dash import html
from dash.dependencies import Input, Output

# END OF IMPORTS #
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

# SET PLOTTING DEFAULT AS PLOTLY
pd.options.plotting.backend = "plotly"


# CONNECT TO ORACLE
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

# SET UP INITIAL START TIME AND END TIME FOR DATE PICKER DATE FUNCTION
init_endtime = datetime.now()
init_starttime = init_endtime - (timedelta(weeks=6))

# FUNCTION TO CONVERT A DATE INTO A SET_TIME FORMAT
def set_time_convert(time):
    time = date.toordinal(time)
    time = 86400 * (time - 719163)
    return time


# FUNCTION TO CONVERT A SET_TIME INTO A DATE
def set_time_decode(time):
    time = int(int(time) / 86400 + 719163)
    time = date.fromordinal(time)
    return time


# the initial time (6 weeks back) in set time format
sql_init_endtime = set_time_convert(init_endtime)
sql_init_starttime = set_time_convert(init_starttime)
start_date = str(init_starttime.date())
end_date = str(init_endtime.date())

# DATAFRAME THAT is used to create Handler and Alarm Paretos
def initial_df():
    global df
    global group_count_data
    global Unique_Group
    global sql_init_endtime
    global sql_init_starttime

    statement = "SELECT MTX_JAM_STAT_DATA.ALID, MTX_JAM_STAT_DATA.HANDLERNAME, MTX_JAM_STAT_ALARMINFO.ALARMTEXT, MTX_JAM_STAT_ALARMINFO.GROUPID, NVL(MTX_JAM_STAT_ALARMINFO.SUBGROUPID, 'NO_SUB_GROUP') AS SUBGROUPID, COUNT(MTX_JAM_STAT_DATA.ALID) AS COUNT FROM MTX_JAM_STAT_DATA LEFT JOIN MTX_JAM_STAT_ALARMINFO ON MTX_JAM_STAT_ALARMINFO.ALID = MTX_JAM_STAT_DATA.ALID WHERE MTX_JAM_STAT_DATA.SET_TIME >= "
    statement = statement + str(sql_init_starttime)
    statement = (
        statement + " AND MTX_JAM_STAT_DATA.SET_TIME <= " + str(sql_init_endtime)
    )
    statement = (
        statement
        + " GROUP BY MTX_JAM_STAT_DATA.ALID, MTX_JAM_STAT_DATA.HANDLERNAME, MTX_JAM_STAT_ALARMINFO.ALARMTEXT, MTX_JAM_STAT_ALARMINFO.GROUPID, MTX_JAM_STAT_ALARMINFO.SUBGROUPID ORDER BY COUNT DESC"
    )

    sql_query = pd.read_sql_query(statement, conn)
    df = pd.DataFrame(
        sql_query,
        columns=["ALID", "HANDLERNAME", "ALARMTEXT", "GROUPID", "SUBGROUPID", "COUNT"],
    )

    # print("df", df)

    Unique_Group = df["GROUPID"].sort_values(ascending=True).unique()
    # print(Unique_Group)

    # Dataframe that plot will be generated from
    no_group_alids = list()
    for i, row in df.iterrows():
        alid = row[0]
        handler = row[1]
        group = row[2]
        sub_group = row[3]
        count = row[4]
        if not group:
            no_group_explain = handler + ":" + str(alid) + ", " + str(count)
            no_group_alids.append(no_group_explain)
    # print("No Group ALIDs (Group is null): \n", no_group_alids)
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
    return


# Handler Pareto
def Plot1():
    global fig1
    global sql_init_endtime
    global sql_init_starttime
    initial_df()
    start_date = set_time_decode(sql_init_starttime)
    end_date = set_time_decode(sql_init_endtime)

    fig1 = group_count_data.T.plot.bar(
        labels={"value": "Count", "index": "Handler"},
        title=f"Handler Pareto {start_date} to {end_date}",
    )
    fig1.update_xaxes(categoryorder="total descending")
    fig1.update_layout(legend_title_text="Alarm Type")
    return fig1


# Alarm Pareto
def Plot2():
    global fig2
    global sql_init_endtime
    global sql_init_starttime
    initial_df()
    fig2 = group_count_data.plot.bar(
        labels={"value": "Count", "index": "Alarm Type"},
        title=f"Alarm Pareto {start_date} to {end_date}",
    )
    fig2.update_xaxes(categoryorder="total descending")
    fig2.update_layout(legend_title_text="Handler")
    return fig2


# Handler Trend
def Plot3():
    global fig3
    global sql_init_endtime
    global sql_init_starttime
    statement3 = "SELECT MTX_JAM_STAT_DATA.HANDLERNAME, MTX_JAM_STAT_DATA.WEEK, COUNT(MTX_JAM_STAT_DATA.ALID) AS COUNT FROM MTX_JAM_STAT_DATA WHERE MTX_JAM_STAT_DATA.SET_TIME >= "
    statement3 = statement3 + str(sql_init_starttime)
    statement3 = (
        statement3 + " AND MTX_JAM_STAT_DATA.SET_TIME <= " + str(sql_init_endtime)
    )
    statement3 = statement3 + " GROUP BY HANDLERNAME, WEEK ORDER BY HANDLERNAME DESC"

    sql_query3 = pd.read_sql_query(statement3, conn)
    df3 = pd.DataFrame(sql_query3, columns=["HANDLERNAME", "WEEK", "COUNT"])
    weeks = df3["WEEK"].sort_values(ascending=True).unique()
    handler_week_count = pd.DataFrame(columns=weeks)
    selected_duration = max(weeks) - min(weeks)

    for index, handler in enumerate(Handlers):
        Y = list()
        for week in weeks:
            handler_match = df3["HANDLERNAME"] == handler
            week_match = df3["WEEK"] == week
            count = df3["COUNT"][handler_match & week_match]
            count = list(count)
            try:
                count = count[0]
            except IndexError:
                count = 0
            Y.append(count)
        handler_week_count.loc[handler] = Y

    fig3 = handler_week_count.T.plot(
        labels={"value": "Count", "index": "Work Week"},
        title=f"Handler Trend {start_date} to {end_date}",
    )
    fig3.update_layout(legend_title_text="Handler")
    return fig3


# Alarm Trend
def Plot4():
    global fig4
    global sql_init_endtime
    global sql_init_starttime
    statement4 = "SELECT MTX_JAM_STAT_DATA.ALID, MTX_JAM_STAT_DATA.WEEK, MTX_JAM_STAT_DATA.HANDLERNAME, MTX_JAM_STAT_GROUPINGS.GROUPID, COUNT(MTX_JAM_STAT_DATA.ALID) AS COUNT FROM MTX_JAM_STAT_DATA LEFT JOIN MTX_JAM_STAT_GROUPINGS ON MTX_JAM_STAT_GROUPINGS.ALID = MTX_JAM_STAT_DATA.ALID WHERE MTX_JAM_STAT_DATA.SET_TIME >= "
    statement4 = statement4 + str(sql_init_starttime)
    statement4 = statement4 + " AND MTX_JAM_STAT_DATA.SET_TIME <= "
    statement4 = statement4 + str(sql_init_endtime)
    statement4 = (
        statement4
        + "GROUP BY MTX_JAM_STAT_DATA.ALID, MTX_JAM_STAT_DATA.WEEK, MTX_JAM_STAT_DATA.HANDLERNAME, MTX_JAM_STAT_GROUPINGS.GROUPID"
    )

    sql_query4 = pd.read_sql_query(statement4, conn)
    df4 = pd.DataFrame(
        sql_query4, columns=["ALID", "WEEK", "HANDLERNAME", "GROUPID", "COUNT"]
    )
    weeks = df4["WEEK"].sort_values(ascending=True).unique()
    alarmgroup_week_count = pd.DataFrame(columns=weeks)

    for index, group in enumerate(Unique_Group):
        if group is None:
            continue
        Y = list()
        for week in weeks:
            handler_match = df4["GROUPID"] == group
            week_match = df4["WEEK"] == week
            count = df4["COUNT"][handler_match & week_match]
            sumation = count.sum()
            Y.append(sumation)
        alarmgroup_week_count.loc[group] = Y

    fig4 = alarmgroup_week_count.T.plot(
        labels={"value": "Count", "index": "Work Week"},
        title=f"Alarm Trend {start_date} to {end_date}",
    )
    fig4.update_layout(legend_title_text="Alarm Type")
    return fig4


app = dash.Dash(__name__)

app.layout = html.Div(
    [
        dcc.DatePickerRange(
            id="date-picker-range",
            min_date_allowed=date(2022, 1, 1),
            max_date_allowed=datetime.today(),
            end_date=datetime.today(),
        ),
        dcc.Dropdown(
            options=[
                "Handler Pareto",
                "Alarm Pareto",
                "Handler Trend",
                "Alarm Trend",
            ],
            value="Handler Pareto",
            id="dropdown",
        ),
        dcc.Graph(id="Plot", figure={}),
        html.Button("Download Graph Content", id="download_button"),
        dcc.Download(id="download_content"),
    ]
)

# CALLBACK THAT CHANGES GRAPH BASED ON DROPDOWN MENU
# @app.callback(Output("Plot", "figure"), Input("dropdown", "value"))
# def dropdown_update(dropdown_value):
#     if dropdown_value == "Handler Pareto":
#         return Plot1()
#     if dropdown_value == "Alarm Pareto":
#         return Plot2()
#     if dropdown_value == "Handler Trend":
#         return Plot3()
#     if dropdown_value == "Alarm Trend":
#         return Plot4()


# CALLBACK THAT UPDATES GRAPHS BASED ON SELECTED DATE AND DROPDOWN SELECTION
@app.callback(
    Output("Plot", "figure"),
    [
        Input("dropdown", "value"),
        Input("date-picker-range", "start_date"),
        Input("date-picker-range", "end_date"),
    ],
)
def date_update(dropdown_value, date_start, date_end):
    global sql_init_endtime
    global sql_init_starttime

    date_end = date_end.split("T")[0]
    if date_start is None:
        date_start = datetime.strptime(date_end, "%Y-%m-%d") - timedelta(weeks=6)
    else:
        date_start = date_start.split("T")[0]
        date_start = datetime.strptime(date_start, "%Y-%m-%d")

    date_end = datetime.strptime(date_end, "%Y-%m-%d")
    sql_init_endtime = set_time_convert(date_end)
    sql_init_starttime = set_time_convert(date_start)

    if dropdown_value == "Handler Pareto":
        return Plot1()
    if dropdown_value == "Alarm Pareto":
        return Plot2()
    if dropdown_value == "Handler Trend":
        return Plot3()
    if dropdown_value == "Alarm Trend":
        return Plot4()


# MULTIPLE CALLBACKS TRIGGERED ON CLICK, DRILL DOWN INTO EACH GRAPH

# CALLBACK THAT ACTS AS A BACK BUTTON FROM DRILL DOWN

# CALLBACK THAT SAVES DATA CURRENTLY DISPLAYED ON THE GRAPH INTO A EXCEL FILE

app.run_server(debug=True)
