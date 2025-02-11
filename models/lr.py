import csv
import argparse
import numpy as np
import pandas as pd
import random
from sklearn.model_selection import cross_validate, cross_val_score, train_test_split
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix, roc_auc_score
from sklearn.linear_model import LogisticRegression
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


def auc_score(yHat, yActual):
    return roc_auc_score(yActual, yHat)


def trainModel(xData, yData, filename):
    xTrain, xTest, yTrain, yTest = train_test_split(xData, yData, test_size=0.3, shuffle=True)

    scaler = StandardScaler()
    xTrain_scaled = scaler.fit_transform(xTrain)
    xTest_scaled = scaler.transform(xTest)

    lr = LogisticRegression(solver='saga', max_iter=6000, tol=1e-4)
    lr.fit(xTrain_scaled, yTrain[:, 0].astype(int))

    yHat_train = lr.predict_proba(xTrain_scaled)[:, 1]  # Predict probabilities for AUC calculation
    auc_train = roc_auc_score(yTrain[:, 0].astype(int), yHat_train)
    print("TRAIN AUC: ", auc_train)

    yHat_test = lr.predict_proba(xTest_scaled)[:, 1]  # Predict probabilities for AUC calculation
    auc_test = roc_auc_score(yTest[:, 0].astype(int), yHat_test)
    print("TEST AUC: ", auc_test)

    # Save the yHat data as a csv file (if needed)
    with open(filename, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['yHat'])  # Write header if needed
        csv_writer.writerows(zip(yHat_test))  # Write yHat data row-wise to the CSV file

    return lr, auc_train, auc_test


