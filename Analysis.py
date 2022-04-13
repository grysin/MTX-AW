# Warning / Alarm Parsing
# Import packages needed to parse, analyze, plot data
from ast import Num
import csv
from doctest import master
from turtle import width
from typing import List, OrderedDict
import numpy
import matplotlib.pyplot as plt
import re
from re import split
from collections import Counter
from numpy import source
from matplotlib.widgets import Button

# Import packages needed for user interface
from tkinter import *
import os
from tkinter import filedialog

from platformdirs import user_config_dir

# create the root window
root = Tk()
root.title("MTX Alarm / Warning Analysis")
# # create the input box that asks for the directory where csv files are located
# # create the frame
input_csv_directory_frame = LabelFrame(root, text="Input the CSV directory")
input_csv_directory_frame.grid(row=0, column=0)
input_csv_directory = Label(input_csv_directory_frame, width=90)
input_csv_directory.grid()
# define browse command that will be used with browse button
def browse():
    global input_directory
    input_file = str(filedialog.askopenfile())
    print("input_file = ",input_file)
    input_directory = str(os.path.dirname(input_file))
    print("input_directory = ",input_directory)
    a=1/0
    input_csv_directory = Label(
        input_csv_directory_frame, width=90, text=input_directory
    )
    input_csv_directory.grid(row=0, column=0)


# define the button on the UI that is used to browse for directory containing alarm/warning CSVs
csv_directory_browse = Button(input_csv_directory_frame, text="Browse", command=browse)
csv_directory_browse.grid(row=0, column=1)

check_csv_frame = LabelFrame(root, text="Files to be analzyed")
check_csv_frame.grid(row=2, column=0)
check_csv_list = Listbox(check_csv_frame, width=90)
check_csv_list.grid(row=0, column=0, columnspan=2)

# define function that collects data from the CSVs
def collect_data():
    # initialize list to catch csv files we care about
    global csv_files
    csv_files = []
    for root, dirs, files in os.walk(input_directory):
        for file in files:
            # only interested in csv files that match these two criteria
            if file.endswith(".csv") and file.startswith("MTX"):
                csv_files.append(file)
                check_csv_list.insert(END, file)
    # print("Files collected: ", csv_files)  # test
    return


# MTX-04-Alarm_Stats-2022_03_18_14_17_31.csv
# MTX-04-Warn_Stats-2022_03_18_14_17_41.csv
# MTX-06-Alarm_Stats-2022_03_18_14_20_46.csv
# MTX-06-Warn_Stats-2022_03_18_14_20_58.csv
# MTX-A05-Alarm_Stats-2022_03_18_14_17_08.csv
# MTX-A05-Warn_Stats-2022_03_18_14_17_18.csv
# MTX-A07-Alarm_Stats-2022_03_18_14_17_43.csv
# MTX-A07-Warn_Stats-2022_03_18_14_17_50.csv
# Regex: MTX-[A|0|1].+-(Alarm|Warn)_Stats-\d{4}_\d{2}_\d{2}_\d{2}_\d{2}_\d{2}\.csv

def date_adjust():
    
    return

