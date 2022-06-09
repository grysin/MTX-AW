import cx_Oracle
import os
import csv
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

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

statement = "SELECT MTX_ALARM_LOG.HANDLERNAME, JAM_STAT_GROUPS.GROUPID, COUNT(MTX_ALARM_LOG.ALID) AS COUNT FROM MTX_ALARM_LOG LEFT JOIN JAM_STAT_GROUPS ON JAM_STAT_GROUPS.ALID = MTX_ALARM_LOG.ALID GROUP BY JAM_STAT_GROUPS.GROUPID, MTX_ALARM_LOG.HANDLERNAME ORDER BY COUNT DESC"

sql_query = pd.read_sql_query(statement, conn)
df = pd.DataFrame(sql_query, columns=["HANDLERNAME", "GROUPID", "COUNT"])

Handlers = df["HANDLERNAME"].sort_values(ascending=True).unique()
Unique_ALID = df["GROUPID"].sort_values(ascending=True).unique()

duration_data = pd.DataFrame(columns=Handlers)
plt.figure()

for alid in Unique_ALID:
    print(alid)
    if not alid:
        print("triggered")
        alid = "Other"
    Y = list()
    for handler in Handlers:
        if alid == "Other":
            statement = (
                "SELECT NVL(COUNT(MTX_ALARM_LOG.ALID),0) AS COUNT FROM MTX_ALARM_LOG, JAM_STAT_GROUPS WHERE HANDLERNAME = '"
                + handler
                + "' AND NOT EXISTS (SELECT null FROM JAM_STAT_GROUPS WHERE MTX_ALARM_LOG.ALID = JAM_STAT_GROUPS.ALID)"
            )
        else:
            print("Else triggered")
            statement = (
                "SELECT NVL(COUNT(MTX_ALARM_LOG.ALID),0) AS COUNT FROM MTX_ALARM_LOG, JAM_STAT_GROUPS WHERE MTX_ALARM_LOG.ALID = JAM_STAT_GROUPS.ALID AND HANDLERNAME ='"
                + str(handler)
            )
            statement = (
                statement + "' AND JAM_STAT_GROUPS.GROUPID = '" + str(alid) + "'"
            )

        # print(statement)
        cursor.execute(statement)
        result = cursor.fetchall()
        count = result[0][0]
        if alid == "Other":
            count = count / 100
        Y.append(count)
    print("Y", Y)
    duration_data.loc[alid] = Y
    plt.bar(Handlers, Y, label=alid)

print(duration_data)

plt.title("Count of Alarm Groups")
plt.xlabel("Handler")
plt.ylabel("Count")
plt.legend()
plt.show()
