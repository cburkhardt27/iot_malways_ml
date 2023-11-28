import argparse
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

'''
Combine the feature and target datasets so we can run correlations on variables and target
Create a generic function to combine all the 3 types of data: train, HP, and OM
'''


def combine_data(featData, targetData):
    data = pd.concat([featData, targetData], axis=1)  # merge the data by adding targetData as columns
    return data


'''
Perform Pearson correlation on each of the 3 datasets: 
    (1)features variables with the target variable
    (2)features with other features to check multicollinearity
Create a generic function for (1) but will need to find specific coefficients for step (2) 
'''


def correlation(data):
    correlation_matrix = data.corr()
    return correlation_matrix


# Heatmap to display the correlations
def heatMap(matrix):
    plt.figure(figsize=(20, 12))
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

    '''
    #Test if we can read it
    print("Contents of the DataFrames:")
    print(xDF)
    print(yDF)
    '''

    combinedData = combine_data(xDF, yDF)
    # Testing lol
    '''
    print("Contents of the Merged DF:")
    print(combinedData)
    rows, columns = combinedData.shape
    print("Number of rows:", rows)
    print("Number of columns:", columns)
    '''
    '''
    # Save DataFrame as a CSV file in the same directory to prevent repeated  calls
    file_name = 'xyTrain.csv'
    combinedData.to_csv(file_name, index=False)
    '''

    corrMatrix = correlation(combinedData)
    # Set display options to show all rows and columns
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    print("This is the TRAIN Matrix")
    # print(corrMatrix)
    #  heatMap(corrMatrix)

    # Check for NaN values in each column
    columnsWithNan = xDF.columns[xDF.isnull().any()].tolist()

    print("Columns with NaN values:", columnsWithNan)  # 'duration', 'orig_bytes', 'resp_bytes'

    columnsToDrop = ['conn_state_OTH', 'conn_state_S0', 'conn_state_S1', 'conn_state_SF',
                     'id.orig_h_156.240.2.149', 'id.orig_h_185.44.94.22', 'id.orig_h_192.168.1.198',
                     'id.orig_h_91.16.171.210', 'id.orig_h_91.96.91.149', 'resp_pkts', 'resp_ip_bytes',
                     'orig_bytes', 'resp_bytes']

    xDF = xDF.drop(columns=columnsToDrop)

    # Replace missing values in 'duration' column with the median
    median_duration = xDF['duration'].median()
    xDF['duration'].fillna(median_duration, inplace=True)

    rows, columns = xDF.shape
    print("Number of rows:", rows)
    print("Number of columns:", columns)

    xDF.to_csv('cleanXTrain.csv', index=False)

    '''
    threshold = 0.4  # TODO reevaluate this value bro

    filtered_corrMatrix = corrMatrix[
        (corrMatrix.abs() > threshold) & (corrMatrix != 1.0)]
    print("This is the TRAIN WITH RELEVANT FEATURES Matrix")
    print(filtered_corrMatrix)
    # heatMap(filtered_corrMatrix)
    '''
    '''
    # Compute correlations between 'detailed-label' and other features
    corr = combinedData.corrwith(combinedData['label']).sort_values(ascending=False)
    print("HP data correlations")
    print(corr)

    # Filter features based on the threshold
    relevant_features = corr[abs(corr) >= threshold]

    # Display features correlated above the threshold with the target variable
    print("Features with correlation coefficients above", threshold, "with 'detailed-label':")
    print(relevant_features)
    '''
    '''
    Consider multicollinearity

    print(combinedData[['proto_udp', 'history_D']].corr()) #have 1.0 so one of them isn't relevant
    print(combinedData[['proto_udp', 'orig_ip_bytes']].corr()) # about 0.99
    print(combinedData[['proto_udp', 'orig_pkts']].corr())
    print(combinedData[['proto_udp', 'duration']].corr()) # Most unrelated 0.492
    print(combinedData[['proto_udp', 'proto_tcp']].corr())
    print(combinedData[['proto_udp', 'history_S']].corr())


    print(combinedData[['history_D', 'orig_ip_bytes']].corr()) #too high
    print(combinedData[['history_D', 'orig_pkts']].corr())
    print(combinedData[['history_D', 'duration']].corr())  # Most unrelated 0.492
    print(combinedData[['history_D', 'proto_tcp']].corr())
    print(combinedData[['history_D', 'history_S']].corr())

    print(combinedData[['orig_ip_bytes', 'history_S']].corr())  # too high
    print(combinedData[['orig_ip_bytes', 'orig_pkts']].corr())
    print(combinedData[['orig_ip_bytes', 'duration']].corr())  # Most unrelated 0.492
    print(combinedData[['orig_ip_bytes', 'proto_tcp']].corr())

    print(combinedData[['orig_pkts', 'duration']].corr())  # too high
    print(combinedData[['orig_pkts', 'proto_tcp']].corr())
    print(combinedData[['orig_pkts', 'history_S']].corr())  # Most unrelated 0.492

    print(combinedData[['duration', 'history_S']].corr())  # too high
    print(combinedData[['duration', 'proto_tcp']].corr())

    print(combinedData[['proto_tcp', 'history_S']].corr())
    '''


if __name__ == "__main__":
    main()
