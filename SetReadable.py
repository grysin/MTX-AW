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
from dash import html
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

current_datetime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
current_week = date.today().isocalendar()[1]
current_year = date.today().isocalendar()[0]
pd.options.plotting.backend = "plotly"

selected_duration = 6
start_week = current_week - selected_duration
weeks = list(np.arange(start=start_week, stop=current_week + 1, step=1))


def initial_df():
    global group_count_data
    global Unique_Group

    statement = "SELECT MTX_JAM_STAT_DATA.ALID, MTX_JAM_STAT_DATA.HANDLERNAME, MTX_JAM_STAT_ALARMINFO.GROUPID, NVL(MTX_JAM_STAT_ALARMINFO.SUBGROUPID, 'NO_SUB_GROUP') AS SUBGROUPID, COUNT(MTX_JAM_STAT_DATA.ALID) AS COUNT FROM MTX_JAM_STAT_DATA LEFT JOIN MTX_JAM_STAT_ALARMINFO ON MTX_JAM_STAT_ALARMINFO.ALID = MTX_JAM_STAT_DATA.ALID WHERE MTX_JAM_STAT_DATA.WEEK >= "
    statement = statement + str(start_week)
    statement = statement + "AND YEAR = " + str(current_year)
    statement = (
        statement
        + " GROUP BY MTX_JAM_STAT_DATA.ALID, MTX_JAM_STAT_DATA.HANDLERNAME,MTX_JAM_STAT_ALARMINFO.GROUPID, MTX_JAM_STAT_ALARMINFO.SUBGROUPID ORDER BY COUNT DESC"
    )

    sql_query = pd.read_sql_query(statement, conn)
    df = pd.DataFrame(
        sql_query, columns=["ALID", "HANDLERNAME", "GROUPID", "SUBGROUPID", "COUNT"]
    )

    print("df", df)

    Unique_Group = df["GROUPID"].sort_values(ascending=True).unique()
    print(Unique_Group)

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

    # print(group_count_data)
    return


initial_df()
