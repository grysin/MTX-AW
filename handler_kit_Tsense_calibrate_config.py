#!/user/bin/env python3

program_name = "handler_kit_Tsense_calibrate_config"
program_version = "20220324"
program_title = "Tsense Kit Calibrate Config"

config_prog_name = program_name
config_prog_version = program_version
input_data_type = 1
# search_format = "config_file"
search_format = "kit_file"
upload_permissions = ["ra2325"]
user_list = []
usage = []
handler_list = [
    "MTXX",
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
    "MTXA11",
    "MTXA12",
    "MTXA13",
]
custom_apps_list = ["kit_file_history_extractor.py", "matrix_kit_files_summary.py"]
Drive_letter_read = "t:"
Drive_letter_write = "s:"
stdf_extractor = "stdfExtract.exe"
stdf_extractor_path = "C:/Program Files (x86)/stdfExtractor"
maintStdfDir = "\\\\atxtest\\UFLEX_dev\\DougG\\temp_data\\T-sense Calibration"
maintSchedDir = "\\\\Tx30cifs01\\tx32file15\\Groups\\Tech_Support\\Main\\Matrix_Handler\\Matrix T-Sense\\Matrix T-sense Calibration Schedule.xlsx"
workingdir = "Tsense calibration"
clean_workdir_on_startup = 1
check_revision_on_startup = 1
check_config_revision = 1
# relese_archives = r'"\\npi1412-09\C$\Program Files (x86)\Anaconda2\matt\kit_file_editing\Release_Archives"'
# config_relese_archives = r'"\\npi1412-09\C$\Program Files (x86)\Anaconda2\matt\kit_file_editing\Release_Archives"'
release_archives = r'"\\Tx30cifs01\TX32FILE16\Groups\Probe\NPI Improvement Teams\Tsense\Analysis Scripts\kit_file_editing\Release_Archives"'
config_release_archives = r'"\\Tx30cifs01\TX32FILE16\Groups\Probe\NPI Improvement Teams\Tsense\Analysis Scripts\kit_file_editing\Release_Archives"'
inputInitialDir = "Tsense Calibration"
inputkitfilename = "Enter"
inputresultsfilename = workingdir + "/Hot/*"
kitconfigfilename = "Enter"
inputkitfilename_b = "none"
inputresultsfilename_b = workingdir + "/Cold/*"
kitconfigfilename_b = "Enter"
outputfilename = "update_cal_values.csv"
outputdir = "."
# connect_string = 'gntcaadm/gntcaadm01@ohntweb_12c.am.freescale.net:1521/ohntweb'
connect_string = (
     "gntcaadm/gntcaadm01@OHNTWEBDB_VCS.am.freescale.net:1522/OHNTWEB.AM.FREESCALE.NET"
)
ndn = "mtxx"
# c4_value = 1
username = "username"
password = "password"
valid_user = False

## if update_database = 1 output results are recorded in the database
## controled in configuration
# update_database=0
update_database = 1

## if legacy trace analysis = 1 old style T0 and Tinf calculates are used
## if legacy_trace_analysis = 0 non-linear curve fit to estimate T0 and Tinf is used
## controled in configuration
# legacy_trace_analysis=0
legacy_trace_analysis = 1

## if review fits = 1 a plot showing raw data and non-linear fit is shown for every die tested
review_fits = 0

## input data control factors
min_num_readings = 5
disable_min_readings = 0
## number of trace data points to average for T0 estimate
T0_num_pts = 5
## number of trace data points to average for Tinf estimate
Tinf_num_pts = 10
## maximum number of degrees C Tinf can differ from target temp and still be included
Tinf_flier_filter = 20
T0_flier_filter = 40

## offset correction control factors
max_offset = 40
disable_max_offset = 0
max_temp = 200
min_temp = -170

global_T0 = 150
global_Tinf = 150
global_b = 0.087
# global_b = 0.17
# global_b = 0.26
force_time_const = 1
wu = "fsl\\ultraflexdev"
wup = "Development1"

