# Plotly Test

# Report plot 1
# Past 6 weeks, get pareto of alarms

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
fig1 = 0
# get data for drill down attempt

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

init_endtime = datetime.now()
init_starttime = init_endtime - (timedelta(weeks=6))


def set_time_convert(time):
    time = date.toordinal(time)
    time = 86400 * (time - 719163)
    return time


def set_time_decode(time):
    time = int(int(time) / 86400 + 719163)
    time = date.fromordinal(time)
    return time


global sql_init_endtime
global sql_init_starttime

sql_init_endtime = set_time_convert(init_endtime)
sql_init_starttime = set_time_convert(init_starttime)


# print("SQL INITIAL END:", sql_init_endtime)
# print("SQL INITIAL START", sql_init_starttime)

current_week = date.today().isocalendar()[1]
current_year = date.today().isocalendar()[0]
pd.options.plotting.backend = "plotly"

selected_duration = 6
start_week = current_week - selected_duration
weeks = list(np.arange(start=start_week, stop=current_week + 1, step=1))


def initial_df():
    global df
    global group_count_data
    global Unique_Group
    global init_starttime

    init_endtime = set_time_decode(sql_init_endtime)
    print("INIT BS TYPE:", type(init_endtime))
    init_starttime = set_time_decode(sql_init_starttime)
    init_starttime = init_starttime.strftime("%Y-%m-%d")

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

    # print("GROUP COUNT DATA", group_count_data)
    return


def Plot1():
    global fig1
    initial_df()
    # print("PLOT 1 Function triggered")
    # print(group_count_data)
    fig1 = group_count_data.T.plot.bar(
        labels={"value": "Count", "index": "Handler"},
        title=f"Week Alarm Summary: Handler Focus {init_starttime} to {init_endtime}",
    )
    fig1.update_xaxes(categoryorder="total descending")
    fig1.update_layout(legend_title_text="Alarm Type")
    return fig1


app = dash.Dash(__name__)

app.layout = html.Div(
    [
        dcc.DatePickerRange(
            id="date-picker-range",
            min_date_allowed=date(2022, 1, 1),
            max_date_allowed=datetime.today(),
            end_date=datetime.today(),
        ),
        dcc.Graph(id="Plot-1", figure=Plot1()),
    ]
)


@app.callback(
    Output(component_id="Plot-1", component_property="figure"),
    [
        Input(component_id="date-picker-range", component_property="start_date"),
        Input(component_id="date-picker-range", component_property="end_date"),
    ],
)
def date_update_plot1(start_date, end_date):
    global sql_init_endtime
    global sql_init_starttime
    global init_endtime
    global init_starttime

    if start_date is not None:
        start_date_list = start_date.split("T")
        start_date = start_date_list[0]

        start_date = date.fromisoformat(start_date)
        init_starttime = start_date
        sql_init_starttime = set_time_convert(start_date)

        print(sql_init_starttime)

    if end_date is not None:
        # START_DATE is a str in the format 2022-08-23T13:12:26.165775
        end_date_list = end_date.split("T")
        end_date = end_date_list[0]
        init_endtime = end_date
        end_date = date.fromisoformat(end_date)
        init_endtime = end_date
        sql_init_endtime = set_time_convert(end_date)
    Plot1()

    return fig1


app.run_server(debug=True)
