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
   # pdb.set_trace()

    #picking a stupid small column sample, only id.resp_p and proto.tcp and proto.udp
    xTrain_edited = xTrain[:,[1,15,16]]
    gnb.fit(xTrain_edited,yTrain[:,0])
    #picking a stupid small column sample, only id.resp_p and proto.tcp and proto.udp
  #  pdb.set_trace()
    xTest_edited = xTest[:,[1,15,16]] 
    yHat = gnb.predict(xTest_edited)
  #  pdb.set_trace()
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

    xTest_edited = xTest[:,[1,15,16]]
    yHat = gnbModel.predict(xTest_edited)
    acc = acc_score(yHat,yTest[:,0])
    print("ULTIMATE TEST ACC: ", acc)

# the only wrong answers we get are false positives --> good!

    capture_34_xTrain = "C:/Users/Claire Burkhardt/CS_334/iot_malware_detection/preprocessing/xTrain.csv"
    capture_34_yTrain = "C:/Users/Claire Burkhardt/CS_334/iot_malware_detection/preprocessing/yTrain.csv"
    
    xTrain_34 = file_to_numpy(capture_34_xTrain)
    yTrain_34 = file_to_numpy(capture_34_yTrain)
    #id.resp_p and proto.ucp and proto.tcp
    xTrain_34_edited = xTrain_34[:,[4,18,19]]
    yHat_34 = gnbModel.predict(xTrain_34_edited)
    acc_34 = acc_score(yHat_34,yTrain_34[:,0])
    print("34 TEST ACC: ", acc_34)

if __name__ == "__main__":
    main()