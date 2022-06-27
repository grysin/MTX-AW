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

# statement = "SELECT ALID, COUNT(ALID) AS COUNT FROM MTX_JAM_STAT_DATA WHERE HANDLERNAME = 'MTXA09' AND YEAR = '2022' GROUP BY ALID ORDER BY COUNT DESC"
statement = "SELECT MTX_JAM_STAT_DATA.HANDLERNAME, MTX_JAM_STAT_DATA.WEEK, MTX_JAM_STAT_GROUPINGS.GROUPID,  COUNT(MTX_JAM_STAT_DATA.ALID) AS COUNT FROM MTX_JAM_STAT_DATA LEFT JOIN MTX_JAM_STAT_GROUPINGS ON MTX_JAM_STAT_GROUPINGS.ALID = MTX_JAM_STAT_DATA.ALID WHERE HANDLERNAME = 'MTXA09' AND WEEK BETWEEN 1 AND 26 GROUP BY MTX_JAM_STAT_GROUPINGS.GROUPID, MTX_JAM_STAT_DATA.HANDLERNAME, MTX_JAM_STAT_DATA.WEEK ORDER BY MTX_JAM_STAT_DATA.WEEK DESC"

sql_query = pd.read_sql_query(statement, conn)
df = pd.DataFrame(sql_query, columns=["HANDLERNAME", "WEEK", "GROUPID", "COUNT"])
print(df)
