import pandas as pd
import ast
import numpy as np

# Load the data
data = pd.read_csv('userALL.csv')

# Convert stringified lists in 'flight_times' to actual lists
# repeat the process for the 'dwelling_times' column
data['flight_times'] = data['flight_times'].apply(lambda x: ast.literal_eval(x) if pd.notnull(x) else np.nan)

# Explode the 'flight_times' lists into rows
# repeat the process for the 'dwelling_times' column
data = data.explode('flight_times')

# Convert 'flight_times' to numeric
# repeat the process for the 'dwelling_times' column
data['flight_times'] = pd.to_numeric(data['flight_times'], errors='coerce')

# Group by 'user_id' and calculate the mean and standard deviation
# repeat the process for the 'dwelling_times' column
user_stats = data.groupby('user_id')['flight_times'].agg(['mean', 'std', 'count'])

# Print the resulting statistics
print(user_stats)
