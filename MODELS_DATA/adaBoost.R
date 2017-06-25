
# Credit: Dr. Prashant Singh Rana                             #

cat("\nAdaBoost")
startTime = proc.time()[3]
library(ada)
library(hmeasure)
modelName <- "adaBoost"
InputDataFileName="sample.csv"
training = 50      # Defining Training Percentage; Testing = 100 - Training
dataset <- read.csv(InputDataFileName)      # Read the datafile
dataset <- dataset[sample(nrow(dataset)),]  # Shuffle the data row wise.
totalDataset <- nrow(dataset)
target  <- names(dataset)[10]   # i.e. Cancer
inputs <- setdiff(names(dataset),target)
trainDataset <- dataset[1:(totalDataset * training/100),c(inputs, target)]
testDataset <- dataset[(totalDataset * training/100):totalDataset,c(inputs, target)]
formula <- as.formula(paste(target, "~", paste(c(inputs), collapse = "+")))
model <- ada(formula, trainDataset)
Predicted <- predict(model, testDataset)
PredictedProb <- predict(model, testDataset,type="prob")[,2]
Actual <- as.double(unlist(testDataset[target]))
ConfusionMatrix <- misclassCounts(Predicted,Actual)$conf.matrix


# Step 12.2: Evaluations Parameters
# AUC, ERR, Sen, Spec, Pre,Recall, TPR, FPR, etc 
EvaluationsParameters <- round(HMeasure(Actual,PredictedProb)$metrics,3)


# Step 12.3: Accuracy
accuracy <- round(mean(Actual==Predicted) *100,2)


# Step 12.4: Total Time
totalTime = proc.time()[3] - startTime



# Step 12.5: Plotting
# ROC and ROCH Curve
png(filename=paste(modelName,"-01-ROCPlot.png",sep=''))
plotROC(HMeasure(Actual,PredictedProb),which=1)
dev.off()

# H Measure Curve
png(filename=paste(modelName,"-02-HMeasure.png",sep=''))
plotROC(HMeasure(Actual,PredictedProb),which=2)
dev.off()

# AUC Curve
png(filename=paste(modelName,"-03-AUC.png",sep=''))
plotROC(HMeasure(Actual,PredictedProb),which=3)
dev.off()

# SmoothScoreDistribution Curve
png(filename=paste(modelName,"-04-SmoothScoreDistribution.png",sep=''))
plotROC(HMeasure(Actual,PredictedProb),which=4)
dev.off()


# Step 12.5: Save evaluation resut 
EvaluationsParameters$Accuracy <- accuracy
EvaluationsParameters$TotalTime <- totalTime
rownames(EvaluationsParameters)=modelName



#--------------------------------------------------------------
# Step 13: Writing to file
#--------------------------------------------------------------

# Step 13.1: Writing to file (evaluation result)
write.csv(EvaluationsParameters, file=paste(modelName,"-Evaluation-Result.csv",sep=''), row.names=TRUE)

# Step 13.2: Writing to file (Actual and Predicted)
write.csv(data.frame(Actual,Predicted), file=paste(modelName,"-ActualPredicted-Result.csv",sep=''), row.names=FALSE)



#--------------------------------------------------------------
# Step 14: Saving the Model
#--------------------------------------------------------------
save.image(file=paste(modelName,"-Model.RData",sep=''))


cat("\nDone")
cat("\nTotal Time Taken: ", totalTime," sec")



