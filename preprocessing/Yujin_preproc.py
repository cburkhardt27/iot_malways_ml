import argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def encode_label(data, col):
    label_column = data[col]

    # Encode 'Benign' as 0 and other values as 1 using boolean indexing
    label_column[label_column == 'Benign'] = 0
    label_column[label_column != 0] = 1

    # Print modified label column
    print("Modified label column:")
    print(label_column)

    # Update data array with the modified label column
    data[col] = label_column.astype(np.int32)  # Convert to float if necessary

    return data

def encode_detailed_label(data, col):
    label_column = data[col]
    
    # Encode 'Benign' as 0 and other values as 1 using boolean indexing
    label_column[label_column == '-'] = 0
    label_column[label_column == 'PartOfAHorizontalPortScan'] = 1
    label_column[label_column == 'Benign'] = 2
    label_column[label_column == 'Benign'] = 3
    label_column[label_column == 'Benign'] = 4
    label_column[label_column == 'Benign'] = 5
    label_column[label_column == 'Benign'] = 6
    label_column[label_column == 'Benign'] = 7
    # Print modified label column
    print("Modified label column:")
    print(label_column)

    # Update data array with the modified label column
    data[col] = label_column.astype(np.int32)  # Convert to float if necessary

    return data

def encode_unique_vals(data, col):
    """
    input is 2d numpy array of data, col name
    returns unqiue vals in column
    """

    # Extract the specified column
    column_data = data[col]

    # Find unique values in the column
    unique_values = np.unique(column_data)

    # Create a mapping from unique values to encoded integers
    value_to_int_map = {value: index for index, value in enumerate(unique_values)}

    # Encode the entire column using the mapping
    encoded_column = np.vectorize(value_to_int_map.get)(column_data)  

    data[col] = encoded_column

    return data

def one_hot_encode_column(df, column_name):
    """
    One-hot encodes the unique values in the specified column of a DataFrame.
    df: The input DataFrame.
    column_name: The name of the column to be one-hot encoded.
    
    Returns: DataFrame with the specified column one-hot encoded.
    """
    # Extract the specified column
    column_data = df[column_name]
    
    # Use pd.get_dummies to one-hot encode the column
    one_hot_encoded = pd.get_dummies(column_data, prefix=column_name)
    
    # Concatenate the one-hot encoded columns with the original DataFrame
    df_encoded = pd.concat([df, one_hot_encoded], axis=1)
    
    # Drop the original column as it's no longer needed
    df_encoded = df_encoded.drop(column_name, axis=1)
    
    return df_encoded




def main():
    capture_43 = "/Users/yujinkwon/Documents/CS334/Final_project/train_data_500k 1.csv"

    # ** COLUMN LABELING **

    df43 = pd.read_table(capture_43, skiprows = 2, delimiter='\t', header =None) 
    df43.columns = [
        'ts',	
        'uid',
        'id.orig_h',
        'id.orig_p',
        'id.resp_h',
        'id.resp_p',
        'proto',
        'service',
        'duration',
        'orig_bytes',
        'resp_bytes',
        'conn_state',
        'local_orig',
        'local_resp',
        'missed_bytes',
        'history',
        'orig_pkts',
        'orig_ip_bytes',
        'resp_pkts',
        'resp_ip_bytes',
        'last_col'
    ]
    df43[['tunnel_parents', 'label', 'detailed-label']] = df43['last_col'].str.split(expand=True)
    df43.drop('last_col', axis=1, inplace=True)

    # 
    df43['ts'] = pd.to_datetime(df43['ts'], unit = 's')
    df43.replace('-', 'NULL', inplace=True)
    # Replace 'NULL' with NaN (a common representation for missing values)
    df43.replace('NULL', np.nan, inplace=True)


    # ** TYPE DEFINITIONS ** 
    

    # column_types = {
    #     'uid': str,
    #     'id.orig_h': str,
    #     'id.orig_p': str,
    #     'id.resp_h': str,
    #     'id.resp_p': int,
    #     'proto': str,
    #     'service': str,
    #     'duration': str,
    #     'orig_bytes': int,
    #     'resp_bytes': int,
    #     'conn_state': str,
    #     'local_orig': bool,
    #     'local_resp': bool,
    #     'missed_bytes': int,
    #     'history': int,
    #     'orig_pkts': int,
    #     'orig_ip_bytes': int,
    #     'resp_pkts': int,
    #     'resp_ip_bytes': int,
    #     'tunnel_parents': str,
    #     'label': str,
    #     'detailed-label': str
    # }

    df43['uid'] = df43['uid'].astype(str)
    df43['local_orig'] = df43['local_orig'].astype(bool)
    df43['local_resp'] = df43['local_resp'].astype(bool)
    df43['resp_ip_bytes'] = df43['resp_ip_bytes'].astype(int)
    df43['orig_ip_bytes'] = df43['orig_ip_bytes'].astype(int)

    df43_clean = df43.copy()

    # **ONE HOT ENCODING THE VARIABLES **

    mod_column = 'id.orig_h'
    print("id.orig_h")
    df43 = one_hot_encode_column(df43, 'id.orig_h')

    mod_column = 'proto'
    print(mod_column)
    df43 = one_hot_encode_column(df43, mod_column)

    mod_column = 'conn_state'
    print(mod_column)
    df43 = one_hot_encode_column(df43, mod_column)

    mod_column = 'local_orig'
    print(mod_column)
    df43 = one_hot_encode_column(df43, mod_column)

    mod_column = 'history'
    print(mod_column)
    df43 = one_hot_encode_column(df43, mod_column)

    mod_column = 'label'
    print(mod_column)
    df43 = encode_label(df43, mod_column)
    print(df43.columns)

    ## TESTING PRINTING FUNCTIONS

    print(df43.shape)
    print(df43.columns)
    print(df43['label'].unique())
    df43['label'].iloc[65]

    column = 'label'
    unique_values = df43[column].unique()
    print(f"Column '{column}' has {len(unique_values)} unique values:")
    print(unique_values)

    # # CREATING A NEW FILE FROM THE PANDADRAME

    # filename = "train500k_preproc.csv"
    # df43.to_csv(filename, sep=',', index=False, encoding='utf-8')

    # # split the data df43
    # yData = df43['label','detailed-label']
    # xData = df43.drop(['label','detailed-label'],axis=1)

    # xData.to_csv("xTrain.csv",index=False)
    # yData.to_csv("yTrain.csv",index=False,)





if __name__ == "__main__":
    main()
