import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV files
df1 = pd.read_csv('task1_local_stats_history.csv')
df2 = pd.read_csv('task2_vmss_failover_stats_history.csv')
df3 = pd.read_csv('task3_scale_test_stats_history.csv')
df4 = pd.read_csv('task4_function_test_stats_history.csv')

# Function to process dataframe: normalize time
def process_df(df):
    # Sort just in case
    df = df.sort_values('Timestamp')
    # Normalize timestamp to start at 0
    df['Time'] = df['Timestamp'] - df['Timestamp'].iloc[0]
    return df

df1 = process_df(df1)
df2 = process_df(df2)
df3 = process_df(df3)
df4 = process_df(df4)

# Plotting
plt.figure(figsize=(10, 6))

plt.plot(df1['Time'], df1['Requests/s'], label='Locally deployed')
plt.plot(df2['Time'], df2['Requests/s'], label='VM scaleset (Failover)')
plt.plot(df3['Time'], df3['Requests/s'], label='Autoscale Webapp')
plt.plot(df4['Time'], df4['Requests/s'], label='Autoscale Function')

plt.xlabel('Time (seconds)')
plt.ylabel('Requests/s')
plt.title('Locust Test: Successful Requests per Second')
plt.legend()
plt.grid(True)

# Save the plot
plt.savefig('locust_graph.png')