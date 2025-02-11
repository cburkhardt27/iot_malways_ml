import argparse
import numpy as np
import pandas as pd
import random
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import cross_validate, cross_val_score, train_test_split
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, roc_auc_score
from sklearn.naive_bayes import GaussianNB
import pdb

def file_to_numpy(filename):
    """
    Read an input file and convert it to numpy
    """
    df = pd.read_csv(filename)
    return df.to_numpy()

def file_to_numpy_select_cols(filename,columnList):
    """
    Read an input file and convert it to numpy
    """
    df = pd.read_csv(filename)
    df_columns = sorted(df)
    missing_cols = list(set(columnList) - set(df_columns))

    # add dummy row to every missing column
    for col in missing_cols:
        df[col] = 0

    # select on the relevant columns (in the right order!) from df
    df_updated = df[columnList]

    return df_updated.to_numpy()

def acc_score(yHat,yActual):
    correct = 0
    for i in range(len(yHat)):
        if yHat[i] == yActual[i]:
            correct +=1
       # else:
         #   print("WRONG: PREDICTED ", yHat[i], " ACTUAL: ", yActual[i], " TYPE: ", yActual[i,1] )
    acc = correct / len(yHat)
    return acc

def trainModel(xData, yData):
    xTrain, xTest, yTrain, yTest = train_test_split(xData,yData, test_size=0.3,shuffle=True) 

    gnb = GaussianNB()

  #  pdb.set_trace()
    gnb.fit(xTrain,yTrain[:,0].astype(int))
    yHat_train = gnb.predict(xTrain)
    # take the above
    acc_train = acc_score(yHat_train,yTrain[:,0])
    print("TRAIN ACCURACY: ", acc_train)

    yHat = gnb.predict(xTest)
    auc = roc_auc_score(yTest[:,0].astype(int), gnb.predict(xTest))
    acc = acc_score(yHat,yTest[:,0].astype(int))
    cm = confusion_matrix(yTest[:,0].astype(int),yHat)
  #  print("TRAIN CONFUSION MATRIX: ", cm)
    return gnb, acc, auc, cm

def main():
    print("NAIVE BAYES")

    print("DATA 43")
    xTrainFile_43 = "C:/Users/Claire Burkhardt/CS_334/iot_malware_detection/preprocessing/43re_xTrain.csv"
    yTrainFile_43 = "C:/Users/Claire Burkhardt/CS_334/iot_malware_detection/preprocessing/43re_yTrain.csv"

    columns_43 = ['id.resp_p']

    xData_43 = file_to_numpy_select_cols(xTrainFile_43,columns_43)
    yData_43 = file_to_numpy(yTrainFile_43)

    gnbModel_43, accTrain_43, auc_43, cm_43 = trainModel(xData_43,yData_43)
    print("TEST ACCURACY: ", accTrain_43)
    print("TEST AUC", auc_43)
    print("CONFUSION MATRIX :")
    print(cm_43)
    
########################################################
    print("DATA 34:")
    xTrainFile_34 = "C:/Users/Claire Burkhardt/CS_334/iot_malware_detection/preprocessing/34re_xTrain.csv"
    yTrainFile_34 = "C:/Users/Claire Burkhardt/CS_334/iot_malware_detection/preprocessing/34re_yTrain.csv"

    columns_34 = ['missed_bytes','resp_ip_bytes','resp_bytes','service_http', 'history_ShAdDaf', 'conn_state_S3','service_irc','id.resp_p','history_S','conn_state_S0','service_dns', 'history_C', 'conn_state_OTH', 'history_Dd', 'conn_state_SF', 'id.resp_h','history_D','id.orig_p', 'proto_tcp','proto_udp']

    xData_34 = file_to_numpy_select_cols(xTrainFile_34,columns_34)
    yData_34 = file_to_numpy(yTrainFile_34)

    gnbModel_34, accTrain_34, auc_34, cm_34 = trainModel(xData_34,yData_34)
    print("TEST ACCURACY: ", accTrain_34)
    print("TEST AUC", auc_34)
    print("CONFUSION MATRIX: (0,0)-TN, (1,0)-FN, (1,1)-TP, (0,1)-FP")
    print(cm_34)
    
