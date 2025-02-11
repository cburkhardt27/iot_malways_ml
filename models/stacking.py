import pandas as pd
import numpy as np
from sklearn.model_selection import cross_validate, cross_val_score, train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
import pdb


def file_to_numpy(filename):
    """
    Read an input file and convert it to numpy
    """
    df = pd.read_csv(filename)
    return df.to_numpy()


def file_to_numpy_select_cols(filename, columnList):
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


def acc_score(yHat, yActual):
    correct = 0
    for i in range(len(yHat)):
        if yHat[i] == yActual[i]:
            correct += 1
    #    else:
    #         print("WRONG: PREDICTED ", yHat[i], " ACTUAL: ", yActual[i] )
    acc = correct / len(yHat)
    return acc


def stacking_models( xTrain, xTest, yTrain, yTest ):

    print("LR MODEL")
    lr = LogisticRegression(max_iter=1000, tol=1e-4)
    lr.fit(xTrain, yTrain[:, 0].astype(int))
    yHat_trainLR = lr.predict(xTrain)
    acc_trainLR = acc_score(yHat_trainLR, yTrain[:, 0].astype(int))
    print("LR TRAIN ACCURACY: ", acc_trainLR)

    yHat_LR = lr.predict(xTest)
    acc_LR = acc_score(yHat_LR, yTest[:, 0].astype(int))
    cm_LR = confusion_matrix(yTest[:, 0].astype(int), yHat_LR)
    print("LR TEST ACCURACY: ", acc_LR)

    print("NB MODEL")
    gnb = GaussianNB()
    gnb.fit(xTrain, yTrain[:, 0].astype(int))
    yHat_trainNB = gnb.predict(xTrain)
    acc_trainNB = acc_score(yHat_trainNB, yTrain[:, 0])
    print("NB TRAIN ACCURACY: ", acc_trainNB)

    yHat_NB = gnb.predict(xTest)
    acc_NB = acc_score(yHat_NB, yTest[:, 0].astype(int))
    cm_NB = confusion_matrix(yTest[:, 0].astype(int), yHat_NB)
    print("NB TEST ACCURACY: ", acc_NB)

    print("DT MODEL")
    clf = DecisionTreeClassifier(random_state=0)
    clf.fit(xTrain, yTrain[:, 0].astype(int))

    yHat_trainDT = clf.predict(xTrain)
    acc_trainDT = acc_score(yHat_trainDT, yTrain[:, 0].astype(int))
    print("DT TRAIN ACCURACY: ", acc_trainDT)

    yHat_NB = gnb.predict(xTest)
    acc_NB = acc_score(yHat_NB, yTest[:, 0].astype(int))
    cm_NB = confusion_matrix(yTest[:, 0].astype(int), yHat_NB)
    print("NB TEST ACCURACY: ", acc_NB)

    yHat_DT_test = clf.predict(xTest)
    yHat_LR_test = lr.predict(xTest)
    yHat_NB_test = gnb.predict(xTest)

    xMeta_train = np.hstack((yHat_trainLR.reshape(-1, 1), yHat_trainNB.reshape(-1, 1), yHat_trainDT.reshape(-1, 1)))
    xMeta_test = np.hstack((yHat_LR_test.reshape(-1, 1), yHat_NB_test.reshape(-1, 1), yHat_DT_test.reshape(-1, 1)))

    # LR META MODEL
    lrMeta = LogisticRegression(max_iter=1000, tol=1e-4)
    lrMeta.fit(xMeta_train, yTrain[:, 0].astype(int))  # train the model
    yHat_Meta = lrMeta.predict(xMeta_test)
    acc_testLR = acc_score(yHat_Meta, yTest[:, 0].astype(int))

    # Return the meta-model, accuracy, test data which is a
    # combination of the predicted values of the 3 models on test data
    return lrMeta, acc_testLR, xMeta_test


