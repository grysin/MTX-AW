#!/usr/bin/env python3

"""
Python language test program
"""
import sys
from sys import version_info
py3 = version_info[0] > 2

import re
import os
import time
import handler_kit_Tsense_calibrate_config as config
import shutil

from pprint import pprint
if py3:
    from tkinter import *
    from tkinter.filedialog import *
else:
    from Tkinter import *
    from tkFileDialog import *
from shutil import copyfile
from datetime import date
from datetime import datetime
from time import sleep

program_name = "matrix_lot_log_alarm_extractor_shared_folder"
program_version = "20210412b"
program_title = "matrix alarm extractor"
root = Tk()
root.title(program_title + " - " + program_version)
defbg = root.cget('bg')

try:
    handler_list = config.handler_list
except AttributeError:
    handler_list = ["MTX04","MTX06","MTX07","MTXA01","MTXA02","MTXA03","MTXA04", "MTXA05", "MTXA06", "MTXA07", "MTXA08", "MTXA09"]
handler_list.insert(0,"all")
try:
    Drive_letter_read = config.Drive_letter_read
except AttributeError:
    Drive_letter_read = "t:"
try:
    Drive_letter_write = config.Drive_letter_write
except AttributeError:
    Drive_letter_write = "s:"
try:
    check_revision_on_startup = config.check_revision_on_startup
except AttributeError:
    check_revision_on_startup = 1
#check_revision_on_startup = 0

try:
    release_archives = config.release_archives
except AttributeError:
    #release_archives = r'"\\npi1412-09\C$\Program Files (x86)\Anaconda2\matt\kit_file_editing\Release_Archives"'
    release_archives = r'"\\npi1412-09\kit_file_editing\Release_Archives"'

## the method Rob Webb was using as of 20200511 was "Warns_Report"; but, it doesn't seem to work anymore
## the proper method still needs to be resolved before this software version can be rolled out.
method = "Lot_History"
#method = "Warns_Report"

reftime = time.time()
year_secs = 31536000
month_secs = 2592000
week_secs = 604800
print(("reftime =", reftime))
inputdir = "temp"
inputkitfilename = "base_8offset_exp_ml.xml"
updatekitfilename = "base_8offset_exp_ml.xml"
defoutfilename = "results.csv"
defoutputdir = "temp"
outputdir = "temp"
#history_weeks = 12
history_weeks = 4
max_files = 0
max_warnings = 10000
Alarm_text = {}
all_handlers_flag = 0
outf = 0
Drive_letter_read = "t:"
wu = "fsl\\ultraflexdev"
wup = "Development1"

if sys.argv[1:]:
    inputresultsfilename = sys.argv[1]

fields = []
field_names = []
alarm_data = {}
config_data = {}
outcol = []
test_results = {}
tst_temp = -999
calc_table = {}
dev_setting = {}

## begin automatic revision update
#
#

def update_revision():
    global update_win

    try:
        update_win.destroy()
    except NameError:
        print("update_window not open")
    disconnect_string = r'net use ' + Drive_letter_read + r' /del /y'
    os.system(str(disconnect_string))
    cn_status.config(text="not connected", bg=defbg)

    if os.system("ping -n 1 " + 'Npi1412-09') == 0:
        rev_hist_connect_string = r'net use ' + Drive_letter_read + r' ' + release_archives
        os.system(str(rev_hist_connect_string))
        print(("rev_hist_connect_string=",rev_hist_connect_string))
        rev_hist_dir = Drive_letter_read + "/."
    else:
        rev_hist_dir = "Release_Archives"
        return
    if os.path.exists(rev_hist_dir):
        rev_hist_files = sorted(os.listdir(rev_hist_dir))
    else:
        print("unable to find release history")
        return
    for f in rev_hist_files:
        delimiters = " -- ", "."
        regexpPattern = '|'.join(map(re.escape, delimiters))
        [temp_prog_name,temp_prog_ver,py] = re.split(regexpPattern, f)
        print(("temp_prog_name=",temp_prog_name,",temp_prog_rev=",temp_prog_ver))
        if temp_prog_name == program_name:
            latest_prog_ver = temp_prog_ver
            latest_program = f
    print(("lastest_prog_ver=",latest_prog_ver,",program_version=",program_version))
    if latest_prog_ver > program_version:
        shutil.copy(program_name + ".py","Archives/" + program_name + ".bak.py")
        print((program_name + ".py"+ "," + "Archives/" + program_name + ".bak.py"))
        shutil.copy(Drive_letter_read + latest_program,"Archives")
        print((Drive_letter_read + latest_program + "," + "Archives"))
        shutil.copy(Drive_letter_read + latest_program,program_name + ".py")
        print((Drive_letter_read + latest_program + "," + program_name + ".py"))
        #check_revision_update()
        subprocess.Popen('..\..\python matrix_kit_files_summary.py', shell=True)  # ignoring shell=True
        exit_program()
    else:
        notice_text = "program version is up to date"
        print(notice_text)
    os.system(disconnect_string)
    return

