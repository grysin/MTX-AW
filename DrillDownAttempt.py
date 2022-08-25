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

current_datetime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
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

    statement = "SELECT MTX_JAM_STAT_DATA.ALID, MTX_JAM_STAT_DATA.HANDLERNAME, MTX_JAM_STAT_ALARMINFO.ALARMTEXT, MTX_JAM_STAT_ALARMINFO.GROUPID, NVL(MTX_JAM_STAT_ALARMINFO.SUBGROUPID, 'NO_SUB_GROUP') AS SUBGROUPID, COUNT(MTX_JAM_STAT_DATA.ALID) AS COUNT FROM MTX_JAM_STAT_DATA LEFT JOIN MTX_JAM_STAT_ALARMINFO ON MTX_JAM_STAT_ALARMINFO.ALID = MTX_JAM_STAT_DATA.ALID WHERE MTX_JAM_STAT_DATA.WEEK >= "
    statement = statement + str(start_week)
    statement = statement + "AND YEAR = " + str(current_year)
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

    # print(group_count_data)
    return


initial_df()


def Plot1():
    global fig1
    initial_df()
    del fig1
    fig1 = group_count_data.T.plot.bar(
        labels={"value": "Count", "index": "Handler"},
        title=f"Past {selected_duration} Week Alarm Summary: Handler Focus",
    )
    fig1.update_xaxes(categoryorder="total descending")
    fig1.update_layout(legend_title_text="Alarm Type")
    return fig1


# Dash app layout
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = dbc.Container(
    [
        dbc.Card(
            [
                dbc.Button(
                    "🡠",
                    id="back-button",
                    outline=True,
                    size="sm",
                    className="mt-2 ml-2 col-1",
                    style={"display": "none"},
                ),
                dcc.Graph(id="graph", figure=Plot1()),
            ],
        )
    ]
)


@app.callback(
    Output("graph", "figure"),
    Output("back-button", "style"),  # to hide/unhide the back button
    Input("graph", "clickData"),  # for getting the vendor name from graph
    Input("back-button", "n_clicks"),
)
def drilldown(click_data, n_clicks):
    ctx = dash.callback_context
    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
    if trigger_id == "graph":
        if click_data is not None:
            handler = click_data["points"][0]["label"]
            group_number = handler_label = click_data["points"][0]["curveNumber"]
            group = Unique_Group[group_number]
            drill_down_data = df[(df.HANDLERNAME == handler) & (df.GROUPID == group)]
            # print(drill_down_data)
            drill_down_data = drill_down_data[["ALID", "COUNT", "ALARMTEXT"]]
            drill_down_data["ALID"] = drill_down_data["ALID"].astype(str)
            fig1 = px.bar(drill_down_data, x="ALID", y="COUNT", color="ALID")
            fig1.update_layout(title=f"{handler} {group} Specific Issues")
            fig1.update_xaxes(
                categoryorder="total descending", ticks="outside", tickson="boundaries"
            )
            return fig1, {"display": "block"}
        else:
            return Plot1(), {"display": "none"}
    else:
        return Plot1(), {"display": "none"}


app.run_server(debug=True)
