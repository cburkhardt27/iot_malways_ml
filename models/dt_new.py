import pandas as pd
from sklearn.model_selection import cross_validate, cross_val_score, train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn import tree
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import confusion_matrix
import numpy as np
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
    #    else:
   #         print("WRONG: PREDICTED ", yHat[i], " ACTUAL: ", yActual[i] )
    acc = correct / len(yHat)
    return acc

def trainModel(xData, yData):
    xTrain, xTest, yTrain, yTest = train_test_split(xData,yData, test_size=0.3,shuffle=True) 
    clf = DecisionTreeClassifier(random_state=0)
    clf.fit(xTrain,yTrain[:,0].astype(int))
    yHat_train = clf.predict(xTrain)
    acc_train = accuracy_score(yHat_train,yTrain[:,0].astype(int))
    print("TRAIN ACCURACY: ", acc_train)

    yHat = clf.predict(xTest)
    acc = acc_score(yHat,yTest[:,0].astype(int))
    cm = confusion_matrix(yHat,yTest[:,0].astype(int))
  #  print("TRAIN CONFUSION MATRIX: ", cm)
    
    return clf, acc, cm

def main():
    print("DECISION TREE")
    print("DATA 43")
    xTrainFile_43 = "C:/Users/Claire Burkhardt/CS_334/iot_malware_detection/preprocessing/43re_xTrain.csv"
    yTrainFile_43 = "C:/Users/Claire Burkhardt/CS_334/iot_malware_detection/preprocessing/43re_yTrain.csv"

    columns_43 = ['id.resp_p']

    xData_43 = file_to_numpy_select_cols(xTrainFile_43,columns_43)
    yData_43 = file_to_numpy(yTrainFile_43)

    DTModel_43, accTrain_43, cm_43 = trainModel(xData_43,yData_43)
    print("TEST ACCURACY: ", accTrain_43)
    print("CONFUSION MATRIX :")
    print(cm_43)
    
########################################################
    print("DATA 34:")
    xTrainFile_34 = "C:/Users/Claire Burkhardt/CS_334/iot_malware_detection/preprocessing/34re_xTrain.csv"
    yTrainFile_34 = "C:/Users/Claire Burkhardt/CS_334/iot_malware_detection/preprocessing/34re_yTrain.csv"

    columns_34 = ['missed_bytes','resp_ip_bytes','resp_bytes','service_http', 'history_ShAdDaf', 'conn_state_S3','service_irc','id.resp_p','history_S','conn_state_S0','service_dns', 'history_C', 'conn_state_OTH', 'history_Dd', 'conn_state_SF', 'id.resp_h','history_D','id.orig_p', 'proto_tcp','proto_udp']

    xData_34 = file_to_numpy_select_cols(xTrainFile_34,columns_34)
    yData_34 = file_to_numpy(yTrainFile_34)

    DTModel_34, accTrain_34, cm_34 = trainModel(xData_34,yData_34)
    print("TEST ACCURACY: ", accTrain_34)
    print("HEAT MAP:")
    print(cm_34)

########################################################
    print("DATA 35:")
    xTrainFile_35 = "C:/Users/Claire Burkhardt/CS_334/iot_malware_detection/preprocessing/35_500Kre_xTrain.csv"
    yTrainFile_35 = "C:/Users/Claire Burkhardt/CS_334/iot_malware_detection/preprocessing/35_500Kre_yTrain.csv"

    columns_35 = ['id.resp_p','id.orig_p','id.resp_h','duration']

    xData_35 = file_to_numpy_select_cols(xTrainFile_35,columns_35)
    yData_35 = file_to_numpy(yTrainFile_35)

    DTModel_35, accTrain_35, cm_35 = trainModel(xData_35,yData_35)
    print("TEST ACCURACY: ", accTrain_35)
    print("HEAT MAP:")
    print(cm_35)

######################################################################

    print("DATA 48:")
    xTrainFile_48 = "C:/Users/Claire Burkhardt/CS_334/iot_malware_detection/preprocessing/48_500Kre_xTrain.csv"
    yTrainFile_48 = "C:/Users/Claire Burkhardt/CS_334/iot_malware_detection/preprocessing/48_500Kre_yTrain.csv"

    columns_48 = ['orig_bytes','id.orig_h','id.orig_p','id.resp_p','history_D','conn_state_SH']

    xData_48 = file_to_numpy_select_cols(xTrainFile_48,columns_48)
    yData_48 = file_to_numpy(yTrainFile_48)

    DTModel_48, accTrain_48, cm_48 = trainModel(xData_48,yData_48)
    print("TEST ACCURACY: ", accTrain_48)
    print("HEAT MAP:")
    print(cm_48)

######################################################################
          

    #if model 34 predicts benign
    # stick it in a new data array
    # relabel with model 48
  
#train 34 on model 43
    print("\nTRAINING DATA 34 ON MODEL 43")
    xData_34_on_43 = file_to_numpy_select_cols(xTrainFile_34,columns_43)
    yHat_train_34_43 = DTModel_43.predict(xData_34_on_43)
    acc_train_34_43 = acc_score(yHat_train_34_43,yData_34[:,0])
    print("ACCURACY OF DATA 34 on nb_model_43:", acc_train_34_43)
    print("CONFUSION MATRIX:")
    print(confusion_matrix(yData_34[:,0], yHat_train_34_43))
