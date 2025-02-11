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
    xTrain_edited = xTrain[:,[0,1,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25]]
    gnb.fit(xTrain_edited,yTrain[:,0])

    xTest_edited = xTest[:,[0,1,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25]]    
    yHat = gnb.predict(xTest_edited)
    acc = acc_score(yHat,yTest[:,0])
    return gnb, acc

def main():
    xTrainFile = "C:/Users/Claire Burkhardt/CS_334/too_big_data/data/split_data/xTrain.csv"
    yTrainFile = "C:/Users/Claire Burkhardt/CS_334/too_big_data/data/split_data/yTrain.csv"

    xData = file_to_numpy(xTrainFile)
    yData = file_to_numpy(yTrainFile)

    gnbModel, accTrain = trainModel(xData,yData)
    print("ACCURACY USING TRAIN DATA: ", accTrain)

    # test on the entirety of our test data ?? 
    # kinda redundant becuase accTrain is on the 30% test split we did in our train data
    xTestFile = "C:/Users/Claire Burkhardt/CS_334/too_big_data/data/split_data/xTrain.csv"
    yTestFile = "C:/Users/Claire Burkhardt/CS_334/too_big_data/data/split_data/yTrain.csv"

    xTest = file_to_numpy(xTestFile)
    yTest = file_to_numpy(yTestFile)

    xTest_edited = xTest[:,[0,1,5,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25]]    
    yHat = gnbModel.predict(xTest_edited)
    acc = acc_score(yHat,yTest[:,0])
    print("ULTIMATE TEST ACC: ", acc)

# the only wrong answers we get are false positives --> good!

if __name__ == "__main__":
    main()