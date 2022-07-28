import cx_Oracle
import os
import csv

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

# choose csv file to add to database
file = "New_Matrix_alarm_text_lookup.csv"

with open(file) as csv_file:
    # read the file
    csv_data = csv.reader(csv_file)
    # each row is a list
    csv_rows = list(csv_data)
    # first row is the header
    header = csv_rows[0]
    # the rest is actual data
    data = csv_rows[1:]
    for index, row in enumerate(data):
        alid = row[0]
        alarmtext = row[1]
        subgroupid = row[2]
        groupid = row[3]

        sql_insert = "INSERT INTO MTX_JAM_STAT_ALARMINFO(ALID, ALARMTEXT, SUBGROUPID, GROUPID) VALUES('"
        sql_insert = sql_insert + alid + "',"
        sql_insert = sql_insert + " q'[" + alarmtext + "]','"
        sql_insert = sql_insert + subgroupid + "','"
        sql_insert = sql_insert + groupid + "')"
        print(index)
        print(sql_insert)
        try:
            cursor.execute(sql_insert)
        except cx_Oracle.IntegrityError:
            pass

    conn.commit()
    print("completed")