######################################################################
    print("DATA 48:")
    xTrainFile_48 = "C:/Users/Claire Burkhardt/CS_334/iot_malware_detection/preprocessing/48_500Kre_xTrain.csv"
    yTrainFile_48 = "C:/Users/Claire Burkhardt/CS_334/iot_malware_detection/preprocessing/48_500Kre_yTrain.csv"

    columns_48 = ['orig_bytes','id.orig_h','id.orig_p','id.resp_p','history_D','conn_state_SH']

    xData_48 = file_to_numpy_select_cols(xTrainFile_48,columns_48)
    yData_48 = file_to_numpy(yTrainFile_48)
    gnbModel_48, accTrain_48, auc_48, cm_48 = trainModel(xData_48,yData_48)
    # MODEL PREDICTS FALSE FOR EVERYTHING
    print("TEST ACCURACY: ", accTrain_48)
    print("TEST AUC", auc_48)
    print("CONFUSION MATRIX: (0,0)-TN, (1,0)-FN, (1,1)-TP, (0,1)-FP")
    print(cm_48)

######################################################################
    print("DATA 35:")
    xTrainFile_35 = "C:/Users/Claire Burkhardt/CS_334/iot_malware_detection/preprocessing/35_500Kre_xTrain.csv"
    yTrainFile_35 = "C:/Users/Claire Burkhardt/CS_334/iot_malware_detection/preprocessing/35_500Kre_yTrain.csv"

    columns_35 = ['id.resp_p','id.orig_p','id.resp_h','duration']

    xData_35 = file_to_numpy_select_cols(xTrainFile_35,columns_35)
    yData_35 = file_to_numpy(yTrainFile_35)
    gnbModel_35, accTrain_35, auc_35, cm_35 = trainModel(xData_35,yData_35)
    # MODEL PREDICTS FALSE FOR EVERYTHING
    print("TEST ACCURACY: ", accTrain_35)
    print("TEST AUC", auc_35)
    print("CONFUSION MATRIX: (0,0)-TN, (1,0)-FN, (1,1)-TP, (0,1)-FP")
    print(cm_35)
###################################################################################
    print("\n\nTRAINING DATA ON OTHER MODELS:\n\n")
###################################################################################    
#train 43 on model 34
    print("\nTRAINING DATA 43 ON MODEL 34")
    xData_43_on_34 = file_to_numpy_select_cols(xTrainFile_43,columns_34)
    yHat_train_43_34 = gnbModel_34.predict(xData_43_on_34)
    acc_train_43_34 = acc_score(yHat_train_43_34,yData_43[:,0])
    print("ACCURACY OF DATA 43 on nb_model_34:", acc_train_43_34)

    auc_43_34 = roc_auc_score(yData_43[:,0], gnbModel_34.predict(xData_43_on_34))
    print("AUC on 43_34: ", auc_43_34)
    print("CONFUSION MATRIX: (0,0)-TN, (1,0)-FN, (1,1)-TP, (0,1)-FP")
    print(confusion_matrix(yData_43[:,0],yHat_train_43_34))
#train 43 on model 35
    print("\nTRAINING DATA 43 ON MODEL 35")
    xData_43_on_35 = file_to_numpy_select_cols(xTrainFile_43,columns_35)
    yHat_train_43_35 = gnbModel_35.predict(xData_43_on_35)
    acc_train_43_35 = acc_score(yHat_train_43_35,yData_43[:,0])
    print("ACCURACY OF DATA 43 on nb_model_35:", acc_train_43_35)
    auc_43_35 = roc_auc_score(yData_43[:,0], gnbModel_35.predict(xData_43_on_35))
    print("AUC on 43_35: ", auc_43_35)
    print("CONFUSION MATRIX: (0,0)-TN, (1,0)-FN, (1,1)-TP, (0,1)-FP")
    print(confusion_matrix(yData_43[:,0],yHat_train_43_35))
