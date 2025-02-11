import argparse
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pdb

'''
Combine the feature and target datasets so we can run correlations on both feature and target variables 
'''
def combine_data(featData, targetData):
    data = pd.concat([featData, targetData], axis=1)  # merge the data by adding targetData as columns
    return data

'''
Perform Pearson correlation: 
    (1)features with other features to check multicollinearity
    (2)features variables with the target variable
Create a generic function for (1) but will need to find specific coefficients for step (2) 
'''
def featCorr(xData):
    corrFeat = xData.corr()
    return corrFeat

def correlation(data):
    correlation_matrix = data.corr()
    return correlation_matrix

'''
Heatmap to display the correlations
'''
def heatMap(matrix):
    plt.figure(figsize=(24, 16))
    sns.heatmap(matrix, annot=True, cmap='coolwarm', fmt=".2f")
    plt.title('Correlation Matrix Heatmap')
    plt.show()

# Main method
def main():
    # Get the data at terminal

    parser = argparse.ArgumentParser()
    parser.add_argument("xData",
                        help="filename for the training data")
    parser.add_argument("yData",
                        help="filename for the test data")

    args = parser.parse_args()

    xDF = pd.read_csv(args.xData)
    yDF = pd.read_csv(args.yData)

    # drop detailed label
    yDF = yDF['label']
    print(yDF)

    # This 34 dataset has so many features gah!?!
    columns = ['id.orig_h', 'id.orig_p', 'id.resp_h', 'id.resp_p,duration',
               'orig_bytes', 'resp_bytes', 'local_orig', 'local_resp', 'missed_bytes,orig_pkts',
               'orig_ip_bytes', 'resp_pkts', 'resp_ip_bytes', 'proto_tcp', 'proto_udp', 'conn_state_OTH',
               'conn_state_RSTR', 'conn_state_S0', 'conn_state_S1', 'conn_state_S3', 'conn_state_SF',
               'history_C', 'history_CCC', 'history_CCCC', 'history_D', 'history_Dd', 'history_DdAtaFf',
               'history_S', 'history_ShAD', 'history_ShADacdtfF', 'history_ShADad', 'history_ShADadf',
               'history_ShADadtcfF', 'history_ShADadtctfF', 'history_ShADadtctfFR', 'history_ShADadttcfF',
               'history_ShADadttfF', 'history_ShAdD', 'history_ShAdDa', 'history_ShAdDaf', 'history_ShAdDaft',
               'history_ShAdDatf', 'history_ShAdDatfr', 'history_ShAdDfr', 'history_ShAdfDr', 'history_ShAfdtDr',
               'history_ShDadAf', 'service_dhcp', 'service_dns', 'service_http', 'service_irc']

    # Check for NaN values in each column
    columnsWithNan = xDF.columns[xDF.isnull().any()].tolist()
    # Check if there's any columns left with NaN values
    print("Columns with NaN values:", columnsWithNan)

    # Set display options to show all rows and columns
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)

    # Threshold for correlation coefficient to identify highly correlated features
    threshold = 0.8  # This can change

    xy = combine_data(xDF, yDF)
    print(xy.columns)
    corrMatrixFeat = correlation(xy)
    # heatMap(corrMatrixFeat)

    '''
    corrMatrixFeat = featCorr(xDF)
    heatMap(corrMatrixFeat)
    '''

    # Find pairs of highly correlated features
    correlatedFeatures = set()
    droppedFeatures = set()  # To keep track of already dropped features
    for i in range(len(corrMatrixFeat.columns)):
        for j in range(i):
            if abs(corrMatrixFeat.iloc[i, j]) > threshold:
                colname_i = corrMatrixFeat.columns[i]
                colname_j = corrMatrixFeat.columns[j]
                # Ensure only one of the pair is dropped
                if colname_i not in droppedFeatures:
                    correlatedFeatures.add(colname_i)
                    droppedFeatures.add(colname_j)
                elif colname_j not in droppedFeatures:
                    correlatedFeatures.add(colname_j)
                    droppedFeatures.add(colname_i)

    print("These are the correlated Features to be dropped: ")
    print(correlatedFeatures)

    # Drop one of the correlated features
    filteredFeatures = xy.drop(correlatedFeatures, axis=1)

    print("Filtered Features Columns")
    print(filteredFeatures.columns)

    print("All Data Columns")
    print(xy.columns)

    # Correlation with both variables and features
    allData = combine_data(filteredFeatures, yDF)
    corrMatrix = correlation(allData)
    label_row = corrMatrix['label'].abs()
    print("Most Predictive Features after dropping correlated features:")
    print(label_row.sort_values(ascending=False))
    # heatMap(corrMatrix)

if __name__ == "__main__":
    main()
