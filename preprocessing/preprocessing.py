import argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def read_data(filename):
    # Read the CSV file using Pandas
    data = pd.read_csv(filename, delimiter='\t', header=None).values
    data = np.array(data)
    return data


def encode_label(data):
    label_column = data[:, -2]

    # Encode 'Benign' as 0 and other values as 1 using boolean indexing
    label_column[label_column == 'Benign'] = 0
    label_column[label_column != 0] = 1

    # Print modified label column
    print("Modified label column:")
    print(label_column)

    # Update data array with the modified label column
    data[:, -2] = label_column.astype(np.float32)  # Convert to float if necessary

    return data

# Removes the timestamp column
def delete_timecol(data):
    return data[:, 1:]  # Retains columns starting from index 2 onwards

# Delete unnecessary features in our
def delete_feat(data):
    # TODO Fill in to delete unecessary features
    return data

#Uncomment after encoding all the data as numerical values
'''
def corr_matrix(data):
    # Calculate the correlation matrix using NumPy's corrcoef function
    correlation_matrix = np.corrcoef(data, rowvar=False)

    # Plotting the heatmap
    plt.figure(figsize=(12, 10))
    plt.imshow(correlation_matrix, cmap='coolwarm', interpolation='nearest')
    plt.colorbar()
    plt.title('Correlation Heatmap')
    plt.show()
'''
def main():
    """
    Main file to run from the command line.
    Take in arguments from the command line
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("trainData",
                        help="filename for the training data")
    parser.add_argument("testData",
                        help="filename for the test data")

    args = parser.parse_args()

    # Load the train and test data as numpy arrays using the helper function created above
    train = read_data(args.trainData)
    test = read_data(args.testData)

    print(np.shape(train))
    print(np.shape(test))
    print(train[15])
    print(train[200])
    '''
    print(train[0])
    print(train[1])
    print(train[2])
    print(train[200])
    '''
    new_train = encode_label(train)
    print("0-1 Benign Malicious Encoding")
    print(np.shape(new_train))
    print(new_train[15])
    print(new_train[200])

    train2 = delete_timecol(train)
    print("No time column?")
    print(np.shape(train2))
    print(train2[200])
    # corr_matrix(train)

if __name__ == "__main__":
    main()