def check_revision_update(notify_if_uptodate=1):
    disconnect_string = r'net use ' + Drive_letter_read + r' /del /y'
    os.system(str(disconnect_string))
    cn_status.config(text="not connected", bg=defbg)
    if os.system("ping -n 1 " + 'Npi1412-09') == 0:
        rev_hist_connect_string = r'net use ' + Drive_letter_read + r' ' + release_archives
        os.system(str(rev_hist_connect_string))
        print(("rev_hist_connect_string=",rev_hist_connect_string))
        rev_hist_dir = Drive_letter_read + "/."
    else:
        rev_hist_dir = "Release_Archives"
        return
    if os.path.exists(rev_hist_dir):
        rev_hist_files = sorted(os.listdir(rev_hist_dir))
    else:
        print("unable to find release history")
        return
    for f in rev_hist_files:
        delimiters = " -- ", "."
        regexpPattern = '|'.join(map(re.escape, delimiters))
        [temp_prog_name,temp_prog_ver,py] = re.split(regexpPattern, f)
        print(("temp_prog_name=",temp_prog_name,",temp_prog_rev=",temp_prog_ver))
        if temp_prog_name == program_name:
            latest_prog_ver = temp_prog_ver
    print(("lastest_prog_ver=",latest_prog_ver,",program_version=",program_version))
    if latest_prog_ver > program_version:
        notice_text = "new program version (" + latest_prog_ver + ") is available"
        Update_window(notice_text,"red")
    else:
        notice_text = "program version is up to date"
        if notify_if_uptodate == 1:
            Update_window(notice_text,"green")
    print(notice_text)
    os.system(disconnect_string)
    #check_config_revision_update(notify_if_uptodate)
    return

def Update_window(message,color="red"):
    global update_win

    update_win = Toplevel()
    update_win.focus_force()
    #update_win.grab_set()

    update_win.l1 = Label(update_win, text=message, bg=color)
    update_win.selections = Frame(update_win)
    update_win.b1 = Button(update_win.selections, text="Cancel", fg="red", command=update_win.destroy)
    if "config" in message:
        update_win.b2 = Button(update_win.selections, text="Update", fg="red", command=update_config_revision)
    else:
        update_win.b2 = Button(update_win.selections, text="Update", fg="red", command=update_revision)
    update_win.l1.pack(side=TOP,fill=X,expand=1)
    update_win.selections.pack(side=BOTTOM,fill=X,expand=1)
    update_win.b1.pack(side=LEFT)
    update_win.b2.pack(side=RIGHT)
    return
#
#
## end automatic revision update


