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
    clf.fit(xTrain,yTrain[:,0])
    yHat_train = clf.predict(xTrain)
    acc_train = accuracy_score(yHat_train,yTrain[:,0])
    print("TRAIN ACCURACY: ", acc_train)

    yHat = clf.predict(xTest)
    acc = acc_score(yHat,yTest[:,0])
    cm = confusion_matrix(yHat,yTest[:,0])
  #  print("TRAIN CONFUSION MATRIX: ", cm)
    
    return clf, acc, cm

def main():
    print("DECISION TREE")
    print("DATA 43")
    xTrainFile_43 = "/Users/yujinkwon/Documents/CS334/Final_project/iot_malware_detection/preprocessing/43re_xTrain.csv"
    yTrainFile_43 = "/Users/yujinkwon/Documents/CS334/Final_project/iot_malware_detection/preprocessing/43re_yTrain.csv"

    columns_43 = ['id.resp_p']

    xData_43 = file_to_numpy_select_cols(xTrainFile_43,columns_43)
    yData_43 = file_to_numpy(yTrainFile_43)

    DTModel_43, accTrain_43, cm_43 = trainModel(xData_43,yData_43)
    print("TEST ACCURACY: ", accTrain_43)
    print("CONFUSION MATRIX :")
    print(cm_43)
    
########################################################
    print("DATA 34:")
    xTrainFile_34 = "/Users/yujinkwon/Documents/CS334/Final_project/iot_malware_detection/preprocessing/34re_xTrain.csv"
    yTrainFile_34 = "/Users/yujinkwon/Documents/CS334/Final_project/iot_malware_detection/preprocessing/34re_yTrain.csv"

    columns_34 = ['missed_bytes','resp_ip_bytes','resp_bytes','service_http', 'history_ShAdDaf', 'conn_state_S3','service_irc','id.resp_p','history_S','conn_state_S0','service_dns', 'history_C', 'conn_state_OTH', 'history_Dd', 'conn_state_SF', 'id.resp_h','history_D','id.orig_p', 'proto_tcp','proto_udp']

    xData_34 = file_to_numpy_select_cols(xTrainFile_34,columns_34)
    yData_34 = file_to_numpy(yTrainFile_34)

    DTModel_34, accTrain_34, cm_34 = trainModel(xData_34,yData_34)
    print("TEST ACCURACY: ", accTrain_34)
    print("HEAT MAP:")
    print(cm_34)

######################################################################

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
if __name__ == "__main__":
    main()



    



if __name__ == "__main__":
    main()