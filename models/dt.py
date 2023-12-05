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
    clf.fit(xTrain,yTrain[:,0].astype(int))
    yHat_train = clf.predict(xTrain)
    acc_train = accuracy_score(yHat_train,yTrain[:,0].astype(int))
    print("TRAIN ACCURACY: ", acc_train)

    yHat = clf.predict(xTest)
    acc = acc_score(yHat,yTest[:,0].astype(int))
    cm = confusion_matrix(yHat,yTest[:,0].astype(int))
  #  print("TRAIN CONFUSION MATRIX: ", cm)
    
    return clf, acc, cm

def trainModel1(xData, yData):
    xTrain, xTest, yTrain, yTest = train_test_split(xData,yData, test_size=0.3,shuffle=True) 

    # Use GridSearchCV to find the best hyperparameters
    clf = DecisionTreeClassifier(random_state=0)
    param_grid = {
        'max_depth': [3, 5, 7],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 2, 4],
        'max_features': [None, 'sqrt', 'log2']
    }
    grid_search = GridSearchCV(clf, param_grid, cv=5)
    # Get the best hyperparameters
    grid_search.fit(xTrain, yTrain[:,0].astype(int))
    best_params = grid_search.best_params_

    clf = DecisionTreeClassifier(random_state=0, **best_params)
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
    xTrainFile_43 = "/Users/yujinkwon/Documents/CS334/Final_project/iot_malware_detection/preprocessing/43re_xTrain.csv"
    yTrainFile_43 = "/Users/yujinkwon/Documents/CS334/Final_project/iot_malware_detection/preprocessing/43re_yTrain.csv"

    columns_43 = ['id.resp_p']

    xData_43 = file_to_numpy_select_cols(xTrainFile_43,columns_43)
    yData_43 = file_to_numpy(yTrainFile_43)

    DTModel_43, accTrain_43, cm_43 = trainModel1(xData_43,yData_43)
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

    DTModel_34, accTrain_34, cm_34 = trainModel1(xData_34,yData_34)
    print("TEST ACCURACY: ", accTrain_34)
    print("HEAT MAP:")
    print(cm_34)

########################################################
    print("DATA 35:")
    xTrainFile_35 = "/Users/yujinkwon/Documents/CS334/Final_project/iot_malware_detection/preprocessing/35_500Kre_xTrain.csv"
    yTrainFile_35 = "/Users/yujinkwon/Documents/CS334/Final_project/iot_malware_detection/preprocessing/35_500Kre_yTrain.csv"

    columns_35 = ['id.resp_p','id.orig_p','id.resp_h','duration']

    xData_35 = file_to_numpy_select_cols(xTrainFile_35,columns_35)
    yData_35 = file_to_numpy(yTrainFile_35)

    DTModel_35, accTrain_35, cm_35 = trainModel1(xData_35,yData_35)
    print("TEST ACCURACY: ", accTrain_35)
    print("HEAT MAP:")
    print(cm_35)

######################################################################

    print("DATA 48:")
    xTrainFile_48 = "/Users/yujinkwon/Documents/CS334/Final_project/iot_malware_detection/preprocessing/48_500Kre_xTrain.csv"
    yTrainFile_48 = "/Users/yujinkwon/Documents/CS334/Final_project/iot_malware_detection/preprocessing/48_500Kre_yTrain.csv"

    columns_48 = ['orig_bytes','id.orig_h','id.orig_p','id.resp_p','history_D','conn_state_SH']

    xData_48 = file_to_numpy_select_cols(xTrainFile_48,columns_48)
    yData_48 = file_to_numpy(yTrainFile_48)

    DTModel_48, accTrain_48, cm_48 = trainModel1(xData_48,yData_48)
    print("TEST ACCURACY: ", accTrain_48)
    print("HEAT MAP:")
    print(cm_48)

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
    ######################################################################

    model_number = [34, 35, 43, 48]
    models = [DTModel_34, DTModel_35, DTModel_43, DTModel_48]
    columns = [columns_34, columns_35, columns_43, columns_48]
    xTrainFile = [xTrainFile_34, xTrainFile_35, xTrainFile_43, xTrainFile_48]
    yData = [yData_34, yData_35, yData_43, yData_48]

    for j in range(4): 
        print("*** ACCURACY OF MODEL ", model_number[j], " ***")
        for i in range(4):
            xData_1_on_2 = file_to_numpy_select_cols(xTrainFile[i],columns[j])
            yHat_train_1_2 = models[j].predict(xData_1_on_2)
            acc_train_1_2 = acc_score(yHat_train_1_2, yData[i][:,0])
            print("ACCURACY OF DATA ", model_number[i], ": ", acc_train_1_2)
            print("CONFUSION MATRIX:")
            print(confusion_matrix(yData[i][:,0].astype(int), yHat_train_1_2))




if __name__ == "__main__":
    main()