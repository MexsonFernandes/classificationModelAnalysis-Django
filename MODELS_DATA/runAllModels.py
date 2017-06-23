
import os
import glob
resutlFileName="finalResult.csv"


#-------------------------------------------------------------
# Step 3: Model Execution
#-------------------------------------------------------------

# Decision Tree
os.system("Rscript decisionTree.R")

# Linear Model
os.system("Rscript linearModel.R")

# Neural Network
os.system("Rscript neuralNetwork.R")

# Random Forest
os.system("Rscript randomForest.R")

# SVM
os.system("Rscript svm.R")

# Ada Boost
os.system("Rscript adaBoost.R")

#-------------------------------------------------------------
# Step 4: Merging Result 
#-------------------------------------------------------------

listOfResultFiles = glob.glob('*Evaluation-Result.csv')
fwp=open(resutlFileName,"w")
fwp.write("Model,H,Gini,AUC,AUCH,KS,MER,MWL,Spec.Sens95,Sens.Spec95,ER,Sens,Spec,Precision,Recall,TPR,FPR,F,Youden,TP,FP,TN,FN,Accuracy,TotalTime\n")

for f in listOfResultFiles:
    i=1    
    for fp in open(f):
        if i==1:
            i=i+1
            continue
        fwp.write(fp)
        break

fwp.close()
print ("Done")
print ("Result is save in " + resutlFileName + "\n")


