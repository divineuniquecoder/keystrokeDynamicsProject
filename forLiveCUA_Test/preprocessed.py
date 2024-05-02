import pandas as pd
import numpy as np
import ast
from sklearn.preprocessing import StandardScaler
from sklearn.base import BaseEstimator, TransformerMixin

# Load the dataset
data_path = 'theOutput.csv'  # Update this path
df = pd.read_csv(data_path)

# Drop the 'shift_key_usage' column
df.drop('shift_key_usage', axis=1, inplace=True)
df.drop('session_id', axis=1, inplace=True)
df.drop('task_type', axis=1, inplace=True)
#df.drop(['task_type_Custom Text', 'task_type_Fixed Text', 'task_type_Free Typing'], axis=1, inplace=True)

# Custom transformer for list-type features
class ListStatsTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, stat_funcs):
        self.stat_funcs = stat_funcs

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        result = []
        for item in X:
            try:
                lst = ast.literal_eval(item) if isinstance(item, str) else []
                if not lst:
                    raise ValueError
                stats = [func(lst) for func in self.stat_funcs]
            except (ValueError, SyntaxError):
                stats = [np.nan for func in self.stat_funcs]
            result.append(stats)
        return np.array(result)

# Function to sum values in dictionary-type columns
def sum_dict_values(dict_str):
    try:
        dictionary = ast.literal_eval(dict_str) if isinstance(dict_str, str) else {}
        # Filter out keys containing 'shift'
        filtered_dictionary = {k: v for k, v in dictionary.items() if 'shift' not in k.lower()}
        return sum(filtered_dictionary.values())
    except ValueError:
        return np.nan

def calculate_structure_metrics(text):
    #paragraph_count = text.count('\n') + 1  # Assuming paragraphs are separated by newline characters
    sentence_delimiters = ['. ', '! ', '? ', '\n']  # Define end of sentence delimiters
    sentence_count = sum(text.count(delimiter) for delimiter in sentence_delimiters)
    return sentence_count, #paragraph_count

# Placeholder function for dwell time calculation
# You'll need to adjust this based on how your data for dwell time is structured
def calculate_dwell_times(dwell_times_str):
    dwell_times = ast.literal_eval(dwell_times_str) if isinstance(dwell_times_str, str) else []
    if dwell_times:
        return np.mean(dwell_times), np.std(dwell_times), np.median(dwell_times)
    else:
        return np.nan, np.nan, np.nan
    
if 'text' in df.columns:
    df[['sentence_count']] = df['text'].apply(lambda x: calculate_structure_metrics(x)).tolist()

# Assuming you have a way to calculate or approximate dwell times and have a 'dwell_times' column
if 'dwell_times' in df.columns:
    df[['dwell_time_mean', 'dwell_time_std', 'dwell_time_median']] = df['dwell_times'].apply(lambda x: calculate_dwell_times(x)).tolist()
# Apply transformations
stat_funcs = [np.mean, np.std, np.median]
flight_time_transformer = ListStatsTransformer(stat_funcs)
inter_key_latency_transformer = ListStatsTransformer(stat_funcs)


flight_times_transformed = flight_time_transformer.transform(df['flight_times'].values)
inter_key_latencies_transformed = inter_key_latency_transformer.transform(df['inter_key_latencies'].values)
bigram_freq_sum = df['bigram_freq'].apply(sum_dict_values)
#punctuation_count_sum = df['punctuation_count'].apply(sum_dict_values)

# Integrate transformations into the original DataFrame
df['flight_time_mean'], df['flight_time_std'], df['flight_time_median'] = flight_times_transformed.T
df['inter_key_latency_mean'], df['inter_key_latency_std'], df['inter_key_latency_median'] = inter_key_latencies_transformed.T
df['bigram_freq_sum'] = bigram_freq_sum
#df['punctuation_count_sum'] = punctuation_count_sum

# Drop original columns that have been transformed
df.drop(['flight_times', 'inter_key_latencies', 'bigram_freq', 'punctuation_count', 'dwell_times'], axis=1, inplace=True)

# Normalize numerical features
numerical_columns = df.select_dtypes(include=['float64', 'int64']).columns
df[numerical_columns] = StandardScaler().fit_transform(df[numerical_columns])

# One-hot encode 'task_type' variable
#df = pd.get_dummies(df, columns=['task_type'])

# Save the preprocessed DataFrame to a CSV file
preprocessed_file_path = 'postProcessed.csv'  # Update this path
df.to_csv(preprocessed_file_path, index=False)

print(f"Preprocessed data saved to {preprocessed_file_path}")
