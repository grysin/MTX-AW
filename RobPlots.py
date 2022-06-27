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

handler_list = [
    "MTXA05",
    "MTXA06",
    "MTXA07",
    "MTXA08",
    "MTXA09",
    "MTXA11",
    "MTXA12",
    "MTXA13",
]

for handler in handler_list:
    statement = (
        "SELECT MTX_JAM_STAT_DATA.HANDLERNAME, MTX_JAM_STAT_GROUPINGS.GROUPID, COUNT(MTX_JAM_STAT_DATA.ALID) AS COUNT FROM MTX_JAM_STAT_DATA LEFT JOIN MTX_JAM_STAT_GROUPINGS ON MTX_JAM_STAT_GROUPINGS.ALID = MTX_JAM_STAT_DATA.ALID WHERE HANDLERNAME = '"
        + handler
        + "' AND WEEK BETWEEN 20 AND 26 GROUP BY MTX_JAM_STAT_GROUPINGS.GROUPID, MTX_JAM_STAT_DATA.HANDLERNAME ORDER BY COUNT DESC"
    )
    sql_query = pd.read_sql_query(statement, conn)
    df = pd.DataFrame(sql_query, columns=["HANDLERNAME", "GROUPID", "COUNT"])
    print(df)
    plt.figure()
    X = df["GROUPID"]
    Y = df["COUNT"]
    plt.bar(X, Y, color="black")
    plt.title(handler)
    plt.xlabel("Jam Stat Group")
    plt.ylabel("Count")
    plt.show()
