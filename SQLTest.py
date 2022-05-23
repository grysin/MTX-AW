#!/usr/bin/env python3

import cx_Oracle
import os

cx_Oracle.init_oracle_client(lib_dir=r"C:\Program Files (x86)\Oracle\instantclient_21_3")

#SQL="SELECT * FROM TSENSE_CALIBRATION_INDEX"
SQL="SELECT SYSDATE FROM DUAL"
SQL="SELECT 2+4, 3+7 FROM DUAL"
#SQL="INSERT INTO TSENSE_CALIBRATION_INDEX (EVENT_ID) VALUES ('1')"

#os.putenv('ORACLE_HOME','/oracle/product/10.2.0/db_1')
#os.putenv('ORACLE_HOME','C:\Program Files\Oracle\instantclient_12_1')
#os.putenv('LD_LIBRARY_PATH','/oracle/product/10.2.0/db_1/lib')

#connection = cx_Oracle.connect('gntcaadm/gntcaadm01@ohntweb_12c.am.freescale.net:1521/ohntweb')
#connection = cx_Oracle.connect('gntcaadm/gntcaadm01@OHNTWEBDB_VCS.am.freescale.net:1522/ohntweb')
#connection = cx_Oracle.connect('gntcaadm/gntcaadm01@OHNTWEBDB_VCS.am.freescale.net:1522/OHNTWEB')
#connection = cx_Oracle.connect('gntcaadm/gntcaadm01@OHNTWEBDB_VCS.am.freescale.net:1522/?service_name=OHNTWEB')
#connection = cx_Oracle.connect('oracle://gntcaadm:gntcaadm01@OHNTWEBDB_VCS.am.freescale.net:1522/?service_name=OHNTWEB')
#connection = cx_Oracle.connect('oracle://gntcaadm:gntcaadm01@OHNTWEBDB_VCS.am.freescale.net:1522/OHNTWEB')
#connection = cx_Oracle.connect('gntcaadm/gntcaadm01@OHNTWEBDB_VCS.am.freescale.net:1522/?sid=OHNTWEB')
#connection = cx_Oracle.connect('gntcaadm/gntcaadm01@OHNTWEBDB_VCS.am.freescale.net:1522:OHNTWEB')

## this works for a service name connection
connection = cx_Oracle.connect('gntcaadm/gntcaadm01@OHNTWEBDB_VCS.am.freescale.net:1522/OHNTWEB.AM.FREESCALE.NET')

## alternative connection formats

#dsn_tns = cx_Oracle.makedsn('OHNTWEBDB_VCS.am.freescale.net','1522',service_name='OHNTWEB')
#dsn_tns = cx_Oracle.makedsn('OHNTWEBDB_VCS.am.freescale.net','1522',sid='OHNTWEB')

## this one works for a service name connection
#dsn_tns = cx_Oracle.makedsn('OHNTWEBDB_VCS.am.freescale.net','1522',service_name='OHNTWEB.AM.FREESCALE.NET')

## this one works for and SID based connection
#dsn_tns = cx_Oracle.makedsn('OHNTWEBDB_VCS.am.freescale.net','1522',sid='OHNTWEB')
#connection = cx_Oracle.connect(user=r'gntcaadm',password='gntcaadm01',dsn=dsn_tns)
cursor = connection.cursor()
SQL = "select * from TSENSE_USERS"
#SQL = "select * from V$ACTIVE_SERVICES"
#SQL = "select * from global_name"
cursor.execute(SQL)
value =cursor.fetchone()[0]
print("value=",value)
print("cursor=",cursor)
for row in cursor:
	print("row=",row)
cursor.close()
connection.close()
	

#file = "new_blank_new"
#
#if (".xml" not in file and ".XML" not in file) or "_new" not in file:
	#print ("don't copy")