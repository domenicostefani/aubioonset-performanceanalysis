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
onsets = read.csv(CSV_PATH)


total = length(onsets$difference)
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
