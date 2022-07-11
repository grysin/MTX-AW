# CASTLE COUNTER

import csv
import pandas as pd

# file_name = "CAS15JAM.csv"
# file_name = "CAS20JAM.csv"
file_name = "CAS21JAM.csv"

csv_file = open(file_name)
# Reading the csv file, and getting rid of the headeer
csv_data = csv.reader(csv_file)
csv_rows = list(csv_data)
csv_rows = csv_rows[18:]
total_rows = len(csv_rows)

jam_stat = {
    "Missing Sort IC": 0,
    "Picker detects parts stuck": 0,
    "Picker can't detect all parts": 0,
    "TS Picker missing parts": 0,
    "PnP sensed an unexpected IC": 0,
    "TS Picker detected unexpected parts": 0,
    "PNP lost a device": 0,
    "Indexer failed to move boat": 0,
    "Motor stalled": 0,
}

text_exists_count = 0

for i, row in enumerate(csv_rows):
    print("i:", i, "\n", "row:", row[8])  # test
    date = row[3]

    try:
        jam_text = str(row[8])
        if "Missing sort IC" in jam_text:
            jam_stat["Missing Sort IC"] = jam_stat["Missing Sort IC"] + 1

        if "parts stuck" in jam_text:
            jam_stat["Picker detect parts stuck"] = (
                jam_stat["Picker detects parts stuck"] + 1
            )

        if "Picker can't detect all parts" in jam_text:
            jam_stat["Picker can't detect all parts"] = (
                jam_stat["Picker can't detect all parts"] + 1
            )

        if "TS Picker missing parts" in jam_text:
            jam_stat["TS Picker missing parts"] = (
                jam_stat["TS Picker missing parts"] + 1
            )

        if "PnP sensed an unexpected IC" in jam_text:
            jam_stat["PnP sensed an unexpected IC"] = (
                jam_stat["PnP sensed an unexpected IC"] + 1
            )

        if "TS Picker detected unexpected parts" in jam_text:
            jam_stat["TS Picker detected unexpected parts"] = (
                jam_stat["TS Picker detected unexpected parts"] + 1
            )

        if "Pick and Place lost" in jam_text:
            jam_stat["PNP lost a device"] = jam_stat["PNP lost a device"] + 1

    except NameError:
        pass

# text_exists_count = str(text_exists_count)
# total_rows = str(total_rows)
print(str(text_exists_count) + "/" + str(total_rows) + "contain text")
print(jam_stat)
