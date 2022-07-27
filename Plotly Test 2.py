# Report plot 1
# Past 6 weeks

from cProfile import label
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
six_weeks_back = current_week - 6
weeks = list(np.arange(start=six_weeks_back, stop=current_week + 1, step=1))

statement2 = "SELECT MTX_JAM_STAT_DATA.HANDLERNAME, MTX_JAM_STAT_DATA.WEEK, COUNT(MTX_JAM_STAT_DATA.ALID) AS COUNT FROM MTX_JAM_STAT_DATA WHERE WEEK >= "
statement2 = statement2 + str(six_weeks_back)
statement2 = statement2 + " AND WEEK <= "
statement2 = statement2 + str(current_week)
statement2 = statement2 + " GROUP BY HANDLERNAME, WEEK ORDER BY HANDLERNAME DESC"

sql_query2 = pd.read_sql_query(statement2, conn)
df2 = pd.DataFrame(sql_query2, columns=["HANDLERNAME", "WEEK", "COUNT"])


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

week_count = pd.DataFrame(columns=weeks)

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
    week_count.loc[handler] = Y

pd.options.plotting.backend = "plotly"
fig4 = week_count.T.plot()
fig4.update_xaxes(categoryorder="total descending")
fig4.show()