def parse_file_Warns_Report(fname,outf):
    print("parse_file_Warns_Report(",fname,",",outf,"):")
    f = open(fname, 'r')
    handlername = handler.get()
    header = 0
    IntID_list = []
    n = 0
    num_warnings = 0
    for line in f:
        print("line=",line)
        n = n + 1
        #max_warnings = 10
        if num_warnings > max_warnings:
            break
        if "IntID" in line:
            header = 1
            #outf.write(line)
            #print("*** ",line)
            continue
        if header == 1:
            IntID = line.split(",")[1]
            set_time = line.split(",")[13]
            warningtime = datetime.strptime(set_time, '%H:%M:%S %d-%b-%Y')
            #print("IntID=",IntID)
            #print("IntID_list=",IntID_list)
            epoch = datetime.utcfromtimestamp(0)
            warningtime = (warningtime - epoch).total_seconds()
            if reftime - warningtime > int(history_weeks) * week_secs:
                #print ("reftime=",reftime," warningtime=",warningtime,"delta=",reftime - warningtime,"\n")
                #print ("history_weeks=",history_weeks," week_secs=",week_secs,"product=",int(history_weeks)*week_secs,"\n")
                #print("exceeds file age\n")
                continue
            if IntID not in IntID_list:
                #print(".... included \n")
                #outf.write(str(reftime) + "," + str(warningtime) + "," + line)
                outf.write(line)
                #print("*** ",line)
                IntID_list.append(IntID)
                num_warnings = num_warnings + 1
    f.close()
    return

def parse_file_Lot_History(fname,outf):
    print("parse_file_Lot_History(",fname,",",outf,"):")
    f = open(fname, 'r')
    handlername = handler.get()

    for line in f:
        if "Global:Kit " in line:
            kit = line.split()[1]
        if "Global:Test " in line:
            test = line.split()[1]
        if "Global:System " in line:
            system = line.split()[1]
        if "Global:Setpoint " in line:
            setpoint = line.split()[1]
        if "Global:Job_Time " in line:
            job_time = line.split()[1]
        if "Global:Job_Time_Readable " in line:
            job_time_readable = line.split()[1] + " " + line.split()[2]
            job_time_readable = job_time_readable.replace("{","\"")
            job_time_readable = job_time_readable.replace("}","\"")
        if "Global:End_Time " in line:
            end_time = line.split()[1]
        if "Global:End_Time_Readable " in line:
            end_time_readable = line.split()[1] + " " + line.split()[2]
            end_time_readable = end_time_readable.replace("{","\"")
            end_time_readable = end_time_readable.replace("}","\"")
        #if "Warn:" in line:
        if "AlarmData:" in line:
            alarmstring = line.strip()
            outstring = fname + "," + kit + "," + test + "," + system + "," + setpoint
            outstring = outstring + "," + job_time + "," + job_time_readable
            outstring = outstring + "," + end_time + "," + end_time_readable
            outstring = outstring + "," + alarmstring
            #outf.write(outstring + "\n")

            fields = parse_alarm(line)
            IntID = fields[0]
            AlarmText = fields[1]
            ALID = AlarmText[5:]
            if AlarmText in list(Alarm_text.keys()):
                AlarmText = AlarmText + "-" + Alarm_text[AlarmText]
            else:
                Alarm_text[AlarmText] = "Text not found"
                AlarmText = AlarmText + "-" + Alarm_text[AlarmText]
                print((AlarmText," -- text not found"))
            if "," in AlarmText:
                AlarmText = "\"" + AlarmText + "\""
            LotParts = fields[2]
            SubID = fields[3]
            Source = fields[4]
            Type = fields[5]
            Class = fields[6]
            Subclass = fields[7]
            unknown1 = fields[8]
            Arg1 = fields[9]
            Arg2 = fields[10]
            RebootCount = fields[11]
            ReinitCount = fields[12]
            RetryCount = fields[13]
            ClearCount = fields[14]
            set_time = fields[15]

            ## handler time is in seconds since 1/1/1970
            ## python date is days since 1/1/1
            ## there are 86400 seconds in a day
            ## there are 719163 days between 1/1/1 and 1/1/1970
            d = int(int(set_time) / 86400 + 719163)
            d = date.fromordinal(d)
            week = d.isocalendar()[1]
            quarter = week / 13 + 1
            dt = d.timetuple()
            DayOfWeek = dt.tm_wday
            month = dt.tm_mon
            year = dt.tm_year

            cleared_time = fields[16]
            set_readable = fields[17]
            cleared_readable = fields[18]
            ElapsedTime = fields[19]
            unknown2 = fields[20]
            unknown3 = fields[21]
            unknown4 = fields[22]
            Temperature = fields[23]
            E10Mode = fields[24]
            OpMode = fields[25]
            StationMode = fields[26]
            TesterMode = fields[27]
            AirPLow = fields[28]
            PartCount = fields[29]
            CycleCount = fields[30]
            unknown5 = fields[31]
            UserID = fields[32]
            HandlerID = fields[33]
            SiteID = fields[34]

            if 1 == 1:
                outstring_b = fname + "," + kit + "," + test + "," + system + "," + setpoint
                outstring_b = outstring_b + "," + job_time + "," + job_time_readable
                outstring_b = outstring_b + "," + end_time + "," + end_time_readable
                outstring_b = outstring_b + "," + handlername
                outstring_b = outstring_b + "," + str(DayOfWeek)
                outstring_b = outstring_b + "," + str(month)
                outstring_b = outstring_b + "," + str(week)
                outstring_b = outstring_b + "," + str(quarter)
                outstring_b = outstring_b + "," + str(year)
                outstring_b = outstring_b + "," + IntID
                outstring_b = outstring_b + "," + ALID
                outstring_b = outstring_b + "," + AlarmText
                outstring_b = outstring_b + "," + LotParts
                outstring_b = outstring_b + "," + SubID
                outstring_b = outstring_b + "," + Source
                outstring_b = outstring_b + "," + Type
                outstring_b = outstring_b + "," + Class
                outstring_b = outstring_b + "," + Subclass
                outstring_b = outstring_b + "," + unknown1
                outstring_b = outstring_b + "," + Arg1
                outstring_b = outstring_b + "," + Arg2
                outstring_b = outstring_b + "," + RebootCount
                outstring_b = outstring_b + "," + ReinitCount
                outstring_b = outstring_b + "," + RetryCount
                outstring_b = outstring_b + "," + ClearCount
                outstring_b = outstring_b + "," + set_time
                outstring_b = outstring_b + "," + cleared_time
                outstring_b = outstring_b + "," + set_readable
                outstring_b = outstring_b + "," + cleared_readable
                outstring_b = outstring_b + "," + ElapsedTime
                outstring_b = outstring_b + "," + unknown2
                outstring_b = outstring_b + "," + unknown3
                outstring_b = outstring_b + "," + unknown4
                outstring_b = outstring_b + "," + Temperature
                outstring_b = outstring_b + "," + E10Mode
                outstring_b = outstring_b + "," + OpMode
                outstring_b = outstring_b + "," + StationMode
                outstring_b = outstring_b + "," + TesterMode
                outstring_b = outstring_b + "," + AirPLow
                outstring_b = outstring_b + "," + PartCount
                outstring_b = outstring_b + "," + CycleCount
                outstring_b = outstring_b + "," + unknown5
                outstring_b = outstring_b + "," + UserID
                outstring_b = outstring_b + "," + HandlerID
                outstring_b = outstring_b + "," + SiteID

        #       for fld in fields:
        #               outstring_b = outstring_b + "," + fld
