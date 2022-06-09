import cx_Oracle
import os
import csv
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# set Oracle client
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

# create graph of 10 most common all time
data_select = "SELECT ALID, HANDLERNAME, COUNT(ALID) AS COUNT FROM MTX_ALARM_LOG GROUP BY ALID, HANDLERNAME"
# data_select = "SELECT HANDLERNAME, ALID, ALARMTEXT AS DESCRIPTION, ELAPSEDTIME AS DURATION FROM MTX_ALARM_LOG"

sql_query = pd.read_sql_query(data_select, conn)
df = pd.DataFrame(sql_query, columns=["HANDLERNAME", "ALID", "COUNT"])

Handlers = df["HANDLERNAME"].sort_values(ascending=True).unique()
print(Handlers)
Unique_ALID = df["ALID"].sort_values(ascending=True).unique()

instance_data = pd.DataFrame(columns=Handlers)

fig = plt.figure(
    num="Instances of ALIDs", figsize=(22, 10), dpi=80, facecolor="w", edgecolor="k"
)
fig.canvas.set_window_title("Instances")

for alid in Unique_ALID:
    Y = list()
    for handler in Handlers:
        statement = (
            "SELECT COUNT(ALID) AS COUNT FROM MTX_ALARM_LOG WHERE HANDLERNAME = '"
            + str(handler)
            + "' AND ALID = '"
            + str(alid)
            + "'"
        )
        cursor.execute(statement)
        result = cursor.fetchall()
        count = result[0][0]
        Y.append(count)
    instance_data.loc[alid] = Y
    plt.bar(Handlers, Y, label=alid)

print(instance_data)

plt.title("Instances of Alarm Codes")
plt.xlabel("Handler")
plt.ylabel("Number of Times Alarm Occured")
plt.show()