#train 43 on model 48
    print("\nTRAINING DATA 43 ON MODEL 48")
    xData_43_on_48 = file_to_numpy_select_cols(xTrainFile_43,columns_48)
    yHat_train_43_48 = gnbModel_48.predict(xData_43_on_48)
    acc_train_43_48 = acc_score(yHat_train_43_48,yData_43[:,0])
    print("ACCURACY OF DATA 43 on nb_model_48:", acc_train_43_48)
    auc_43_48 = roc_auc_score(yData_43[:,0], gnbModel_48.predict(xData_43_on_48))
    print("AUC on 43_48: ", auc_43_48)
    print("CONFUSION MATRIX: (0,0)-TN, (1,0)-FN, (1,1)-TP, (0,1)-FP")
    print(confusion_matrix(yData_43[:,0],yHat_train_43_48))

#train 34 on model 43
# PREDICTS EVERYTHING AS BENIGN; THE .91 IS DECEIVING
    print("\nTRAINING DATA 34 ON MODEL 43")
    xData_34_on_43 = file_to_numpy_select_cols(xTrainFile_34,columns_43)
    yHat_train_34_43 = gnbModel_43.predict(xData_34_on_43)
    acc_train_34_43 = acc_score(yHat_train_34_43,yData_34[:,0])
    print("ACCURACY OF DATA 34 on nb_model_43:", acc_train_34_43)
    auc_34_43 = roc_auc_score(yData_34[:,0], gnbModel_43.predict(xData_34_on_43))
    print("AUC on 34_43: ", auc_34_43)
    print("CONFUSION MATRIX: (0,0)-TN, (1,0)-FN, (1,1)-TP, (0,1)-FP")
    print(confusion_matrix(yData_34[:,0],yHat_train_34_43))

# train 34 on 48
    print("\nTRAINING DATA 34 ON MODEL 48")
    xData_34_on_48 = file_to_numpy_select_cols(xTrainFile_34,columns_48)
    yHat_train_34_48 = gnbModel_48.predict(xData_34_on_48)
    acc_train_34_48 = acc_score(yHat_train_34_48,yData_34[:,0])
    print("ACCURACY OF DATA 34 on nb_model_43:", acc_train_34_43)
    auc_34_48 = roc_auc_score(yData_34[:,0], gnbModel_48.predict(xData_34_on_48))
    print("AUC on 34_48: ", auc_34_48)
    print("CONFUSION MATRIX: (0,0)-TN, (1,0)-FN, (1,1)-TP, (0,1)-FP")
    print(confusion_matrix(yData_34[:,0],yHat_train_34_48))
# train 34 on 35
    print("\nTRAINING DATA 34 ON MODEL 35")
    xData_34_on_35 = file_to_numpy_select_cols(xTrainFile_34,columns_35)
    yHat_train_34_35 = gnbModel_35.predict(xData_34_on_35)
    acc_train_34_35 = acc_score(yHat_train_34_35,yData_34[:,0])
    print("ACCURACY OF DATA 34 on nb_model_35:", acc_train_34_35)
    auc_34_35 = roc_auc_score(yData_34[:,0], gnbModel_35.predict(xData_34_on_35))
    print("AUC on 34_35: ", auc_34_35)
    print("CONFUSION MATRIX: (0,0)-TN, (1,0)-FN, (1,1)-TP, (0,1)-FP")
    print(confusion_matrix(yData_34[:,0],yHat_train_34_35))
###################################################################################

######################################################################

#train 35 on model 43
    print("\nTRAINING DATA 35 ON MODEL 43")
    xData_35_on_43 = file_to_numpy_select_cols(xTrainFile_35,columns_43)
    yHat_train_35_43 = gnbModel_43.predict(xData_35_on_43)
    acc_train_35_43 = acc_score(yHat_train_35_43,yData_35[:,0])
    print("ACCURACY OF DATA 35 on nb_model_43:", acc_train_35_43)
    auc_35_43 = roc_auc_score(yData_35[:,0], gnbModel_43.predict(xData_35_on_43))
    print("AUC on 35_43: ", auc_35_43)
    print("CONFUSION MATRIX: (0,0)-TN, (1,0)-FN, (1,1)-TP, (0,1)-FP")
    print(confusion_matrix(yData_35[:,0],yHat_train_35_43))
