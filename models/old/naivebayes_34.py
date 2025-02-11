import argparse
import numpy as np
import pandas as pd
import random
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import cross_validate, cross_val_score, train_test_split
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
import pdb

def file_to_numpy(filename):
    """
    Read an input file and convert it to numpy
    """
    df = pd.read_csv(filename)
    return df.to_numpy()


def acc_score(yHat,yActual):
    correct = 0
    for i in range(len(yHat)):
        if yHat[i] == yActual[i]:
            correct +=1
        else:
            print("WRONG: PREDICTED ", yHat[i], " ACTUAL: ", yActual[i] )
    acc = correct / len(yHat)
    return acc

def trainModel(xData, yData):
    xTrain, xTest, yTrain, yTest = train_test_split(xData,yData, test_size=0.3,shuffle=True) 

    gnb = GaussianNB()
    # pdb.set_trace()
    # we are hard coding a drop of columns 2,3,4 because they contain NaN
    
    # deleted any cols that were non-numerical or with strings
    xTrain_edited = np.delete(xTrain,[0,1,3,5,6,7,8,15],axis=1)
   # pdb.set_trace()
    gnb.fit(xTrain_edited,yTrain[:,0].astype('int'))

    xTest_edited = np.delete(xTest,[0,1,3,5,6,7,8,15],axis=1)    
    yHat = gnb.predict(xTest_edited)
    acc = acc_score(yHat,yTest[:,0])
    return gnb, acc

def main():
    capture_34_xTrain = "C:/Users/Claire Burkhardt/CS_334/iot_malware_detection/preprocessing/xTrain.csv"
    capture_34_yTrain = "C:/Users/Claire Burkhardt/CS_334/iot_malware_detection/preprocessing/yTrain.csv"
    
    xTrain = file_to_numpy(capture_34_xTrain)
    yTrain = file_to_numpy(capture_34_yTrain)

    gnbModel, accTrain = trainModel(xTrain,yTrain)
    print(accTrain)

if __name__ == "__main__":
    main()