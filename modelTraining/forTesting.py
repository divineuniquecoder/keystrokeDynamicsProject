import pandas as pd

# Load the CSV file
data = pd.read_csv('userALL.csv')

# Count the occurrences of '/'
slash_count = data['punctuation_count'].str.count('/').sum()

print(f"Total number of slashes in 'fixed_type' column: {slash_count}")
