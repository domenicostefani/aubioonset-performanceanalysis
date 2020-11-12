modded <- read.csv("MODDED/acoustic_guitar_percussive_keybed_f_DavRos_20200820.txt",sep="\t", header = FALSE)
standard <- read.csv("STANDARD/acoustic_guitar_percussive_keybed_f_DavRos_20200820.txt",sep ="\t", header = FALSE)

absmax <- 0.00000000000000000000001

delay <- 275.0 / 48000.0
comparison <- data.frame(standard$V1+delay,modded$V1)
comparison$difference = comparison$standard.V1...delay - comparison$modded.V1
comparison$difference = round(comparison$difference,4)
curmax <- max(comparison$difference)
absmax <- max(absmax,curmax)

setwd("MODDED")
temp = list.files(pattern="*.txt")
allmodded = lapply(temp, read.csv, sep="\t", header=FALSE)


setwd("../STANDARD")
temp = list.files(pattern="*.txt")
allstandard = lapply(temp, read.csv, sep="\t", header=FALSE)
setwd("..")

getwd()

stopifnot(length(allstandard) == length(allmodded))

totlength = 0
for(i in 1:length(allstandard)){
  totlength <- totlength + nrow(data.frame(allstandard[i]))
}
comparison <- c(totlength)

cumulative_i = 0
for(i in 1:length(allstandard))
{
  dfS <- data.frame(allstandard[i])
  dfM <- data.frame(allmodded[i])
  stopifnot(nrow(dfS) == nrow(dfM))
  for(j in 1:nrow(dfS))
  {
    index = cumulative_i+j
    print(index)
    val <- dfS$V1[j]+delay-dfM$V1[j]
    comparison[index] <- val
    abs(val)
  }
  cumulative_i <- cumulative_i + nrow(dfS)
}


comp <- data.frame(comparison)
