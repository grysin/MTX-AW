import cx_Oracle
import os
import csv
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import date
from datetime import datetime


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

oracle_statement = "SELECT SET_READABLE AS TIME, ALARMTEXT FROM MTX_JAM_STAT_DATA WHERE HANDLERNAME = 'MTXA05' AND WEEK > 22 ORDER BY TIME DESC"

sql_query = pd.read_sql_query(oracle_statement, conn)
initial_oracle = pd.DataFrame(sql_query, columns=["TIME", "ALARMTEXT"])
initial_oracle.sort_values(by=["TIME"])

timeline_data = pd.DataFrame(columns=["Time", "Data Source", "Comments/Alarm"])

for row in initial_oracle.iterrows():
    date_time = row[1][0]
    date_time = datetime.strptime(date_time, "%H:%M:%S %d-%b-%Y")
    print(date_time)
    alarm_text = row[1][1]
    new_row = [date_time, "Alarm", alarm_text]
    insert_index = len(timeline_data)
    timeline_data.loc[insert_index] = new_row

file = r"Documentation/A05_EMS_6_28.csv"
csv_file = open(file)
csv_data = csv.reader(csv_file)
csv_rows = list(csv_data)
csv_rows = csv_rows[2:]

for row in csv_rows:
    status = row[0]
    user = row[2]
    date_time = row[3]
    date_time = datetime.strptime(date_time, "%m/%d/%Y %H:%M")
    ems_comments = row[5]
    comments = "Status: " + status + ", User: " + user + ", Comments: " + ems_comments
    new_row = [date_time, "EMS", comments]
    insert_index = len(timeline_data)
    timeline_data.loc[insert_index] = new_row

timeline_data = timeline_data.sort_values(by=["Time"])
timeline_data.to_csv("A05_EMS_JAM_6_28.csv")