#train 35 on model 34
    print("\nTRAINING DATA 35 ON MODEL 34")
    xData_35_on_34 = file_to_numpy_select_cols(xTrainFile_35,columns_34)
    yHat_train_35_34 = gnbModel_34.predict(xData_35_on_34)
    acc_train_35_34 = acc_score(yHat_train_35_34,yData_35[:,0])
    print("ACCURACY OF DATA 35 on nb_model_34:", acc_train_35_34)
    auc_35_34 = roc_auc_score(yData_35[:,0], gnbModel_34.predict(xData_35_on_34))
    print("AUC on 35_34: ", auc_35_34)
    print("CONFUSION MATRIX: (0,0)-TN, (1,0)-FN, (1,1)-TP, (0,1)-FP")
    print(confusion_matrix(yData_35[:,0],yHat_train_35_34))
#train 35 on model 48
    print("\nTRAINING DATA 35 ON MODEL 48")
    xData_35_on_48 = file_to_numpy_select_cols(xTrainFile_35,columns_48)
    yHat_train_35_48 = gnbModel_48.predict(xData_35_on_48)
    acc_train_35_48 = acc_score(yHat_train_35_48,yData_35[:,0])
    print("ACCURACY OF DATA 35 on nb_model_48:", acc_train_35_48)
    auc_35_48 = roc_auc_score(yData_35[:,0], gnbModel_48.predict(xData_35_on_48))
    print("AUC on 35_48: ", auc_35_48)
    print("CONFUSION MATRIX: (0,0)-TN, (1,0)-FN, (1,1)-TP, (0,1)-FP")
    print(confusion_matrix(yData_35[:,0],yHat_train_35_48))
######################################################################

######################################################################

#train 48 on model 43
    print("\nTRAINING DATA 48 ON MODEL 43")
    xData_48_on_43 = file_to_numpy_select_cols(xTrainFile_48,columns_43)
    yHat_train_48_43 = gnbModel_43.predict(xData_48_on_43)
    acc_train_48_43 = acc_score(yHat_train_48_43,yData_48[:,0])
    print("ACCURACY OF DATA 48 on nb_model_43:", acc_train_48_43)
    auc_48_43 = roc_auc_score(yData_48[:,0].astype(int), gnbModel_43.predict(xData_48_on_43))
    print("AUC on 48_43: ", auc_48_43)
    print("CONFUSION MATRIX: (0,0)-TN, (1,0)-FN, (1,1)-TP, (0,1)-FP")
    print(confusion_matrix(yData_48[:,0].astype(int),yHat_train_48_43.astype(int)))
#train 48 on model 34
    print("\nTRAINING DATA 48 ON MODEL 34")
    xData_48_on_34 = file_to_numpy_select_cols(xTrainFile_48,columns_34)
    yHat_train_48_34 = gnbModel_34.predict(xData_48_on_34)
    acc_train_48_34 = acc_score(yHat_train_48_34,yData_48[:,0])
    print("ACCURACY OF DATA 48 on nb_model_34:", acc_train_48_34)
    auc_48_34 = roc_auc_score(yData_48[:,0].astype(int), gnbModel_34.predict(xData_48_on_34))
    print("AUC on 48_34: ", auc_48_34)
    print("CONFUSION MATRIX: (0,0)-TN, (1,0)-FN, (1,1)-TP, (0,1)-FP")
    print(confusion_matrix(yData_48[:,0].astype(int),yHat_train_48_34.astype(int)))
#train 48 on model 35
    print("\nTRAINING DATA 48 ON MODEL 35")
    xData_48_on_35 = file_to_numpy_select_cols(xTrainFile_48,columns_35)
    yHat_train_48_35 = gnbModel_35.predict(xData_48_on_35)
    acc_train_48_35 = acc_score(yHat_train_48_35,yData_48[:,0])
    print("ACCURACY OF DATA 48 on nb_model_35:", acc_train_48_35)
    auc_48_35 = roc_auc_score(yData_48[:,0].astype(int), gnbModel_35.predict(xData_48_on_35))
    print("AUC on 48_35: ", auc_48_35)
    print("CONFUSION MATRIX: (0,0)-TN, (1,0)-FN, (1,1)-TP, (0,1)-FP")
    print(confusion_matrix(yData_48[:,0].astype(int),yHat_train_48_35.astype(int)))


if __name__ == "__main__":
    main()