optimal_plus_keep_list = {
    "Lot": "lot_id",
    "Operation": "tst_cod",
    "Product": "stdf_file",
    "Die Test Order": "part_id",
    "Wafer": "wf_id",
    "Hard Bin": "HBIN_NUM",
    "Site": "SITE_NUM",
    "Soft Bin": "SBIN_NUM",
    "Die Test Time": "TEST_T",
    "DieX": "die_x",
    "DieY": "die_y",
    "ECID": "X_ECID",
    "Loadboard": "X_Loadboard",
    "Temperature": "tst_temp",
    "Test Floor": "facil_id",
    "Facility": "facil_id",
    "Tester": "none_nam",
    "Tester Type": "tstr_typ",
    "Prober/Handler": "X_handler_id",
    "Prober/Handler Type": "X_handler_type",
}

diamond_keep_list = {
    "MASK": "stdf_file",
    "LOTID": "lot_id",
    "FT_LOT_ID": "lot_id",
    "FT_TEST_CD": "tst_cod",
    "FT_PROC_ID": "X_FT_PROC_ID",
    "FT_JOB_NAM": "job_nam",
    "FT_JOB_REV": "job_rev",
    "FT_TEST_TEMP": "tst_temp",
    "FT_FACILITY": "facil_id",
    "FT_TESTER_TYPE": "tstr_typ",
    "FT_TESTER_ID": "node_nam",
    "FT_LOADBOARD": "X_FT_LOADBOARD",
    "FT_HANDLER_ID": "X_FT_HANDLER_ID",
    "FT_HANDLER_TYPE": "X_FT_HANDLER_TYPE",
    "FT_PACKAGE_CD": "X_FT_PACKAGE_CD",
    "FT_PACKAGE_DESC": "X_FT_PACKAGE_DESC",
    "FT_WAFER_ID": "x_FT_WAFER_ID",
    "DIEX": "die_x",
    "DIEY": "die_y",
    "WAFER_NUM": "wf_id",
    "FT_ECID": "X_FT_ECID",
    "FT_HARD_BIN": "HBIN_NUM",
    "FT_SOFT_BIN": "SBIN_NUM",
    "FT_SITE_NUM": "SITE_NUM",
    "FT_HEAD_NUM": "HEAD_NUM",
    "FT_PART_ID": "part_id",
    "FT_TEST_DUR": "TEST_T",
}

keep_list = [
    "stdf_file",
    "lot_id",
    "wf_id",
    "exec_typ",
    "exec_ver",
    "proc_id",
    "setup_t",
    "start_t",
    "finish_t",
    "facil_id",
    "rtst_cod",
    "job_rev",
    "job_nam",
    "load_id",
    "dib_id",
    "part_typ",
    "tstr_typ",
    "node_nam",
    "oper_nam",
    "test_cod",
    "tst_temp",
    "mode_cod",
    "part_id",
    "die_x",
    "die_y",
    "HEAD_NUM",
    "SITE_NUM",
    "HBIN_NUM",
    "HBIN_NAM",
    "SBIN_NUM",
    "SBIN_NAM",
    "NUM_TEST",
    "TEST_T",
    "chuck_used",
]

zone_list = [
    "Left_TS_1A",
    "Left_TS_1B",
    "Left_TS_1C",
    "Left_TS_1D",
    "Left_TS_2A",
    "Left_TS_2B",
    "Left_TS_2C",
    "Left_TS_2D",
    "Left_TS_3A",
    "Left_TS_3B",
    "Left_TS_3C",
    "Left_TS_3D",
    "Left_TS_4A",
    "Left_TS_4B",
    "Left_TS_4C",
    "Left_TS_4D",
    "Right_TS_1A",
    "Right_TS_1B",
    "Right_TS_1C",
    "Right_TS_1D",
    "Right_TS_2A",
    "Right_TS_2B",
    "Right_TS_2C",
    "Right_TS_2D",
    "Right_TS_3A",
    "Right_TS_3B",
    "Right_TS_3C",
    "Right_TS_3D",
    "Right_TS_4A",
    "Right_TS_4B",
    "Right_TS_4C",
    "Right_TS_4D",
    "Contactor",
]

# chuck_string_list = ["chuck_used","chuck_read","MATRIX_CHUCK","GPIB_check_read"]
chuck_string_list = [
    "chuck_used",
    "chuck_read",
    "MATRIX_CHUCK",
    "matrix_chuck",
    "Chuck_Read",
]

temp_string_list = ["> ia_tsenseXtdiode_trace.dm.x.x.temp", "> ia_thermXtdiode_temperature.dm.x.x.x_spec_vn"]

dependent_files = ["STDF_Archive_Editor.py"]
