

SAVEPLOT = TRUE

if(!SAVEPLOT){
  library(tcltk)
}

dir = (tail(unlist(strsplit(getwd(),"/")),1))
CSV_PATH=""
if(dir == "r_analysis"){
  CSV_PATH = "../../output/onset_delay.csv"
}else if(dir == "src"){
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

sprintf("%d  onsets were labeled",length(na.omit(onsets$onset_labeled)))

accuracy = true_predictions / total
sprintf("accuracy: %.10f",accuracy)

precision = true_predictions / (true_predictions + FP)
recall    = true_predictions / (true_predictions + FN)


sprintf("precision: %.10f",precision)
sprintf("recall: %.10f",recall)
f1    = 2.0 * ((precision*recall)/(precision+recall))

sprintf("f1-score: %.10f",f1)


print("Delay summary (in ms)")
delays_ms = na.omit(onsets$difference)*1000
summary(delays_ms)
sprintf("avg_delay:  %.10f",mean(delays_ms))








print("Per Sound type")
soundtype_name <- c("percussive","pitched")
soundtype_pattern <- c("_percussive_", "_pitched_")

accuracies = c()
precisions = c()
recalls = c()
f1s = c()

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
  f1_tmp <- 2.0 * ((precision_temp*recall_temp)/(precision_temp+recall_temp))

  print("")
  print(soundtype_name[i])
  print(paste(length(na.omit(onset_labeled_temp))," ",soundtype_name[i]," onsets were labeled"))
  cat(sprintf("%s  accuracy %.10f\n",soundtype_name[i],accuracy_temp))
  cat(sprintf("%s  precision %.10f\n",soundtype_name[i],precision_temp))
  cat(sprintf("%s  recall %.10f\n",soundtype_name[i],recall_temp))
  cat(sprintf("%s  f1-score %.10f\n",soundtype_name[i],f1_tmp))

  accuracies[i] <- accuracy_temp
  precisions[i] <- precision_temp
  recalls[i] <- recall_temp
  f1s[i] <- f1_tmp

  print("Delay summary (in ms)")
  temp_delays_ms = na.omit(difference_temp)*1000
  print(summary(temp_delays_ms))
}

print("Average metrics per soundtype")
sprintf("avg_accuracy: %.10f",mean(accuracies))
sprintf("avg_precision: %.10f",mean(precisions))
sprintf("avg_recall: %.10f",mean(recalls))
sprintf("avg_f1-score: %.10f",mean(f1s))











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
  cat(sprintf("%s  accuracy %.10f\n",intensities_name[i],accuracy_temp))
  cat(sprintf("%s  precision %.10f\n",intensities_name[i],precision_temp))
  cat(sprintf("%s  recall %.10f\n",intensities_name[i],recall_temp))
  cat(sprintf("%s  f1-score %.10f\n",intensities_name[i],f1_tmp))
}




print("Per Technique")
technique_name <- c("keybed", "kick","lowerside","thumb","palmmute","naturalharmonics","picknearbridge","soundhole")
technique_pattern <- c("keybed", "kick","lowerside","thumb","palmmute","naturalharmonics","picknearbridge","soundhole")

accuracies_by_technique = c()
precisions_by_technique = c()
recalls_by_technique = c()
f1s_by_technique = c()

for(i in 1:length(technique_name)){
  difference_temp = onsets$difference[grepl(technique_pattern[i],onsets$recording)]
  onset_labeled_temp = onsets$onset_labeled[grepl(technique_pattern[i],onsets$recording)]
  onset_extracted_temp = onsets$onset_extracted[grepl(technique_pattern[i],onsets$recording)]

  accuracy_temp <- length(na.omit(difference_temp)) / length(difference_temp)
  FP_temp = sum(is.na(onset_labeled_temp))
  FN_temp = sum(is.na(onset_extracted_temp))
  true_predictions_temp=length(na.omit(difference_temp))
  precision_temp <- true_predictions_temp / (true_predictions_temp + FP_temp)
  recall_temp <- true_predictions_temp / (true_predictions_temp + FN_temp)
  f1_tmp <- 2.0 * ((precision_temp*recall_temp)/(precision_temp+recall_temp))

  print("")
  print(paste("Technique: ",technique_name[i]))
  print(paste(length(na.omit(onset_labeled_temp))," ",technique_name[i]," onsets were labeled"))
  cat(sprintf("%s  accuracy %.10f\n",technique_name[i],accuracy_temp))
  cat(sprintf("%s  precision %.10f\n",technique_name[i],precision_temp))
  cat(sprintf("%s  recall %.10f\n",technique_name[i],recall_temp))
  cat(sprintf("%s  f1-score %.10f\n",technique_name[i],f1_tmp))

  accuracies_by_technique[i] <- accuracy_temp
  precisions_by_technique[i] <- precision_temp
  recalls_by_technique[i] <- recall_temp
  f1s_by_technique[i] <- f1_tmp

  print("Delay summary (in ms)")
  temp_delays_ms = na.omit(difference_temp)*1000
  print(summary(temp_delays_ms))
}

print("Average metrics per technique")
sprintf("avg_tech_accuracy: %.10f",mean(accuracies_by_technique))
sprintf("avg_tech_precision: %.10f",mean(precisions_by_technique))
sprintf("avg_tech_recall: %.10f",mean(recalls_by_technique))
sprintf("avg_tech_f1-score: %.10f",mean(f1s_by_technique))












if(SAVEPLOT){
  pdf(file = "./delay.pdf",   # The directory you want to save the file in
      width = 5, # The width of the plot in inches
      height = 8) # The height of the plot in inches
}else{
  x11()
  prompt  <- "Close plot?"
  extra   <- ""
}

bp = boxplot(delays_ms,main="Onset Detection Delay (ms)",ylab="Delay(ms)", ylim=c(0.0,20.0), yaxt="n")
axis(2, at=seq(0, 20, by=1),las=1)
lower_adj = bp$stats[1]
upper_adj = bp$stats[5]
sprintf("adjacent min-max:  %.10f   %.10f",lower_adj,upper_adj)
percentage = 0
for(onsetdiff in na.omit(onsets$difference)){
  if(onsetdiff*1000 < upper_adj && onsetdiff*1000 > lower_adj){
    percentage = percentage + 1
  }
}
percentage = percentage/length(na.omit(onsets$difference))
print(paste(percentage," of the correctly detected onsets fall in the range [",lower_adj,",",upper_adj,"]ms"))

if(SAVEPLOT){
  dev.off()
}else{
  capture <- tk_messageBox(message = prompt, detail = extra)
}


if(SAVEPLOT){
  pdf(file = "./metrics.pdf",   # The directory you want to save the file in
      width = 6, # The width of the plot in inches
      height = 8) # The height of the plot in inches
}

metrics <- c(c(accuracy,precision,recall))
bx <- barplot(metrics,
              names.arg = c("Accuracy","Precision","Recall"),
              ylim=c(0,1))

text(bx,metrics*.9,labels = format(round(metrics, 4), nsmall = 4))
if(!SAVEPLOT){
  capture <- tk_messageBox(message = prompt, detail = extra)
}else{
  dev.off()
}
