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