#
#                       outstring_b = outstring_b + "," + AlarmText
            outf.write(outstring_b + "\n")

            #print(fname,",",kit,",",test,",",system,",",setpoint,"\n")
    f.close()
    return

def outfile_header_row_Warns_Report(outf):
    header = "Handler Name" + "," + "IntID" + "," + "WARNID" + "," + "Warn Text" + "," + "Source"
    header = header + ",Type"
    header = header + ",Class"
    header = header + ",Subclass"
    header = header + ",Annotation"
    header = header + ",Reboot Count"
    header = header + ",Reinit Count"
    header = header + ",Retry Count"
    header = header + ",Clear Count"
    header = header + ",Set"
    header = header + ",Cleared"
    header = header + ",Elapsed"
    header = header + ",Response time"
    header = header + ",Temperature"
    header = header + ",E10 Mode"
    header = header + ",OpMode"
    header = header + ",Station Mode"
    header = header + ",Tester Mode"
    header = header + ",Air P Low"
    header = header + ",Part Count"
    header = header + ",Cycle Count"
    header = header + ",User ID"
    header = header + ",Handler ID"
    header = header + ",Site ID"
    outf.write(header + "\n")
    return

def outfile_header_row_Lot_History(outf):
    header = "fname" + "," + "kit" + "," + "test" + "," + "system" + "," + "setpoint"
    header = header + "," + "job_time" + "," + "job_time_readable"
    header = header + "," + "end_time" + "," + "end_time_readable"
    header = header + "," + "handlername" + "," + "DayOfWeek" + "," + "month" + "," + "week" + ","+"quarter"+","+"year"
    header = header + ",IntID"
    header = header + ",ALID"
    header = header + ",AlarmText"
    header = header + ",LotParts"
    header = header + ",SubID"
    header = header + ",Source"
    header = header + ",Type"
    header = header + ",Class"
    header = header + ",Subclass"
    header = header + ",unknown1"
    header = header + ",Arg1"
    header = header + ",Arg2"
    header = header + ",RebootCount"
    header = header + ",ReinitCount"
    header = header + ",RetryCount"
    header = header + ",ClearCount"
    header = header + ",set_time"
    header = header + ",cleared_time"
    header = header + ",set_readable"
    header = header + ",cleared_readable"
    header = header + ",ElapsedTime"
    header = header + ",unknown2"
    header = header + ",unknown3"
    header = header + ",unknown4"
    header = header + ",Temperature"
    header = header + ",E10Mode"
    header = header + ",OpMode"
    header = header + ",StationMode"
    header = header + ",TesterMode"
    header = header + ",AirPLow"
    header = header + ",PartCount"
    header = header + ",CycleCount"
    header = header + ",unknown5"
    header = header + ",UserID"
    header = header + ",HandlerID"
    header = header + ",SiteID"
    outf.write(header + "\n")
    return

