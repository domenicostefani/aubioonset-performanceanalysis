
import glob
import os

MAX_ONSET_DIFFERENCE_S = 0.3 # Onsets further apart than this interval will be considered different

def computeDifference(labels_file,extracted_file):
    #print(labels_file.readline())
    #print(extracted_file.readline())
    
    end_flag = False
    counter = 0
    while not end_flag:
        lbl_line = labels_file.readline()
        ext_line = extracted_file.readline()
        if lbl_line is "":
            end_flag = True
        else:
            label_value = float(lbl_line.split()[0])
            print(str(counter) + " " +  str(label_value))
        counter += 1











onsets_labeled = glob.glob("onsets_labeled/*.txt")

for filename in onsets_labeled:
    filename = os.path.basename(filename)
    file_labels = open("onsets_labeled/"+filename, "r")
    file_extrac = open("onsets_extracted/"+filename, "r")
    computeDifference(file_labels,file_extrac)
    file_labels.close()
    file_extrac.close()


