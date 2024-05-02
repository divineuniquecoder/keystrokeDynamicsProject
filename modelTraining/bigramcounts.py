import pandas as pd
import ast  # This module helps convert strings to their actual data types

# Load the data
data = pd.read_csv('userALL.csv')

# Let's say you want to count how often the key 'a' appears with a non-zero value in the 'bigram_freq' column
# First, convert the string representation of a dictionary to an actual dictionary
data['bigram_freq'] = data['bigram_freq'].apply(ast.literal_eval)

# Now, count the occurrences
a_count = sum(1 for item in data['bigram_freq'] if item.get('a', 0) > 0)

print(f"Count of 'a' in 'bigram_freq' with non-zero values: {a_count}")
