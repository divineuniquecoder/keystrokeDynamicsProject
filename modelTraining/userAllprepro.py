
import pandas as pd
import numpy as np
import ast
from sklearn.preprocessing import StandardScaler
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.impute import SimpleImputer
import re

# Load the dataset
data_path = 'user_test11trueusers_Alltasks.csv'  # Update this path #do this to each files separate
df = pd.read_csv(data_path)

# Custom transformer for list-type features
class ListStatsTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, stat_funcs):
        self.stat_funcs = stat_funcs

    def fit(self, X, y=None):
        return self

    def transform(self, X, task_type, applicable_task_types):
        result = []
        for item, task in zip(X, task_type):
            if task in applicable_task_types:
                try:
                    # Improved handling for NaN values in list columns
                    if pd.isna(item):
                        raise ValueError("Missing list data")
                    lst = ast.literal_eval(item) if isinstance(item, str) else item
                    stats = [func(lst) for func in self.stat_funcs]
                except (ValueError, SyntaxError) as e:
                    stats = [np.nan for func in self.stat_funcs]
            else:
                stats = [np.nan for _ in self.stat_funcs]
            result.append(stats)
        return np.array(result)

# Function to sum values in dictionary-type columns
def sum_dict_values(dict_str):
    try:
        if pd.isna(dict_str):
            raise ValueError("Missing dictionary data")
        dictionary = ast.literal_eval(dict_str) if isinstance(dict_str, str) else dict_str
        return sum(dictionary.values())
    except (ValueError, SyntaxError):
        return np.nan
    
# Function to filter and encode bigrams
def encode_bigrams(bigram_freq):
    filtered_bigrams = {k: v for k, v in bigram_freq.items() if re.fullmatch(r'[a-z]{2}', k)}
    encoded_bigrams = {k: (ord(k[0]) - ord('a') + 1) * 100 + (ord(k[1]) - ord('a') + 1) for k in filtered_bigrams.keys()}
    weighted_encoded_bigrams = {encoded_bigrams[k]: v for k, v in filtered_bigrams.items()}
    return sum(k * v for k, v in weighted_encoded_bigrams.items())

# Function to encode punctuation marks
def encode_punctuation(punctuation_count):
    if pd.isna(punctuation_count):
        return np.nan
    punctuation_mapping = {
    '!': 0.1, '"': 0.2, '#': 0.3, '$': 0.4, '%': 0.5,
    '&': 0.6, '\'': 0.7, '(': 0.8, ')': 0.9, '*': 1.0,
    '+': 1.1, ',': 1.2, '-': 1.3, '.': 1.4, '/': 1.5,
    ':': 1.6, ';': 1.7, '<': 1.8, '=': 1.9, '>': 2.0,
    '?': 2.1, '@': 2.2, '[': 2.3, '\\': 2.4, ']': 2.5,
    '^': 2.6, '_': 2.7, '`': 2.8, '{': 2.9, '|': 3.0,
    '}': 3.1, '~': 3.2}
    try:
        # Convert string representation of a dictionary to an actual dictionary
        punctuation_count_dict = ast.literal_eval(punctuation_count) if isinstance(punctuation_count, str) else punctuation_count
        encoded_punctuation = {punctuation_mapping.get(k, 0): v for k, v in punctuation_count_dict.items()}
        return sum(k * v for k, v in encoded_punctuation.items())
    except (ValueError, SyntaxError):
        return np.nan

# Encoding the bigrams and punctuation counts in the DataFrame
df['bigram_freq'] = df['bigram_freq'].apply(lambda x: encode_bigrams(ast.literal_eval(x) if isinstance(x, str) else x))
df['punctuation_count'] = df['punctuation_count'].apply(lambda x: encode_punctuation(x) if isinstance(x, str) or not pd.isna(x) else x)


