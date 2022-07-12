# Report plot 2
# Past 6 weeks, get pareto of alarms

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

week = date.today().isocalendar()[1]
six_weeks_back = week - 6

statement = "SELECT MTX_JAM_STAT_DATA.ALID, MTX_JAM_STAT_DATA.HANDLERNAME, MTX_JAM_STAT_GROUPINGS.GROUPID,  FROM MTX_JAM_STAT_DATA LEFT JOIN MTX_JAM_STAT_GROUPINGS ON MTX_JAM_STAT_GROUPINGS.ALID = MTX_JAM_STAT_DATA.ALID WHERE MTX_JAM_STAT_DATA.WEEK > "
statement = statement + str(six_weeks_back)
statement = (
    statement
    + " GROUP BY MTX_JAM_STAT_DATA.ALID, MTX_JAM_STAT_DATA.HANDLERNAME,MTX_JAM_STAT_GROUPINGS.GROUPID ORDER BY COUNT DESC"
)

sql_query = pd.read_sql_query(statement, conn)
df = pd.DataFrame(sql_query, columns=["ALID", "HANDLERNAME", "GROUPID", "COUNT"])

print(df)