def main():
    print("LOGISTIC REGRESSION")
    ########################################################
    print("DATA 43")
    xTrainFile_43 = "C:/Users/Beauttah/Python Programs/MLProject/43re_xTrain.csv"
    yTrainFile_43 = "C:/Users/Beauttah/Python Programs/MLProject/43re_yTrain.csv"

    columns_43 = ['id.resp_p']

    xData_43 = file_to_numpy_select_cols(xTrainFile_43, columns_43)
    yData_43 = file_to_numpy(yTrainFile_43)

    lrModel_43, aucTrain_43, aucTest_43 = trainModel(xData_43, yData_43, 'yHat43_LR.csv')
    print("TRAIN AUC: ", aucTrain_43)

    ########################################################

    print("DATA 34:")
    xTrainFile_34 = "C:/Users/Beauttah/Python Programs/MLProject/34re_xTrain.csv"
    yTrainFile_34 = "C:/Users/Beauttah/Python Programs/MLProject/34re_yTrain.csv"

    columns_34 = ['missed_bytes', 'resp_ip_bytes', 'resp_bytes', 'service_http', 'history_ShAdDaf', 'conn_state_S3',
                  'service_irc', 'id.resp_p', 'history_S', 'conn_state_S0', 'service_dns', 'history_C',
                  'conn_state_OTH', 'history_Dd', 'conn_state_SF', 'id.resp_h', 'history_D', 'id.orig_p', 'proto_tcp',
                  'proto_udp']

    xData_34 = file_to_numpy_select_cols(xTrainFile_34, columns_34)
    yData_34 = file_to_numpy(yTrainFile_34)

    lrModel_34, aucTrain_34, aucTest_34 = trainModel(xData_34, yData_34, 'yHat34_LR.csv')
    print("TRAIN AUC: ", aucTrain_34)

    ######################################################################
    print("DATA 35:")
    xTrainFile_35 = "C:/Users/Beauttah/Python Programs/MLProject/35_500Kre_xTrain.csv"
    yTrainFile_35 = "C:/Users/Beauttah/Python Programs/MLProject/35_500Kre_yTrain.csv"

    columns_35 = ['id.resp_p', 'id.orig_p', 'id.resp_h', 'duration']

    xData_35 = file_to_numpy_select_cols(xTrainFile_35, columns_35)
    yData_35 = file_to_numpy(yTrainFile_35)

    lrModel_35, aucTrain_35, aucTest_43 = trainModel(xData_35, yData_35, 'yHat35_LR.csv')
    print("TRAIN AUC: ", aucTrain_35)

    ######################################################################

    print("DATA 48:")
    xTrainFile_48 = "C:/Users/Beauttah/Python Programs/MLProject/48_500Kre_xTrain.csv"
    yTrainFile_48 = "C:/Users/Beauttah/Python Programs/MLProject/48_500Kre_yTrain.csv"

    columns_48 = ['orig_bytes', 'id.orig_h', 'id.orig_p', 'id.resp_p', 'history_D', 'conn_state_SH']

    xData_48 = file_to_numpy_select_cols(xTrainFile_48, columns_48)
    yData_48 = file_to_numpy(yTrainFile_48)
    yData_48 = np.delete(yData_48, 1, axis=1)
    yData_48 = yData_48.astype(int)
    print("Shape of the array:", yData_48.shape)

    lrModel_48, aucTrain_48, aucTest_43 = trainModel(xData_48, yData_48, 'yHat48_LR.csv')
    print("TRAIN AUC: ", aucTrain_48)

    ########################################################

    # train 34,35,48 on model 43
    print("\nTRAINING DATA 34 ON MODEL 43")
    xData_34_on_43 = file_to_numpy_select_cols(xTrainFile_34, columns_43)
    yHat_train_34_43 = lrModel_43.predict(xData_34_on_43)
    auc_train_34_43 = auc_score(yHat_train_34_43, yData_34[:, 0])
    print("AUC SCORE OF DATA 34 on lrModel_43", auc_train_34_43)

    print("\nTRAINING DATA 35 ON MODEL 43")
    xData_35_on_43 = file_to_numpy_select_cols(xTrainFile_35, columns_43)
    yHat_train_35_43 = lrModel_43.predict(xData_35_on_43)
    auc_train_35_43 = auc_score(yHat_train_35_43, yData_35[:, 0])
    print("AUC SCORE OF DATA 35 on lrModel_43", auc_train_35_43)

    print("\nTRAINING DATA 48 ON MODEL 43")
    xData_48_on_43 = file_to_numpy_select_cols(xTrainFile_48, columns_43)
    yHat_train_48_43 = lrModel_43.predict(xData_48_on_43)
    yHat_train_48_43 = yHat_train_48_43.astype(int)
    auc_train_48_43 = auc_score(yHat_train_48_43, yData_48[:, 0])

    print("AUC SCORE OF DATA 48 on lrModel_43", auc_train_48_43)

    ######################################################################

    # train 43,35,48 on model 34
    print("\nTRAINING DATA 43 ON MODEL 34")
    xData_43_on_34 = file_to_numpy_select_cols(xTrainFile_43, columns_34)
    yHat_train_43_34 = lrModel_34.predict(xData_43_on_34)
    auc_train_43_34 = auc_score(yHat_train_43_34, yData_43[:, 0])
    print("AUC SCORE OF DATA 43 on lrModel_34:", auc_train_43_34)

    print("\nTRAINING DATA 35 ON MODEL 34")
    xData_35_on_34 = file_to_numpy_select_cols(xTrainFile_35, columns_34)
    yHat_train_35_34 = lrModel_34.predict(xData_35_on_34)
    auc_train_35_34 = auc_score(yHat_train_35_34, yData_35[:, 0])
    print("AUC SCORE OF DATA 35 on lrModel_34:", auc_train_35_34)


    print("\nTRAINING DATA 48 ON MODEL 34")
    xData_48_on_34 = file_to_numpy_select_cols(xTrainFile_48, columns_34)
    yHat_train_48_34 = lrModel_34.predict(xData_48_on_34)
    yHat_train_48_34 = yHat_train_48_34.astype(int)
    auc_train_48_34 = auc_score(yHat_train_48_34, yData_48[:, 0])
    print("AUC SCORE OF DATA 48 on lrModel_34:", auc_train_48_34)


    ######################################################################

    # train 43,34,48 on model 35
    print("\nTRAINING DATA 43 ON MODEL 35")
    xData_43_on_35 = file_to_numpy_select_cols(xTrainFile_43, columns_35)
    yHat_train_43_35 = lrModel_35.predict(xData_43_on_35)
    auc_train_43_35 = auc_score(yHat_train_43_35, yData_43[:, 0])
    print("AUC SCORE OF DATA 43 on lrModel_35:", auc_train_43_35)

    print("\nTRAINING DATA 34 ON MODEL 35")
    xData_34_on_35 = file_to_numpy_select_cols(xTrainFile_34, columns_35)
    yHat_train_34_35 = lrModel_35.predict(xData_34_on_35)
    auc_train_34_35 = auc_score(yHat_train_34_35, yData_34[:, 0])
    print("AUC SCORE OF DATA 34 on lrModel_35:", auc_train_34_35)

    print("\nTRAINING DATA 48 ON MODEL 35")
    xData_48_on_35 = file_to_numpy_select_cols(xTrainFile_48, columns_35)
    yHat_train_48_35 = lrModel_35.predict(xData_48_on_35)
    yHat_train_48_35 = yHat_train_48_35.astype(int)
    auc_train_48_35 = auc_score(yHat_train_48_35, yData_48[:, 0])
    print("AUC SCORE OF DATA 48 on lrModel_35:", auc_train_48_35)

    ######################################################################

    # train 43,34,35 on model 48
    print("\nTRAINING DATA 43 ON MODEL 48")
    xData_43_on_48 = file_to_numpy_select_cols(xTrainFile_43, columns_48)
    yHat_train_43_48 = lrModel_48.predict(xData_43_on_48)
    auc_train_43_48 = auc_score(yHat_train_43_48, yData_43[:, 0])
    print("AUC SCORE OF DATA 43 on lrModel_48:", auc_train_43_48)

    print("\nTRAINING DATA 34 ON MODEL 48")
    xData_34_on_48 = file_to_numpy_select_cols(xTrainFile_34, columns_48)
    yHat_train_34_48 = lrModel_48.predict(xData_34_on_48)
    auc_train_34_48 = auc_score(yHat_train_34_48, yData_34[:, 0])
    print("AUC SCORE OF DATA 34 on lrModel_48:", auc_train_34_48)


    print("\nTRAINING DATA 35 ON MODEL 48")
    xData_35_on_48 = file_to_numpy_select_cols(xTrainFile_35, columns_48)
    yHat_train_35_48 = lrModel_48.predict(xData_35_on_48)
    auc_train_35_48 = auc_score(yHat_train_35_48, yData_35[:, 0])
    print("AUC SCORE OF DATA 35 on lrModel_48:", auc_train_35_48)

if __name__ == "__main__":
    main()