def main():
    # Read the data from capture 43
    xTrainFile_43 = "C:/Users/Beauttah/Python Programs/MLProject/43re_xTrain.csv"
    yTrainFile_43 = "C:/Users/Beauttah/Python Programs/MLProject/43re_yTrain.csv"

    columns_43 = ['id.resp_p']

    xData_43 = file_to_numpy_select_cols(xTrainFile_43, columns_43)
    yData_43 = file_to_numpy(yTrainFile_43)

    xTrain43, xTest43, yTrain43, yTest43 = train_test_split(xData_43, yData_43, test_size=0.3, shuffle=True)

    scaler = StandardScaler()
    xTrain43_scaled = scaler.fit_transform(xTrain43)
    xTest43_scaled = scaler.transform(xTest43)

    model43, accuracy43, xTest_meta43 = stacking_models(xTrain43_scaled, xTest43_scaled, yTrain43, yTest43)
    print("STACKED ACCURACY ON CAPTURE 43: ", accuracy43)


    # Read the data from capture 34
    xTrainFile_34 = "C:/Users/Beauttah/Python Programs/MLProject/34re_xTrain.csv"
    yTrainFile_34 = "C:/Users/Beauttah/Python Programs/MLProject/34re_yTrain.csv"

    columns_34 = ['missed_bytes', 'resp_ip_bytes', 'resp_bytes', 'service_http', 'history_ShAdDaf', 'conn_state_S3',
                  'service_irc', 'id.resp_p', 'history_S', 'conn_state_S0', 'service_dns', 'history_C',
                  'conn_state_OTH', 'history_Dd', 'conn_state_SF', 'id.resp_h', 'history_D', 'id.orig_p', 'proto_tcp',
                  'proto_udp']

    xData_34 = file_to_numpy_select_cols(xTrainFile_34, columns_34)
    yData_34 = file_to_numpy(yTrainFile_34)

    xTrain34, xTest34, yTrain34, yTest34 = train_test_split(xData_34, yData_34, test_size=0.3, shuffle=True)

    scaler = StandardScaler()
    xTrain_scaled34 = scaler.fit_transform(xTrain34)
    xTest_scaled34 = scaler.transform(xTest34)

    model34, accuracy34, xTest_meta34 = stacking_models(xTrain_scaled34, xTest_scaled34, yTrain34, yTest34)
    print("STACKED ACCURACY ON CAPTURE 34: ", accuracy34)


    # Read the data from capture 35
    xTrainFile_35 = "C:/Users/Beauttah/Python Programs/MLProject/35_500Kre_xTrain.csv"
    yTrainFile_35 = "C:/Users/Beauttah/Python Programs/MLProject/35_500Kre_yTrain.csv"

    columns_35 = ['id.resp_p', 'id.orig_p', 'id.resp_h', 'duration']

    xData_35 = file_to_numpy_select_cols(xTrainFile_35, columns_35)
    yData_35 = file_to_numpy(yTrainFile_35)

    xTrain35, xTest35, yTrain35, yTest35 = train_test_split(xData_35, yData_35, test_size=0.3, shuffle=True)

    scaler = StandardScaler()
    xTrain_scaled35 = scaler.fit_transform(xTrain35)
    xTest_scaled35 = scaler.transform(xTest35)

    model35, accuracy35, xTest_meta35 = stacking_models(xTrain_scaled35, xTest_scaled35, yTrain35, yTest35)
    print("STACKED ACCURACY ON CAPTURE 35: ", accuracy35)

    # Read data from capture 48
    print("DATA 48:")
    xTrainFile_48 = "C:/Users/Beauttah/Python Programs/MLProject/48_500Kre_xTrain.csv"
    yTrainFile_48 = "C:/Users/Beauttah/Python Programs/MLProject/48_500Kre_yTrain.csv"

    columns_48 = ['orig_bytes', 'id.orig_h', 'id.orig_p', 'id.resp_p', 'history_D', 'conn_state_SH']

    xData_48 = file_to_numpy_select_cols(xTrainFile_48, columns_48)
    yData_48 = file_to_numpy(yTrainFile_48)

    xTrain48, xTest48, yTrain48, yTest48 = train_test_split(xData_48, yData_48, test_size=0.3, shuffle=True)

    scaler = StandardScaler()
    xTrain_scaled48 = scaler.fit_transform(xTrain48)
    xTest_scaled48 = scaler.transform(xTest48)

    model48, accuracy48, xTest_meta48 = stacking_models(xTrain_scaled48, xTest_scaled48, yTrain48, yTest48)
    print("STACKED ACCURACY ON CAPTURE 48: ", accuracy35)

    print("CROSS CAPTURE TESTING META MODEL TRAINED ON MODEL PREDICTIONS FROM CAPTURE 43")
    print("STACKED ACCURACY ON CAPTURE 43: ", accuracy43)

    yHat_Meta43_34 = model43.predict(xTest_meta34)
    acc_testLR43_34 = acc_score(yHat_Meta43_34, yTest34[:, 0].astype(int))
    print("STACKED ACCURACY ON CAPTURE 34: ", acc_testLR43_34)

    yHat_Meta43_35 = model43.predict(xTest_meta35)
    acc_testLR43_35 = acc_score(yHat_Meta43_35, yTest35[:, 0].astype(int))
    print("STACKED ACCURACY ON CAPTURE 35: ", acc_testLR43_35)

    yHat_Meta43_48 = model43.predict(xTest_meta48)
    acc_testLR43_48 = acc_score(yHat_Meta43_48, yTest48[:, 0].astype(int))
    print("STACKED ACCURACY ON CAPTURE 48: ", acc_testLR43_48)

    print("CROSS CAPTURE TESTING META MODEL TRAINED ON MODEL PREDICTIONS FROM CAPTURE 34")
    print("STACKED ACCURACY ON CAPTURE 34: ", accuracy34)

    yHat_Meta34_43 = model34.predict(xTest_meta43)
    acc_testLR34_43 = acc_score(yHat_Meta34_43, yTest43[:, 0].astype(int))
    print("STACKED ACCURACY ON CAPTURE 43: ", acc_testLR34_43)

    yHat_Meta34_35 = model34.predict(xTest_meta35)
    acc_testLR34_35 = acc_score(yHat_Meta34_35, yTest35[:, 0].astype(int))
    print("STACKED ACCURACY ON CAPTURE 35: ", acc_testLR34_35)

    yHat_Meta34_48 = model34.predict(xTest_meta48)
    acc_testLR34_48 = acc_score(yHat_Meta34_48, yTest48[:, 0].astype(int))
    print("STACKED ACCURACY ON CAPTURE 48: ", acc_testLR34_48)

    print("CROSS CAPTURE TESTING META MODEL TRAINED ON MODEL PREDICTIONS FROM CAPTURE 35")
    print("STACKED ACCURACY ON CAPTURE 35: ", accuracy35)

    yHat_Meta35_43 = model35.predict(xTest_meta43)
    acc_testLR35_43 = acc_score(yHat_Meta35_43, yTest43[:, 0].astype(int))
    print("STACKED ACCURACY ON CAPTURE 43: ", acc_testLR35_43)

    yHat_Meta35_34 = model35.predict(xTest_meta34)
    acc_testLR35_34 = acc_score(yHat_Meta35_34, yTest34[:, 0].astype(int))
    print("STACKED ACCURACY ON CAPTURE 34: ", acc_testLR35_34)

    yHat_Meta35_48 = model35.predict(xTest_meta48)
    acc_testLR35_48 = acc_score(yHat_Meta35_48, yTest48[:, 0].astype(int))
    print("STACKED ACCURACY ON CAPTURE 48: ", acc_testLR35_48)

    print("CROSS CAPTURE TESTING META MODEL TRAINED ON MODEL PREDICTIONS FROM CAPTURE 48")
    print("STACKED ACCURACY ON CAPTURE 48: ", accuracy48)

    yHat_Meta48_43 = model48.predict(xTest_meta43)
    acc_testLR48_43 = acc_score(yHat_Meta48_43, yTest43[:, 0].astype(int))
    print("STACKED ACCURACY ON CAPTURE 43: ", acc_testLR48_43)

    yHat_Meta48_34 = model48.predict(xTest_meta34)
    acc_testLR48_34 = acc_score(yHat_Meta48_34, yTest34[:, 0].astype(int))
    print("STACKED ACCURACY ON CAPTURE 34: ", acc_testLR48_34)

    yHat_Meta48_35 = model48.predict(xTest_meta35)
    acc_testLR48_35 = acc_score(yHat_Meta48_35, yTest48[:, 0].astype(int))
    print("STACKED ACCURACY ON CAPTURE 35: ", acc_testLR48_35)

if __name__ == "__main__":
    main()
