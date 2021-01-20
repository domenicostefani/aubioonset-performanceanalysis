
''' Open first file, close previous '''

folder_audio = "./audiofiles"
folder_labels = "./onsets_extracted" 
folder_labels_labeled = "./onsets_labeled" 

import glob, os

def relist():
	folder_audio_filelist = glob.glob(folder_audio+"/*.wav")
	folder_labels_filelist = glob.glob(folder_labels+"/*.txt")
	folder_labels_labeled_filelist = glob.glob(folder_labels_labeled+"/*.txt")

	folder_audio_filelist.sort()
	folder_labels_filelist.sort()

	current_file = folder_audio_filelist[0]
	labels_file_extracted = folder_labels+"/"+os.path.basename(current_file[0:-4]) + ".txt"
	labels_file_labeled = folder_labels_labeled+"/"+os.path.basename(current_file[0:-4]) + ".txt"
	return folder_audio_filelist,folder_labels_filelist,folder_labels_labeled_filelist,current_file,labels_file_extracted,labels_file_labeled

folder_audio_filelist,folder_labels_filelist,folder_labels_labeled_filelist,current_file,labels_file_extracted,labels_file_labeled = relist()


print(current_file)
print(labels_file_extracted)
print(labels_file_labeled)
print(folder_labels_labeled_filelist.count(labels_file_labeled))

while folder_labels_labeled_filelist.count(labels_file_labeled) > 0:
	print("Moving " + labels_file_extracted + " " + current_file)
	os.system("mkdir -p "+folder_audio+"/done")
	os.system("mv "+current_file+" "+folder_audio+"/done")
	os.system("mkdir -p "+folder_labels+"/done")
	os.system("mv "+labels_file_extracted+" "+folder_labels+"/done")

	folder_audio_filelist,folder_labels_filelist,folder_labels_labeled_filelist,current_file,labels_file_extracted,labels_file_labeled = relist()
	print(current_file)
	print(labels_file_extracted)
	print(labels_file_labeled)

os.system("audacity "+current_file)

