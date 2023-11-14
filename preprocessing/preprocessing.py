import csv
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder


def extract_data(file_path, delimiter='\t'):
    data = []  # Create a list to store the data

    # Open the CSV file for reading
    with open(file_path, mode='r', newline='') as file:
        # Create a CSV reader object with the tab delimiter
        csv_reader = csv.reader(file, delimiter=delimiter)
        # Read the header row
        header = next(csv_reader)
        # Iterate through the rows in the CSV file
        for row in csv_reader:
            data.append(row)

    return data

data = extract_data()

data = np.array(data)

# Read the dataset, store it as a dataframe or numpy array?
# Numpy would be better for faster removal of columns we don't need using slicing --> Yujin read it as a df,
# also what is the last column thing about?? TODO

#This is just for my sanity check
column_types = { #not sure about the timestamp data type
    'ts': float,
    'uid': str,
    'id.orig_h': str,
    'id.orig_p': str,
    'id.resp_h': str,
    'id.resp_p': int,
    'proto': str,
    'service': str,
    'duration': str,
    'orig_bytes': int,
    'resp_bytes': int,
    'conn_state': str,
    'local_orig': bool,
    'local_resp': bool,
    'missed_bytes': int,
    'history': int,
    'orig_pkts': int,
    'orig_ip_bytes': int,
    'resp_pkts': int,
    'resp_ip_bytes': int,
    'tunnel_parents': str,
    'label': str,
    'detailed-label': str
}

# One row looks like this
row_example = ['1568940058.775322' 'CEjjLs1iwWYrt8C4O6' '192.168.1.195' '123' '212.111.30.190' '123' 'udp' '-' '0.008239' 
 '96' '96' 'SF' '-' '-' '0' 'Dd' '2' '152' '2' '152' '-' 'Benign' '-']

# Data Processing begins here

# What columns in Capt 43 will be absolutely unnecessary for training our model? Remove those
remove_columns = [0, 1, 2, 4, 12, 13, 14, 20] #add more or remove as necessary

# Use a correlation matrix

# Are the IP addresses important or do we remove them? TODO I removed them

# Remove columns
data = np.delete(dataset, remove_columns, axis=1)
# down to 15 cols

# Encode the label column Malicious/ Benign as 1 , 0 **hold on, our  data doesn't have label values??!! NVM, found the labeled one
# Ensure we have correctly read the dataset and is stored in the right variable name
for row in dataset:
    if row[-2] == 'Benign':
        row[-2] = 0
    else:
        row[-2] = 1

#We need to find a way to account for so much missing data in some of the cols








df = pd.read_csv(dataset) #save it as a pandas dataframe

# Check for missing values
print(df.isnull().sum())

# Accounting for null values:
# Option 1: Drop rows with missing values
df = df.dropna()

# Option 2: Impute missing values using average values
df.fillna(df.mean(), inplace=True)

# Is there categorical data, should encode them
'''
label_encoder = LabelEncoder()
for column in categorical_columns:
    df[column] = label_encoder.fit_transform(df[column])
    
    
    
# Are we splitting the dataset in this script?
'''
def main():
    # read the dataset, split into x(features), y (label or TYPE!!) both train and test
    #

if __name__ == "__main__":
    main()
