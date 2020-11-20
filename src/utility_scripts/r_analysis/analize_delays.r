library(tcltk)

dir = (tail(unlist(strsplit(getwd(),"/")),1))
CSV_PATH=""
if(dir == "r_analysis"){
  CSV_PATH = "../../output/onset_delay.csv"
}else if(dir == "Aubio Analysis"){
  CSV_PATH = "output/onset_delay.csv"
}else{
  print("Call from a project directory")
  exit()
}
onsets = read.csv(CSV_PATH, na.strings = "NAN")


total = nrow(onsets)
true_predictions = length(na.omit(onsets$difference))
FP = sum(is.na(onsets$onset_labeled))
FN = sum(is.na(onsets$onset_extracted))
# Sanity checks
stopifnot(FP+FN == total - true_predictions)

accuracy = true_predictions / total
print(paste("accuracy:",accuracy))

precision = true_predictions / (true_predictions + FP)
recall    = true_predictions / (true_predictions + FN)


print(paste("precision:",precision))
print(paste("recall:",recall))

print("Delay summary (in ms)")
delays_ms = na.omit(onsets$difference)*1000
summary(delays_ms)


print("Per Sound type")
soundtype_name <- c("percussive","pitched")
soundtype_pattern <- c("_percussive_", "_pitched_")
for(i in 1:length(soundtype_name)){
  difference_temp = onsets$difference[grepl(soundtype_pattern[i],onsets$recording)]
  onset_labeled_temp = onsets$onset_labeled[grepl(soundtype_pattern[i],onsets$recording)]
  onset_extracted_temp = onsets$onset_extracted[grepl(soundtype_pattern[i],onsets$recording)]
  
  accuracy_temp <- length(na.omit(difference_temp)) / length(difference_temp)
  FP_temp = sum(is.na(onset_labeled_temp))
  FN_temp = sum(is.na(onset_extracted_temp))
  true_predictions_temp=length(na.omit(difference_temp))
  precision_temp <- true_predictions_temp / (true_predictions_temp + FP_temp)
  recall_temp <- true_predictions_temp / (true_predictions_temp + FN_temp)
  
  print("")
  print(soundtype_name[i])
  print(paste(soundtype_name[i]," accuracy",accuracy_temp))
  print(paste(soundtype_name[i]," precision",precision_temp))
  print(paste(soundtype_name[i]," recall",recall_temp))
  
  print("Delay summary (in ms)")
  temp_delays_ms = na.omit(difference_temp)*1000
  print(summary(temp_delays_ms))
}


print("Per Intensity metrics")
intensities_name <- c("piano","mezzoforte","forte")
intensities_pattern <- c("_p_", "_mf_", "_f_")

for(i in 1:length(intensities_name)){
  difference_temp = onsets$difference[grepl(intensities_pattern[i],onsets$recording)]
  onset_labeled_temp = onsets$onset_labeled[grepl(intensities_pattern[i],onsets$recording)]
  onset_extracted_temp = onsets$onset_extracted[grepl(intensities_pattern[i],onsets$recording)]
  
  accuracy_temp <- length(na.omit(difference_temp)) / length(difference_temp)
  FP_temp = sum(is.na(onset_labeled_temp))
  FN_temp = sum(is.na(onset_extracted_temp))
  true_predictions_temp=length(na.omit(difference_temp))
  precision_temp <- true_predictions_temp / (true_predictions_temp + FP_temp)
  recall_temp <- true_predictions_temp / (true_predictions_temp + FN_temp)
  
  print("")
  print(intensities_name[i])
  print(paste(intensities_name[i]," accuracy",accuracy_temp))
  print(paste(intensities_name[i]," precision",precision_temp))
  print(paste(intensities_name[i]," recall",recall_temp))
}




x11()
prompt  <- "Close plot?"
extra   <- ""

boxplot(delays_ms,main="Onset Detection Delay (ms)",ylab="Delay(ms)")
capture <- tk_messageBox(message = prompt, detail = extra)

metrics <- c(c(accuracy,precision,recall))
bx <- barplot(metrics,
              names.arg = c("Accuracy","Precision","Recall"),
              ylim=c(0,1))

text(bx,metrics*.9,labels = format(round(metrics, 4), nsmall = 4))
capture <- tk_messageBox(message = prompt, detail = extra)

