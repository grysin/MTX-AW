# Warning / Alarm Parsing
# Import packages needed to parse, analyze, plot data
from ast import Num
import csv
from doctest import master
from textwrap import fill
from turtle import bgcolor, width
from typing import List, OrderedDict
import numpy
import matplotlib.pyplot as plt
import re
from re import split
from collections import Counter
from numpy import source

# Import packages needed for user interface
from tkinter import *
import os
from tkinter import filedialog
from tkinter import ttk

# create the root window
root = Tk()
root.title("MTX Alarm / Warning Analysis")
root.geometry("375x135") # Width X Length
# creating the notebook for the tabs
tabs_notebook = ttk.Notebook(root)
tabs_notebook.pack(fill="both", expand=1)

# # create the tab for selecting files
file_tab = Frame(tabs_notebook)
file_tab.pack()
tabs_notebook.add(file_tab, text="File Select")

# what is on the file select tab
# prompt for working file directory

# frame for file directory input
input_csv_directory_frame = LabelFrame(file_tab, text="Input the CSV directory")
input_csv_directory_frame.pack(fill="both")
# originally blank white space for the file directory path
input_csv_directory = Label(input_csv_directory_frame, background="white", width=45)
input_csv_directory.grid(row=0,column=0)


# create the frame 
file_confirm_frame = LabelFrame(file_tab, text="Confirm Files to Analyze")
file_confirm_frame.pack(fill="both")

file_list = Listbox(file_confirm_frame, height=1)
file_list.pack(fill="both")

# define browse command that will be used with browse button
def browse():
    global input_directory
    # ask for a file name in the USB
    input_file = filedialog.askopenfilename()
    #print("input_file = ",input_file)
    # get the path of the file clicked on
    input_directory = (os.path.dirname(input_file))
    #print("input_directory = ",input_directory)
    # change the text of the whitespace to the file directory path
    input_csv_directory.config(text=input_directory)
    collect_data_button.config(state="normal")
    root.geometry("375x135")
    
# create a button that calls the browse command
csv_directory_browse = Button(input_csv_directory_frame, text="Browse", command=browse)
csv_directory_browse.grid(row=0,column=1)

# create function to collect all of the csv files in the input directory
def collect_data():
    # initialize list to catch csv files we care about
    file_list.delete(0,END)
    global csv_files
    csv_files = []
    for root_dir, dirs, files in os.walk(input_directory):
        for file in files:
            # only interested in csv files that match these two criteria
            if file.endswith(".csv") and file.startswith("MTX"):
                csv_files.append(file)
                file_list.insert(END, file)
    file_list.config(height=len(csv_files))
    height_adjust=root.winfo_height()+(14*len(csv_files))
    root.geometry(f"375x{height_adjust}")
    print(root.winfo_geometry())
    return

# create button to call function that collects csv files
collect_data_button = Button(
    file_tab, text="Collect data from directory files", command=collect_data, state="disabled"
)
collect_data_button.pack(fill="both")




# select how far back you want to collect data from 

# select which graphs you want to display, checkbox of MTX # and A/W, All A, All W, All A/W

# decide whether you want instance or duration

# get the description of the 
root.mainloop()


