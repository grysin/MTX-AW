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
data_select = "SELECT ALID, HANDLERNAME, NVL(ELAPSEDTIME,0) AS ELAPSEDTIME FROM MTX_JAM_STAT_DATA ORDER BY ELAPSEDTIME DESC"

sql_query = pd.read_sql_query(data_select, conn)
df = pd.DataFrame(sql_query, columns=["HANDLERNAME", "ALID"])


Handlers = df["HANDLERNAME"].sort_values(ascending=True).unique()
Unique_ALID = df["ALID"].sort_values(ascending=True).unique()

# fig, ax = plt.figure()

duration_data = pd.DataFrame(columns=Handlers)
for alid in Unique_ALID:
    Y = list()
    for handler in Handlers:
        statement = (
            "SELECT SUM(NVL(ELAPSEDTIME,0)) AS ELAPSEDTIME FROM MTX_JAM_STAT_DATA WHERE HANDLERNAME = '"
            + str(handler)
            + "' AND ALID = '"
            + str(alid)
            + "'"
        )
        # print(statement)
        cursor.execute(statement)
        result = cursor.fetchone()
        duration_total = result[0]
        # print("initial: ", duration_total)
        try:
            int(duration_total)
        except TypeError:
            duration_total = 0
        # print("after: ", duration_total)
        Y.append(duration_total)
    # print(Y)
    duration_data.loc[alid] = Y
#     plt.bar(Handlers, Y, label=alid)
print(duration_data)


# plt.title("Duration of Alarm Codes")
# plt.legend(bbox_to_anchor=(1.04, 1), loc="upper left")
# plt.xlabel("Handler")
# plt.ylable("Time (sec)")
# plt.show()
