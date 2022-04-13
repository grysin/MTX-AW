# Csv testing
import csv
import matplotlib.pyplot as plt
from collections import Counter
from numpy import source
from matplotlib.widgets import Button

csv_file = open("MTX-04-Alarm_Stats-2022_03_18_14_17_31.csv")

# Reading the csv file, and getting rid of the headeer
csv_data = csv.reader(csv_file)
csv_rows = list(csv_data)
time_title = csv_rows[0]
export_time = csv_rows[1]
blank = csv_rows[2]
header = csv_rows[3]
# make rows start at 1
csv_rows = csv_rows[4:]
# extract data out of each row
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
    part_count = row[27]
    cycle_count = row[28]
    user_id = row[29]
    handler_id = row[30]
    site_id = row[31]

    # alarm counting
    alarms.append(alarm_id)
    # check for duplicates

    # alarm time duration

print(time_elapsed)
alarms = Counter(alarms)
alarm_id_names = list(alarms.keys())
alarm_id_count = list(alarms.values())

plt.bar(range(len(alarms)), alarm_id_count, tick_label=alarm_id_names)
plt.xticks(rotation=90)
plt.show()
