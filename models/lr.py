import argparse
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import matplotlib.pyplot as plt


def trainModel(xData, yData):
    # 70-30 Split on train and test
    xTrain, xTest, yTrain, yTest = train_test_split(xData, yData, test_size=0.3, random_state=42)

    # Feature Scaling
    scaler = StandardScaler()
    xTrain = scaler.fit_transform(xTrain)
    xTest = scaler.transform(xTest)

    # Train our model on the input data
    model = LogisticRegression(max_iter=1000)
    model.fit(xTrain, yTrain)
    yPred = model.predict(xTest)

    accuracy = accuracy_score(yTest, yPred)
    confMatrix = confusion_matrix(yTest, yPred)
    print(accuracy)
    print(confMatrix)
    print("Classification Report:\n", classification_report(yTest, yPred))

    return accuracy


def main():
    # Getting data from terminal
    parser = argparse.ArgumentParser()
    parser.add_argument("xData",
                        help="filename for the training data")
    parser.add_argument("yData",
                        help="filename for the test data")

    args = parser.parse_args()

    xData = pd.read_csv(args.xData)
    yData = pd.read_csv(args.yData)

    # Drop the detailed-label column in the Y
    dropDetailed = ['detailed-label']
    yData = yData.drop(columns=dropDetailed)

    trainModel(xData, yData)

if __name__ == "__main__":
    main()
