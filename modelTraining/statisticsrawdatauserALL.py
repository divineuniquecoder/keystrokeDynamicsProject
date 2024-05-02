import pandas as pd
import ast
import numpy as np
import matplotlib.pyplot as plt

# Load the data
data = pd.read_csv('userALL.csv')

# Function to parse lists from strings
def parse_times(column):
    return data[column].apply(lambda x: ast.literal_eval(x) if pd.notnull(x) else np.nan)

# Convert stringified lists in 'flight_times' and 'dwell_times' to actual lists
data['flight_times'] = parse_times('flight_times')
data['dwell_times'] = parse_times('dwell_times')

# Explode the 'flight_times' lists into rows
data_flight = data[['user_id', 'flight_times']].explode('flight_times')
data_dwell = data[['user_id', 'dwell_times']].explode('dwell_times')

# Convert 'flight_times' and 'dwell_times' to numeric
data_flight['flight_times'] = pd.to_numeric(data_flight['flight_times'], errors='coerce')
data_dwell['dwell_times'] = pd.to_numeric(data_dwell['dwell_times'], errors='coerce')

# Group by 'user_id' and calculate the count for both metrics
flight_stats = data_flight.groupby('user_id')['flight_times'].agg(['count'])
dwell_stats = data_dwell.groupby('user_id')['dwell_times'].agg(['count'])

# Print the resulting statistics
print("Flight Time Stats:")
print(flight_stats)
print("\nDwell Time Stats:")
print(dwell_stats)

# Plotting the count of flight times per user
plt.figure(figsize=(10, 6))
flight_stats['count'].plot(kind='bar', color='skyblue', alpha=0.6, label='Flight Times')
dwell_stats['count'].plot(kind='bar', color='coral', alpha=0.6, label='Dwell Times')
plt.title('Count of Flight and Dwell Times per User')
plt.xlabel('User ID')
plt.ylabel('Number of Observations')
plt.legend()
plt.xticks(rotation=45)
plt.show()
