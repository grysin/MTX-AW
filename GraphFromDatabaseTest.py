from pickle import TRUE
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
data_select = "SELECT HANDLERNAME, ALID, ALARMTEXT AS DESCRIPTION, ELAPSEDTIME AS DURATION FROM MTX_ALARM_LOG"

sql_query = pd.read_sql_query(data_select, conn)
df = pd.DataFrame(sql_query, columns=["HANDLERNAME", "ALID", "DURATION"])
df["COUNT"] = 1
# X = df["HANDLERNAME"].sort_values(ascending=True).unique()

# Unique_ALID = df["ALID"].sort_values(ascending=True).unique()

# for each_code in Unique_ALID:
#     Y=df[]
# # Y = df["ALID"].loc[df["HANDLERNAME"] == each_handler]
# # Y.groupby(["ALID"])
occurence_df = df.groupby(["ALID", "HANDLERNAME"]).count()["COUNT"]
duration_df = df.groupby(["HANDLERNAME", "ALID"]).sum()["DURATION"]

occurence_df = occurence_df.to_numpy()
print(occurence_df)

# print("DURATION DF: \n", duration_df)  # test
# print("OCCURENCE DF: \n", occurence_df)  # test

# occurence_df.plot.bar(x="HANDLERNAME", y="ALID", stacked=True)
# plt.show()


# BRUTE FORCE
# data = cursor.execute(data_select)

# occurence_count = dict()
# duration_count = dict()

# # for row in data:
#     handler = row[0]
#     alarm = str(row[1])
#     try:
#         duration = int(row[3])
#     except TypeError:
#         pass

#     handler_alarm = handler + "_" + alarm
#     # print(handler_alarm) #test
#     if handler_alarm not in occurence_count:
#         occurence_count[handler_alarm] = 1
#     if handler_alarm in occurence_count:
#         occurence_count[handler_alarm] = occurence_count[handler_alarm] + 1
#     if handler_alarm not in duration_count:
#         duration_count[handler_alarm] = duration
#     if handler_alarm in duration_count:
#         duration_count[handler_alarm] = duration_count[handler_alarm] + duration