######################################################################

#train 43 on model 34
    print("\nTRAINING DATA 43 ON MODEL 34")
    xData_43_on_34 = file_to_numpy_select_cols(xTrainFile_43,columns_34)
    yHat_train_43_34 = DTModel_34.predict(xData_43_on_34)
    acc_train_43_34 = acc_score(yHat_train_43_34,yData_43[:,0])
    print("ACCURACY OF DATA 43 on nb_model_34:", acc_train_43_34)
    print("CONFUSION MATRIX:")
    print(confusion_matrix(yData_43[:,0], yHat_train_43_34))
    ######################################################################

    model_number = [34, 35, 43, 48]
    models = [DTModel_34, DTModel_35, DTModel_43, DTModel_48]
    columns = [columns_34, columns_35, columns_43, columns_48]
    xTrainFile = [xTrainFile_34, xTrainFile_35, xTrainFile_43, xTrainFile_48]
    yData = [yData_34, yData_35, yData_43, yData_48]
    """
    for j in range(4): 
        print("*** ACCURACY OF MODEL ", model_number[j], " ***")
        for i in range(4):
            xData_1_on_2 = file_to_numpy_select_cols(xTrainFile[i],columns[j])
            yHat_train_1_2 = models[j].predict(xData_1_on_2)
            acc_train_1_2 = acc_score(yHat_train_1_2, yData[i][:,0])
            print("ACCURACY OF DATA ", model_number[i], ": ", acc_train_1_2)
            print("CONFUSION MATRIX:")
            print(confusion_matrix(yData[i][:,0].astype(int), yHat_train_1_2))
    """
    print("STARTING STACKING\n\n")
    def stacked_34_48_models(xDataFile,yDataFile,DTModel_34,DTModel_48):

        columns_34 = ['missed_bytes','resp_ip_bytes','resp_bytes','service_http', 'history_ShAdDaf', 'conn_state_S3','service_irc','id.resp_p','history_S','conn_state_S0','service_dns', 'history_C', 'conn_state_OTH', 'history_Dd', 'conn_state_SF', 'id.resp_h','history_D','id.orig_p', 'proto_tcp','proto_udp']
        xData = pd.read_csv(xDataFile)
        xData_34 = xData
        # not working below
      #  pdb.set_trace()
        df_columns = sorted(xData) # get column names of xData
        missing_cols = list(set(columns_34) - set(df_columns)) # get column names of columns 34 not in xData

        # add dummy row to every missing column
        for col in missing_cols:
            xData_34[col] = 0

        # select on the relevant columns (in the right order!) from df
        xData_34 = xData_34[columns_34]

        columns_48 = ['orig_bytes','id.orig_h','id.orig_p','id.resp_p','history_D','conn_state_SH']
        
        yData = file_to_numpy(yDataFile)

        yHat_orig = DTModel_34.predict(xData_34)

        index_arr =[]
        j = 0
        for i in range(len(yHat_orig)):
            if yHat_orig[i] == 0:
                index_arr.append(i)
        # edited updated_array to have model 48's columns
        # pick the rows in xData in our index array
        benign_label_rows = xData.iloc[index_arr]

        ## copy from above to put in buffer rows
        df_columns_again = sorted(benign_label_rows) # get column names of xData
        missing_cols_again = list(set(columns_48) - set(df_columns_again)) # get column names of columns 34 not in xData
        ##
        for col in missing_cols_again:
            benign_label_rows[col] = 0

        # select on the relevant columns (in the right order!) from df
        ben_label_48_cols = benign_label_rows[columns_48]
        

        yHat_small_48 = DTModel_48.predict(ben_label_48_cols)
        
        k = 0
        for index in index_arr:
            yHat_orig[index] = yHat_small_48[k]
            k+=1
        # pdb.set_trace()        
        acc = acc_score(yHat_orig,yData[:,0])
        cm = confusion_matrix(yData[:,0].astype(int),yHat_orig.astype(int))
        return cm

    accuracy_stacked = stacked_34_48_models(xTrainFile_35,yTrainFile_35,DTModel_34,DTModel_48)
    print("ACC on 35: ", accuracy_stacked) # .2018 ## mostly false negatives

    accuracy_stacked = stacked_34_48_models(xTrainFile_34,yTrainFile_34,DTModel_34,DTModel_48)
    print("ACC on 34: ", accuracy_stacked) ## .9875

    accuracy_stacked = stacked_34_48_models(xTrainFile_48,yTrainFile_48,DTModel_34,DTModel_48)
    print("ACC on 48: ", accuracy_stacked) ## .9993

    accuracy_stacked = stacked_34_48_models(xTrainFile_43,yTrainFile_43,DTModel_34,DTModel_48)
    print("ACC on 43: ", accuracy_stacked)  ## .6520 ## mostly false negatives
    



if __name__ == "__main__":
    main()



    



if __name__ == "__main__":
    main()