def Read_matrix_alarm_text_lookup():
    global Alarm_text

    Alarm_text = {}
    lookup = open("Matrix_alarm_text_lookup.csv", 'r')
    for line in lookup:
        #(Alarm,text) = line.strip().split(",")
        (Alarm,text) = parse_line_csv(line.strip())
        Alarm_text[Alarm] = text
    lookup.close()
    return

def connect_handlers(hostname="checklist",lwu='',lwup=''):
    global inputInitialDir
    global ndn
    global cn_status

    if hostname == "checklist":
        hostname = handler.get()

    if hostname == "all":
        e4.delete(0, END)
        for hostname in (handler_list):
            ndn = hostname
            con_stat = connect_handler(hostname,lwu,lwup)
    else:
        ndn = hostname
        con_stat = connect_handler(hostname,lwu,lwup)
    #print "read check complete"
    #e4.insert(0, "read check complete")
    return 0

def connect_handler(hostname="checklist",lwu='',lwup=''):
    global inputInitialDir
    global ndn
    global cn_status
    global connect_path

    if hostname == "all":
        return 1
    if con_dir == "":
        connect_path = "\\Recipes"
    else:
        connect_path = "\\" + con_dir
    if hostname == "checklist":
        hostname = handler.get()
        if hostname == "all":
            print("connect to all is done at run time")
            return
    if "MTX" in hostname:
        hostname = hostname + "-01"
    print(("host name= ",hostname))

    disconnect_string = r'net use ' + Drive_letter_read + r' /del /y'
    os.system(disconnect_string)
    cn_status.config(text="not connected", bg=defbg)
    sleep(8)

    ndn = "ERROR"
    if os.system("ping -n 1 " + hostname) == 0:
        print((hostname, "IS reached"))
        if lwu == '':
            handler_connect_string = r'net use ' + Drive_letter_read + r' \\' + hostname + connect_path
        else:
            handler_connect_string = r'net use ' + Drive_letter_read + r' \\' + hostname + connect_path + r' /user:' + lwu + r' ' + lwup + r' /persistent:no'
        print(handler_connect_string)
        os.system(handler_connect_string)
        ndn = hostname.split("-")[0]
        #if hostname == "MTX01-01":
            #os.system(r'net use t: \\mtx01-01\Recipes')
            #ndn = "MTX01"
        #elif hostname == "MTX02-01":
            #os.system(r'net use t: \\mtx02-01\Recipes')
            #ndn = "MTX02"
        #else:
            #print('MATRIX NAME ERROR')
            #cn_status.config(text="not connected", bg=defbg)
            #return

        #inputInitialDir = Drive_letter_read + "/MatrixHandler/Kit"
        inputInitialDir = Drive_letter_read + "/."

        if os.path.exists(inputInitialDir):
            # update HERE
            cn_status.config(text="connected to %s" % ndn, bg='blue')
            print(("connected to " + ndn))
            e4.insert(0, lwu + " connected to " + hostname + connect_path)
            e4.update()
        else:
            print((hostname, "is NOT connected"))
            cn_status.config(text="not connected", bg=defbg)
            e4.insert(0, lwu + " is NOT connected to " + hostname + connect_path)
            #Error_window("Error: handler is not connected")
            return 1

    else:
        print((hostname, "is NOT reached"))
        cn_status.config(text="not connected", bg=defbg)
        e4.insert(0, hostname + " is NOT REACHED")
        return 1
    return 0


