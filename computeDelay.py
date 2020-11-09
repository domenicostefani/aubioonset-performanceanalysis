#!/usr/bin/env python3

import glob
import os
import re
from enum import Enum

class ParamType(Enum):
    INT = 1
    FLOAT = 2
    STR = 3

def readParam(param_name,default_value,param_type):
    try:
        param_str = input(param_name+"(default: " + str(default_value) + "): ")
        if param_str is not "":
            if param_type is ParamType.INT:
                param_val = int(param_str)
            elif param_type is ParamType.FLOAT:
                param_val = float(param_str)
            elif param_type is ParamType.STR:
                param_val = param_str
            else:
                print("ERROR! Wrong parameter type")
                exit()
        else:
            param_val = default_value;
            print("Using default value for " + param_name + " (" + str(default_value) + ")")
        return param_val
    except ValueError:
        print("ValueError")


print("Extracting all the onsets from the wav files in this folder")
print("Specify the parameter values or press <ENTER> for default")

BUFFER_SIZE = readParam("BUFFER_SIZE",256,ParamType.INT)
HOP_SIZE = readParam("HOP_SIZE",128,ParamType.INT)
SILENCE_THRESHOLD = readParam("SILENCE_THRESHOLD",-40.0,ParamType.FLOAT)
ONSET_THRESHOLD = readParam("ONSET_THRESHOLD",0.75,ParamType.FLOAT)
print("Available methods:<default|energy|hfc|complex|phase|specdiff|kl|mkl|specflux>")
ONSET_METHOD = readParam("ONSET_METHOD","default",ParamType.STR)
MINIMUM_INTER_ONSET_INTERVAL_SECONDS = readParam("MINIMUM_INTER_ONSET_INTERVAL_SECONDS",0.020,ParamType.FLOAT)

opts = "-B " + str(BUFFER_SIZE) + " -H " + str(HOP_SIZE) + " -s " + str(SILENCE_THRESHOLD) + " -t " + str(ONSET_THRESHOLD) + " -O " + str(ONSET_METHOD) + " -M " + str(MINIMUM_INTER_ONSET_INTERVAL_SECONDS) + ""

EXT_RES = os.popen("./utility_scripts/extractAllOnsets.sh " + opts).read()

AUBIODELAY_SAMPLES = int(re.search('[0-9]+', EXT_RES).group(0))
print("The delay introduced by aubioonset is " + str(AUBIODELAY_SAMPLES) + " samples")
SAMPLE_RATE = 48000
AUBIODELAY_S = AUBIODELAY_SAMPLES * 1.0 / SAMPLE_RATE
print("Delay in ms " + str(AUBIODELAY_S*1000.0))

MAX_ONSET_DIFFERENCE_S = 0.3 # Onsets further apart than this interval will be considered different

print("Onset further apart than " + str(MAX_ONSET_DIFFERENCE_S*1000.0) + "ms are considered different")

NAN_STR = "NAN"
SEP_STR = ","

def computeDifference(labels_file,extracted_file,out_file):
    end_flag = False
    lbl_line = labels_file.readline()
    ext_line = extracted_file.readline()
    while not end_flag:
        if lbl_line is "" and ext_line is "": #TODO check closing condition
            end_flag = True
        else:
            lbl_value = float(lbl_line.split()[0] if (lbl_line is not "") else "inf")
            ext_value = float(ext_line.split()[0] if (ext_line is not "") else "inf")
            diff = ext_value - lbl_value + AUBIODELAY_S

            if abs(diff) < MAX_ONSET_DIFFERENCE_S:
                out_file.write(str(lbl_value) + SEP_STR + str(ext_value) + SEP_STR + str(diff) + "\n")
                lbl_line = labels_file.readline()
                ext_line = extracted_file.readline()
            elif lbl_value < ext_value:
                out_file.write(str(lbl_value) + SEP_STR + NAN_STR + SEP_STR + NAN_STR + "\n")
                lbl_line = labels_file.readline()
            elif lbl_value > ext_value:
                out_file.write(NAN_STR + SEP_STR + str(ext_value) + SEP_STR + NAN_STR + "\n")
                ext_line = extracted_file.readline()

print("Computing the delays for:")

onsets_labeled = glob.glob("onsets_labeled/*.txt")
OUT_FILENAME="output/onset_delay.csv"
output_csv = open(OUT_FILENAME, "w")
output_csv.write("onset_labeled" + SEP_STR + "onset_extracted" + SEP_STR + "difference\n")


for filename in onsets_labeled:
    print(filename)
    filename = os.path.basename(filename)
    file_labels = open("onsets_labeled/"+filename, "r")
    file_extrac = open("onsets_extracted/"+filename, "r")
    computeDifference(file_labels,file_extrac,output_csv)
    file_labels.close()
    file_extrac.close()

output_csv.close()

print("Output can be found at " + OUT_FILENAME)

print("Calling R analysis script")
os.system("Rscript utility_scripts/r_analysis/analize_delays.r")