def analyze_csv():
    for file in csv_files:
        # print(file)  # test
        [file_name, dot_csv] = re.split(".csv", file)
        name_info = re.split("-", file_name)
        alarm_warn_type = name_info[2]
        matrix_name = name_info[0] + "-" + name_info[1]
        datetime_gathered = name_info[3]
        [year, month, day, hour, minute, seconds] = datetime_gathered.split("_")
        datetime_gathered = (
            year + "-" + month + "-" + day + " " + hour + ":" + minute + ":" + seconds
        )
        csv_file = open(file)
        csv_data = csv.reader(csv_file)
        csv_rows = list(csv_data)
        if alarm_warn_type == "Alarm_Stats":
            time_title = csv_rows[0]
            export_time = csv_rows[1]
            blank = csv_rows[2]
            header = csv_rows[3]
            # make rows start at 1
            csv_rows = csv_rows[4:]
            alarms = []
            for row in csv_rows:
                int_id = row[0]
                alarm_id = row[1]
                alarm_text = row[2]
                sub_id = row[3]
                alarm_source = row[4]
                alarm_type = row[5]
                alarm_class = row[6]
                alarm_subclass = row[7]
                annotation = row[8]
                arg1 = row[9]
                arg2 = row[10]
                reboot_count = row[11]
                reinit_count = row[12]
                retry_count = row[13]
                clear_count = row[14]
                time_occured = row[15]
                time_cleared = row[16]
                date_set = row[17]
                date_cleared = row[18]
                time_elapsed = row[19]
                response = row[20]
                temperatue = row[21]
                e10_mode = row[22]
                opmode = row[23]
                station_mode = row[24]
                tester_mode = row[25]
                air_p_low = row[26]
                # part_count = row[27]
                # cycle_count = row[28]
                # user_id = row[29]
                handler_id = row[30]
                site_id = row[31]

                # alarm counting
                alarms.append(alarm_id)
                # check for duplicates

                # alarm time duration

            # print(time_elapsed)
            alarms = Counter(alarms)
            alarms = OrderedDict(alarms.most_common())
            alarm_id_names = list(alarms.keys())
            alarm_id_count = list(alarms.values())
            # inst of alarms from the matrix
            alarm_bar_graph = plt.figure(num=(handler_id + " Alarm Bar Graph"))
            plt.bar(range(len(alarms)), alarm_id_count, tick_label=alarm_id_names)
            plt.xticks(rotation=90)
            plt.show()
            # time duration of alarms from the matrix

            # number of alarms from all matrix

        if alarm_warn_type == "Warn_Stats":
            time_title = csv_rows[0]
            export_time = csv_rows[1]
            blank = csv_rows[2]
            header = csv_rows[3]
            csv_rows = csv_rows[4:]
            warnings = []
            continue_count = 1
            for row in csv_rows:
                try:
                    int_id = int(row[0])
                except ValueError:
                    continue
                if continue_count == int_id:
                    continue_count = continue_count + 1
                else:
                    continue
                warn_id = row[1]
                warn_text = row[2]
                try:
                    source = row[3]
                except IndexError:
                    continue
                warn_type = row[4]
                warn_class = row[5]
                warn_subclass = row[6]
                annotation = row[7]
                reboot_cause = row[8]
                reinit_count = row[9]
                retry_count = row[10]
                clear_count = row[11]
                time_set = row[12]
                time_cleared = row[13]
                time_elapsed = row[14]
                response_time = row[15]
                temperature = row[16]
                e10_mode = row[17]
                opmode = row[18]
                station_mode = row[19]
                tester_mode = row[20]
                air_p_low = [21]
                part_count = row[22]
                cycle_count = row[23]
                user_id = row[24]
                handler_id = row[25]
                site_id = row[26]
                warnings.append(warn_id)
            warnings = Counter(warnings)
            warnings = OrderedDict(warnings.most_common())
            warn_id_names = list(warnings.keys())
            warn_id_count = list(warnings.values())
            warning_bar_graph = plt.figure(num=(handler_id + " Warning Bar Graph"))
            plt.bar(range(len(warnings)), warn_id_count, tick_label=warn_id_names)
            plt.xticks(rotation=90)
            plt.show()


collect_data_button = Button(
    root, text="Collect data from directory files", command=collect_data
)
collect_data_button.grid(row=1, column=0, columnspan=2)

# window to check that we got all the files
Analyze_Button = Button(root, text="Analyze these files", command=analyze_csv)
Analyze_Button.grid(row=3, column=0, columnspan=2)

root.mainloop()

# csv_file = open('JeffJanafUpdate9-27-21.csv')

# Reading the csv file, and getting rid of the headeer
# #csv_data = csv.reader(csv_file)
# #csv_rows = list(csv_data)
# #header = csv_rows[0]
# #csv_rows = csv_rows[1:]
# Load JANAF csv, read it, getting rid of the header
# #janaf_name_csv = open('JeffJANAF_data.csv')
# #janaf_name_data = csv.reader(janaf_name_csv)
# #janaf_name_rows = list(janaf_name_data)