def check_connections():
    global wu
    global wup
    global con_dir

    for con_dir in ["Lot_History", "log", "Recipes", "C$", "D$"]:
        connect_handlers()
        connect_handlers('checklist',wu,wup)
    print("check connections complete")
    e4.insert(0, "check connections complete")
    return

def ping_connections():
    global uf
    global inputdir
    global defoutfilename
    global all_handlers_flag
    global outf

    e4.delete(0, END)
    for handler in handler_list:
        hostname = handler + "-01"
        print(("host name= ",hostname))

        response = os.system("ping -n 1 " + hostname)
        if response == 0:
            print((hostname, 'is up'))
            e4.insert(0, hostname + " is reached")
            e4.update()
        else:
            print((hostname, 'is down'))
            e4.insert(0, hostname + " is NOT reached")
            e4.update()

    print("ping check complete")
    e4.insert(0, "ping check complete")
    return


def copy_files():
    global uf
    global inputdir
    global defoutfilename
    global all_handlers_flag
    global outf

    Read_matrix_alarm_text_lookup()
    history_weeks = e2.get()
    print("history_weeks=",history_weeks)
    #max_files = e4.get()
    max_files = "0"
    hostname = handler.get() + "-01"
    filetype = getfiletype.get()
    print(("host name= ",hostname))
    print(("get file type= ",filetype))

    disconnect_string = r'net use ' + Drive_letter_read + r' /del /y'

    os.system(disconnect_string)
    #sleep(10)

    ndn = "ERROR"
    if os.system("ping -n 1 " + hostname) == 0:
        e4.insert(0, hostname + " is connected")
        e4.update()
        if method == "Lot_History":
            handler_connect_string = r'net use ' + Drive_letter_read + r' \\' + hostname + r'\D$ /user:' + wu + r' ' + wup + r' /persistent:no'
            #handler_connect_string = r'net use ' + Drive_letter_read + r' \\' + hostname + r'\Lot_history\ /user:' + wu + r' ' + wup + r' /persistent:no'
            os.system(handler_connect_string)
        elif method == "Warns_Report":
            handler_connect_string = r'net use ' + Drive_letter_read + r' \\' + hostname + r'\C$\log\PeriodicDataUploads /user:' + wu + r' ' + wup + r' /persistent:no'
            #handler_connect_string = r'net use ' + Drive_letter_read + r' \\' + hostname + r'\C$\log\PeriodicDataUploads /persistent:no'
            os.system(handler_connect_string)
        print("handler_connect_string=",handler_connect_string)
        ndn = hostname.split("-")[0]

        outputfilename = e3.get()
        [short_outputfilename] = outputfilename.split("/")[-1:]
        temppath = []
        temppath = outputfilename.split("/")
        temppath.pop()
        kinpath = "/".join(temppath)
        outputdir = defoutputdir
        if kinpath != "":
            outputdir = kinpath

        if method == "Lot_History":
            inputdir = 'T:/Lot_History'
        elif method == "Warns_Report":
            inputdir = 'T:'
        else:
            # inputdir for testing
            inputdir = "C:/Anaconda3/matt/kit_file_editing/temp/Lot_History"
        ndn = ndn + "_lot_log_error"


        #outputdir = outputdir + "/" + ndn
        if all_handlers_flag == 0:
            outfilename = outputdir + "/" + ndn + "_" + defoutfilename
        else:
            outfilename = outputdir + "/" + "all_" + defoutfilename
        print("outputdir:",outputdir)
        if not os.path.exists(outputdir):
            os.makedirs(outputdir)
        if all_handlers_flag < 2:
            outf = open(outfilename, 'w')
            if method == "Lot_History":
                outfile_header_row_Lot_History(outf)
            elif method == "Warns_Report":
                outfile_header_row_Warns_Report(outf)
            else:
                outfile_header_row_Lot_History(outf)
                #outfile_header_row_Warns_Report(outf)
        if all_handlers_flag == 1:
            all_handlers_flag = 2

        print("inputdir:",inputdir)
        if not os.path.exists( inputdir ):
            print("path does not exist on handler: ",inputdir)
            os.system(disconnect_string)
            return
        dirs = os.listdir( inputdir )
        #print("*dirs=",dirs)
        dirst = [os.path.join(inputdir, f) for f in dirs]
        dirs = []
        for fn in dirst:
            t = os.stat(fn)
            #print("t=",t)
            xt = t.st_ctime
            #xt = t.st_mtime
            #print("xt=",xt)
            #print("reftime=",reftime)
            #print("history_weeks * week_secs=",int(history_weeks) * week_secs,",reftime - xt=",reftime - xt)
            if reftime - xt > int(history_weeks) * week_secs:
                continue
            #print("xt=",xt,",fn=",fn)
            dirs.append(fn)

        ##dirlist = [(time.ctime(x[1].st_ctime), x[0]) for x in sorted([(fn, os.stat(fn)) for fn in dirs], key = lambda x: x[1].st_ctime, reverse=True)]
        print("**dirs=",dirs)
        dirlist = [(x[1].st_ctime, x[0]) for x in sorted([(fn, os.stat(fn)) for fn in dirs], key = lambda x: x[1].st_ctime, reverse=True)]
        n = 0
        print("Max_files=",max_files," history_weeks=",history_weeks)
        #print("dirlist=",dirlist)
        for (ftime,file) in dirlist:
            #print("--file = ",file,"\n")
            n = n + 1
            if max_files != "" and max_files != "0":
                if n > int(max_files):
                    print("exceeds max files\n")
                    break
            if reftime - ftime > int(history_weeks) * week_secs:
                print("exceeds file age\n")
                break
            print("ftime=",time.ctime(ftime), "file=",file)
            #if "Warns-Report" not in file:
                #continue
            #origfile = inputdir + "/" + file
            #newfile = outputdir + "/" + file
            #print("inputdir=",inputdir,",file=",file)
            #print("copy ",origfile," to ",newfile)
            #copyfile(origfile, newfile)
            #parse_file_new(file,outf)
            if method == "Lot_History":
                parse_file_Lot_History(file,outf)
                #print("parse_Lot_History")
            elif method == "Warns_Report":
                parse_file_Warns_Report(file,outf)
                #print("parse_file_Warns")
            #break

        os.system(disconnect_string)
        print(("reftime =", reftime))
        print("analysis complete\n")
        if all_handlers_flag == 0:
            outf.close()
    else:
        print((hostname, "is NOT connected"))
        e4.insert(0, hostname + " is NOT connected")
        e4.update()

    return

