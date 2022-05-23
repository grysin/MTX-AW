#!/usr/bin/env python3

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
file = "MTX07_lot_log_error_results.csv"
# open the file
with open(file) as csv_file:
    # read the file
    csv_data = csv.reader(csv_file)
    # each row is a list
    csv_rows = list(csv_data)
    # first row is the header
    header = csv_rows[0]
    # the rest is actual data
    alarms = csv_rows[1:]
    # test row
    test_row = alarms[1]
    # print("test row: \n", test_row)

    for row in alarms:
        fname = row[0]
        kit = row[1]
        test = row[2]
        system = row[3]
        setpoint = row[4]
        jobtime = row[5]
        job_time_readable = row[6]
        endtime = row[7]
        end_time_readable = row[8]
        handlername = row[9]
        dayofweek = row[10]
        month = row[11]
        week = row[12]
        quarter = row[13]
        year = row[14]
        intid = row[15]
        alid = row[16]
        alarm_text = row[17]
        lotparts = row[18]
        subid = row[19]
        source = row[20]
        csv_type = row[21]
        csv_class = row[22]
        csv_subclass = row[23]
        unknown1 = row[24]
        arg1 = row[25]
        arg2 = row[26]
        rebootcount = row[27]
        reinitcount = row[28]
        retrycount = row[29]
        clearcount = row[30]
        settime = row[31]
        clearedtime = row[32]
        settime_readable = row[33]
        clearedtime_readable = row[34]
        elapsedtime = row[35]
        unknown2 = row[36]
        unknown3 = row[37]
        unknown4 = row[38]
        temperature = row[39]
        e10mode = row[40]
        opmode = row[41]
        stationmode = row[42]
        testermode = row[43]
        airplow = row[44]
        partcount = row[45]
        cyclecount = row[46]
        unknown5 = row[47]
        userid = row[48]
        handlerid = row[49]
        siteid = row[50]

        sql_insert = "'INSERT INTO MTX_ALARM_LOG(FNAME, KIT, TEST, SYSTEM, SETPOINT, JOB_TIME, JOB_TIME_READABLE,"
        sql_insert = (
            sql_insert
            + " END_TIME, END_TIME_READABLE, HANDLERNAME, DAYOFWEEK, MONTH, WEEK, QUARTER, YEAR,"
        )
        sql_insert = (
            sql_insert
            + " INTID, ALID, ALARMTEXT, LOTPARTS, SUBID, SOURCE, TYPE, CLASS, SUBCLASS, UNKNOWN1,"
        )
        sql_insert = (
            sql_insert
            + " ARG1, ARG2, REBOOTCOUNT, REINITCOUNT, RETRYCOUNT, CLEARCOUNT, SET_TIME)"
        )  # CLEARED_TIME,"

        # sql_insert = (
        #     sql_insert
        #     + " SET_READABLE, CLEARED_READABLE, ELAPSEDTIME, UNKNOWN2, UNKNOWN3, UNKNOWN4, TEMPERATURE, E10MODE, OPMODE,"
        # )
        # sql_insert = (
        #     sql_insert
        #     + " STATIONMODE, TESTERMODE, AIRPLOW, PARTCOUNT, CYCYLECOUNT, UNKNOWN5, USERID, HANDLERID, SITEID) "
        # )
        # print(sql_insert)
        sql_insert = (
            sql_insert
            + " VALUES(q'["
            + fname
            + "]','"
            + kit
            + "','"
            + test
            + "','"
            + system
            + "',"
            + setpoint
            + ","
            + jobtime
            + ", q'["
            + job_time_readable
            + "]',"
            + endtime
            + ", q'["
            + end_time_readable
            + "]','"
            + handlername
            + "',"
            + dayofweek
            + ","
            + month
            + ","
            + week
            + ","
            + quarter
            + ","
            + year
            + ","
            + intid
            + ","
            + alid
            + ",'"
            + alarm_text
            + "',"
            + lotparts
            + ", q'["
            + subid
            + "]',"
            + source
            + ",'"
            + csv_type
            + "','"
            + csv_class
            + "','"
            + csv_subclass
            + "','"
            + unknown1
            + "','"
            + arg1
            + "','"
            + arg2
            + "',"
            + rebootcount
            + ","
            + reinitcount
            + ","
            + retrycount
            + ","
            + clearcount
            + ","
            + settime
            + ");'"
        )
        # + ","
        # + clearedtime
        # + ","
        # + settime_readable
        # + ","
        # + clearedtime_readable
        # + ","
        # + elapsedtime
        # + ","
        # + unknown2
        # + ","
        # + unknown3
        # + ","
        # + unknown4
        # + ","
        # + temperature
        # + ","
        # + e10mode
        # + ","
        # + opmode
        # + ","
        # + stationmode
        # + ","
        # + testermode
        # + ","
        # + airplow
        # + ","
        # + partcount
        # + ","
        # + cyclecount
        # + ","
        # + unknown5
        # + ","
        # + userid
        # + ","
        # + handlerid
        # + ","
        # + siteid
        print("\n")
        print(sql_insert)
        print("\n")
        cursor.execute(sql_insert)
    conn.commit()

# print("Header: \n", header) #test
# print("Contents of CSV file: \n", alarms) #test

# print out every row in the database
# for row in cursor.execute("SELECT * FROM MTX_ALARM_LOG"):
# print(row)

# Choose a CSV file
# loop through contents of CSV file and place each row into the
