import sys
from sys import version_info
from tkinter.ttk import Notebook

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
    from tkinter import ttk
else:
    from Tkinter import *
    from tkFileDialog import *
from shutil import copyfile
from datetime import date
from datetime import datetime
from time import sleep
import cx_Oracle

cx_Oracle.init_oracle_client(
    lib_dir=r"C:\Program Files (x86)\Oracle\instantclient_21_3"
)

program_name = "matrix_lot_log_alarm_extractor_shared_folder"
program_version = "20220426"
program_title = "MTX Jam Stat Analysis"
root = Tk()
root.title(program_title + " - " + program_version)
defbg = root.cget("bg")

try:
    handler_list = config.handler_list
except AttributeError:
    handler_list = [
        "MTX04",
        "MTX06",
        "MTX07",
        "MTXA01",
        "MTXA02",
        "MTXA03",
        "MTXA04",
        "MTXA05",
        "MTXA06",
        "MTXA07",
        "MTXA08",
        "MTXA09",
        "MTXA10",
    ]
handler_list.insert(0, "all")
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
# check_revision_on_startup = 0

try:
    release_archives = config.release_archives
except AttributeError:
    # release_archives = r'"\\npi1412-09\C$\Program Files (x86)\Anaconda2\matt\kit_file_editing\Release_Archives"'
    release_archives = r'"\\npi1412-09\kit_file_editing\Release_Archives"'

## the method Rob Webb was using as of 20200511 was "Warns_Report"; but, it doesn't seem to work anymore
## the proper method still needs to be resolved before this software version can be rolled out.
method = "Lot_History"
# method = "Warns_Report"

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
# history_weeks = 12
history_weeks = 4
max_files = 0
max_warnings = 10000
Alarm_text = {}
all_handlers_flag = 0
outf = 0  # should this be a zero?
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
def update_revision():
    global update_win
    try:
        update_win.destroy()
    except NameError:
        print("update_window not open")
    disconnect_string = r"net use " + Drive_letter_read + r" /del /y"
    os.system(str(disconnect_string))
    cn_status.config(text="not connected", bg=defbg)

    if os.system("ping -n 1 " + "Npi1412-09") == 0:
        rev_hist_connect_string = (
            r"net use " + Drive_letter_read + r" " + release_archives
        )
        os.system(str(rev_hist_connect_string))
        print(("rev_hist_connect_string=", rev_hist_connect_string))
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
        regexpPattern = "|".join(map(re.escape, delimiters))
        [temp_prog_name, temp_prog_ver, py] = re.split(regexpPattern, f)
        # print(("temp_prog_name=", temp_prog_name, ",temp_prog_rev=", temp_prog_ver))
        if temp_prog_name == program_name:
            latest_prog_ver = temp_prog_ver
            latest_program = f
    # print(("lastest_prog_ver=", latest_prog_ver, ",program_version=", program_version))
    if latest_prog_ver > program_version:
        shutil.copy(program_name + ".py", "Archives/" + program_name + ".bak.py")
        print((program_name + ".py" + "," + "Archives/" + program_name + ".bak.py"))
        shutil.copy(Drive_letter_read + latest_program, "Archives")
        print((Drive_letter_read + latest_program + "," + "Archives"))
        shutil.copy(Drive_letter_read + latest_program, program_name + ".py")
        print((Drive_letter_read + latest_program + "," + program_name + ".py"))
        # check_revision_update()
        subprocess.Popen(
            "..\..\python matrix_kit_files_summary.py", shell=True
        )  # ignoring shell=True
        exit_program()
    else:
        notice_text = "program version is up to date"
        print(notice_text)
    os.system(disconnect_string)
    return


def check_revision_update(notify_if_uptodate=1):
    disconnect_string = r"net use " + Drive_letter_read + r" /del /y"
    os.system(str(disconnect_string))
    cn_status.config(text="not connected", bg=defbg)
    if os.system("ping -n 1 " + "Npi1412-09") == 0:
        rev_hist_connect_string = (
            r"net use " + Drive_letter_read + r" " + release_archives
        )
        os.system(str(rev_hist_connect_string))
        print(("rev_hist_connect_string=", rev_hist_connect_string))
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
        regexpPattern = "|".join(map(re.escape, delimiters))
        [temp_prog_name, temp_prog_ver, py] = re.split(regexpPattern, f)
        print(("temp_prog_name=", temp_prog_name, ",temp_prog_rev=", temp_prog_ver))
        if temp_prog_name == program_name:
            latest_prog_ver = temp_prog_ver
    print(("lastest_prog_ver=", latest_prog_ver, ",program_version=", program_version))
    if latest_prog_ver > program_version:
        notice_text = "new program version (" + latest_prog_ver + ") is available"
        Update_window(notice_text, "red")
    else:
        notice_text = "program version is up to date"
        if notify_if_uptodate == 1:
            Update_window(notice_text, "green")
    print(notice_text)
    os.system(disconnect_string)
    # check_config_revision_update(notify_if_uptodate)
    return


def Update_window(message, color="red"):
    global update_win

    update_win = Toplevel()
    update_win.focus_force()
    # update_win.grab_set()

    update_win.l1 = Label(update_win, text=message, bg=color)
    update_win.selections = Frame(update_win)
    update_win.b1 = Button(
        update_win.selections, text="Cancel", fg="red", command=update_win.destroy
    )
    # update config revision function doesn't exist
    if "config" in message:
        update_win.b2 = Button(
            update_win.selections,
            text="Update",
            fg="red",
            command=update_config_revision,
        )
    else:
        update_win.b2 = Button(
            update_win.selections, text="Update", fg="red", command=update_revision
        )
    update_win.l1.pack(side=TOP, fill=X, expand=1)
    update_win.selections.pack(side=BOTTOM, fill=X, expand=1)
    update_win.b1.pack(side=LEFT)
    update_win.b2.pack(side=RIGHT)
    return


tabs = Notebook(root)
tabs.pack()

data_tab = Frame(tabs)
data_tab.pack(fill="both", expand=1)

plot_tab = Frame(tabs)
plot_tab.pack(fill="both", expand=1)

tabs.add(data_tab, text="Retrieve Jam Stats")
tabs.add(plot_tab, text="Set Plot Paramters")


def conf(event):
    tabs.config(height=root.winfo_height(), width=root.winfo_width())


root.bind("<Configure>", conf)
# geometry = Width*Height
root.geometry("400x300")

# create variable for handler select menu
handler_select = StringVar()
# default value is None
handler_select.set("None")

# create the label frame, box for handler select menu, put it in the data tab
handler_select_frame = LabelFrame(data_tab, text="Retrieve Data From...")
# create the option menu, put it in the handler label frame, default value and list values
handler_option_menu = OptionMenu(handler_select_frame, handler_select, *handler_list)
handler_option_menu.config(width=20)
# put the handler label frame on the screen
handler_select_frame.pack(side=LEFT)
# put the menu on the screen
handler_option_menu.pack()

history_select_frame = LabelFrame(data_tab, text="Select Date Range")
history_select_frame.pack(side=RIGHT)

history_select_entry = Entry(history_select_frame)
history_select_entry.insert(0, "Enter start date")
history_select_entry.pack(side=LEFT)

history_select_entry2 = Entry(history_select_frame)
history_select_entry2.insert(0, "Enter end date")
history_select_entry2.pack(side=RIGHT)

body = Frame(data_tab)
cn_status = Label(body)

root.mainloop()