def parse_alarm(line):
    field = []
    fn = 0
    qs = 0
    fval = ""
    for l in range(len(line)):
        if line[l] == "{":
            qs = qs + 1
        elif line[l] == "}":
            qs = qs - 1
        elif line[l] == " " and qs == 1:
            field.append(fval)
            fn = fn + 1
            fval = ""
        elif qs > 0:
            if line[l] == ",":
                fval = fval + "^"
            else:
                fval = fval + line[l]
    field.append(fval)
    return(field)

def parse_line_csv(line):
    field = []
    fn = 0
    qs = -1
    fval = ""
    for l in range(len(line)):
        if line[l] == "\"":
            qs = qs * -1
        elif line[l] == "," and qs < 0:
            field.append(fval)
            fn = fn + 1
            fval = ""
        else:
            fval = fval + line[l]
    field.append(fval)
    return(field)

def one_handler():
    global all_handlers_flag
    global outf

    all_handlers_flag = 0
    copy_files()
    outf.close()
    e4.insert(0, "task complete")
    return

def all_handlers():
    global all_handlers_flag
    global outf

    all_handlers_flag = 1
    check_connections()
    for handler_name in handler_list:
        handler.set(handler_name)
        copy_files()
    outf.close()
    e4.insert(0, "task complete")
    return