# Apply transformations
stat_funcs = [np.mean, np.std, np.median]
flight_time_transformer = ListStatsTransformer(stat_funcs)
dwell_time_transformer = ListStatsTransformer(stat_funcs)
inter_key_latency_transformer = ListStatsTransformer(stat_funcs)

# Only transform flight times and dwell times for 'Custom Text'
flight_times_transformed = flight_time_transformer.transform(df['flight_times'].values, df['task_type'].values, ['Custom Text'])
dwell_times_transformed = dwell_time_transformer.transform(df['dwell_times'].values, df['task_type'].values, ['Custom Text'])
inter_key_latencies_transformed = inter_key_latency_transformer.transform(df['inter_key_latencies'].values, df['task_type'].values, ['Custom Text', 'Fixed Text', 'Free Typing'])


# Integrate transformations into the original DataFrame
df['flight_time_mean'], df['flight_time_std'], df['flight_time_median'] = flight_times_transformed.T
df['dwell_time_mean'], df['dwell_time_std'], df['dwell_time_median'] = dwell_times_transformed.T
df['inter_key_latency_mean'], df['inter_key_latency_std'], df['inter_key_latency_median'] = inter_key_latencies_transformed.T


# Impute missing numerical features before normalization
numerical_columns = df.select_dtypes(include=['float64', 'int64']).columns
imputer = SimpleImputer(strategy='mean')
df[numerical_columns] = imputer.fit_transform(df[numerical_columns])



# Specify columns to scale
columns_to_scale = ['cpm', 'wpm', 'error_rate', 'rhythm_variability']
scaler = StandardScaler()

# Apply scaling only to the specified columns
df[columns_to_scale] = scaler.fit_transform(df[columns_to_scale])

# One-hot encode 'task_type' variable
df = pd.get_dummies(df, columns=['task_type'])

'''



# Impute missing numerical features before normalization
numerical_columns = df.select_dtypes(include=['float64', 'int64']).columns
imputer = SimpleImputer(strategy='mean')

# Perform imputation on all numerical features
df[numerical_columns] = imputer.fit_transform(df[numerical_columns])

# Apply scaling only to the specified columns
df[columns_to_scale] = scaler.fit_transform(df[columns_to_scale])

# Continue with the rest of your pipeline...



# Convert boolean columns to integer type
df['task_type_Custom Text'] = df['task_type_Custom Text'].astype(int)
df['task_type_Fixed Text'] = df['task_type_Fixed Text'].astype(int)
df['task_type_Free Typing'] = df['task_type_Free Typing'].astype(int)
'''
# Convert boolean columns to integer type
df['task_type_Custom Text'] = df['task_type_Custom Text'].astype(int)
df['task_type_Fixed Text'] = df['task_type_Fixed Text'].astype(int)
df['task_type_Free Typing'] = df['task_type_Free Typing'].astype(int)


# Convert 'user_id' to integers and make it the last column
df['user_id'] = df['user_id'].str.extract('(\d+)').astype(int)
user_id = df.pop('user_id')  # Remove and store the column
df['user_id'] = user_id  # Add 'user_id' back as the last column

# Drop original columns that have been transformed or are no longer needed
df.drop(['flight_times', 'inter_key_latencies', 'bigram_freq', 'punctuation_count', 'dwell_times', 'session_id'], axis=1, inplace=True)
#Drop original columns that have been transformed or are no longer needed
#columns_to_drop = ['flight_times', 'inter_key_latencies', 'dwell_times', 'session_id', 'shift_key_usage', 'task_type_Custom Text', 'task_type_Fixed Text']
# Remove 'task_type' and 'punctuation_count' if they exist
#columns_to_drop = [col for col in columns_to_drop if col in df.columns]
#df.drop(columns_to_drop, axis=1, inplace=True)


# Save the preprocessed DataFrame to a CSV file
preprocessed_file_path = 'user_test11trueusers_AlltasksPRO.csv'  # Update this path
df.to_csv(preprocessed_file_path, index=False)

print(f"Preprocessed data saved to {preprocessed_file_path}")
