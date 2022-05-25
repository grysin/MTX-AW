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
# data_select = "SELECT ALID, COUNT(ALID) AS COUNT FROM MTX_ALARM_LOG GROUP BY ALID"
data_select = "SELECT WEEK, HANDLERNAME, COUNT(ALID) AS COUNT FROM MTX_ALARM_LOG GROUP BY HANDLERNAME, WEEK"

sql_query = pd.read_sql_query(data_select, conn)
data = pd.DataFrame(sql_query, columns=["HANDLERNAME", "COUNT", "WEEK"])

X1

X_ALID = data["HANDLERNAME"]
Y_ALID = data["COUNT"]

print("X:", X_ALID)
print("Y:", Y_ALID)

fig, ax = plt.subplots()
ax.bar(X_ALID, Y_ALID)
plt.xlabel("Handler")
plt.ylabel("Number of Alarms")

plt.show()

# most_common = {}
# most_duration = {}

# for each in cursor.execute(data_select):
#     handler = each[0]
#     alarm_id = each[1]
#     duration = each[2]

#     if alarm_id in most_common:
#         most_common[alarm_id] = most_common[alarm_id] + 1
#     if alarm_id not in most_common:
#         most_common[alarm_id] = 1