def get_updatekitfilename():
    global updatekitfilename
    updatekitfilename = askopenfilename()
    e3.delete(0, END)
    e3.insert(0, updatekitfilename)
    return

def exit_program():
    disconnect_string = r'net use ' + Drive_letter_read + r' /del /y'
    os.system(disconnect_string)
    disconnect_string = r'net use ' + Drive_letter_write + r' /del /y'
    os.system(disconnect_string)
    #os.system(r'net use t: /del /y')
    #os.system(r'net use s: /del /y')
    root.quit()
    return

def build_control_window():
    global e1
    global e2
    global e3
    global e4
    global handler
    global getfiletype
    global ndn
    global cn_status

    root.minsize(width=300, height=475)
    body = Frame(root)
    body.pack(fill=BOTH, expand=1)

    handler = StringVar()
    handler.set("all")
    getfiletype = StringVar()
    getfiletype.set("Lot")
    l1 = LabelFrame(body, text="handler name")
    e1 = OptionMenu(l1,handler,*handler_list)
    l1.pack()
    e1.pack(side=LEFT)

    cn_status = Label(body, text="not connected")
    cn_status.pack(fill=X, expand=1)

    l2 = LabelFrame(body, text="History (Weeks)")
    e2 = Entry(l2)
    #e2_1 = Radiobutton(l2, text="Lot", variable=getfiletype, value="Lot")
    #e2_2 = Radiobutton(l2, text="System", variable=getfiletype, value="System")
    #e2_3 = Radiobutton(l2, text="Test", variable=getfiletype, value="Test")
    l2.pack()
    e2.pack(side=LEFT)
    l4 = LabelFrame(body, text="connection_status")
    e4 = Listbox(l4)
    l4.pack(fill=BOTH, expand=1)
    e4.pack(side=LEFT, fill=BOTH, expand=1)
    #e2_1.pack(side=LEFT)
    #e2_2.pack(side=LEFT)
    #e2_3.pack(side=LEFT)
    l3 = LabelFrame(body, text="output directory")
    e3 = Entry(l3)
    fb3 = Button(l3, text="browse", command=get_updatekitfilename)
    l3.pack()
    e3.pack(side=LEFT)
    fb3.pack(side=LEFT)

    selected_handler = handler.get()
    e2.delete(0, END)
    e2.insert(0, history_weeks)
    e4.delete(0, END)
    e4.insert(0, "none")
    e3.delete(0, END)
    e3.insert(0, outputdir)

    menu = Frame(root)
    menu.pack()
    menu.b1 = Button(menu, text="Quit", fg="red", command=exit_program)
    menu.b2 = Button(menu, text="one handler alarm data", fg="green", command=one_handler)
    menu.b3 = Button(menu, text="all handler alarm data", fg="green", command=all_handlers)
    menu.b4 = Button(menu, text="detailed connections check", fg="green", command=check_connections)
    menu.b5 = Button(menu, text="ping network connections", fg="green", command=ping_connections)
    menu.b1.pack(side=TOP)
    menu.b4.pack(side=TOP)
    menu.b5.pack(side=TOP)
    menu.b2.pack(side=TOP)
    menu.b3.pack(side=TOP)

    menubar = Menu(root)
    helpmenu = Menu(menubar, tearoff=0)
    helpmenu.add_command(label="Check for Update", command=check_revision_update)
    menubar.add_cascade(label="Help", menu=helpmenu)
    root.config(menu=menubar)

    if check_revision_on_startup == 1:
        check_revision_update(0)

    return

build_control_window()
root.mainloop()

#if py3:
    #input("program complete.  Hit 'Enter' to close")
#else:
    #raw_input("program complete.  Hit 'Enter' to close")

## end of program
