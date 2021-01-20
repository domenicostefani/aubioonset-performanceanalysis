''' This takes filenames from folder1 and checks for the same filenames in folder2 '''

folder1 = "onsets_extracted"
folder2 = "onsets_labeled" 

import glob, os

folder1_filelist = glob.glob(folder1+"/*.txt")
folder2_filelist = glob.glob(folder2+"/*.txt")

print(str(len(folder1_filelist)) + " files in " + folder1)
print(str(len(folder2_filelist)) + " files in " + folder2)

for file in folder1_filelist:
    file = file[len(folder1)+1:-4]
    file = folder2 + "/" + file + "_extract.txt"
    # print(file)
    if folder2_filelist.count(file) > 0:
        print(file)
        os.system("mkdir -p "+folder2+"/common")
        os.system("cp "+file+ " " + folder2+"/common/")

