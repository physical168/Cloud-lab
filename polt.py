import pandas as pd
import matplotlib.pyplot as plt

# File names
files = {
    'task1': 'task1_local_stats_history.csv',
    'task2': 'task2_vmss_failover_stats_history.csv',
    'task3': 'task3_scale_test_stats_history.csv',
    'task4': 'task4_function_test_stats_history.csv'
}

dataframes = {}

# Load and process data
for key, filename in files.items():
    try:
        df = pd.read_csv(filename)
        if not df.empty:
            df = df.sort_values('Timestamp')
            df['Time'] = df['Timestamp'] - df['Timestamp'].iloc[0]
            dataframes[key] = df
    except Exception as e:
        print(f"Error loading {filename}: {e}")

# Plot 1: All 4 tasks in one plot
plt.figure(figsize=(12, 7))

labels = {
    'task1': 'Locally deployed',
    'task2': 'VM scaleset (Failover)',
    'task3': 'Autoscale Webapp',
    'task4': 'Autoscale Function'
}

colors = {
    'task1': 'blue',
    'task2': 'orange',
    'task3': 'green',
    'task4': 'red'
}

for key, df in dataframes.items():
    plt.plot(df['Time'], df['Requests/s'], label=labels.get(key, key), color=colors.get(key, 'black'))

plt.xlabel('Time (seconds)')
plt.ylabel('Requests/s')
plt.title('Locust Test Results: Comparison of All Tasks')
plt.legend()
plt.grid(True)
plt.savefig('all_tasks_plot.png')
plt.close()

# Plot 2: Task 3 separate plot
if 'task3' in dataframes:
    df3 = dataframes['task3']
    plt.figure(figsize=(10, 6))
    plt.plot(df3['Time'], df3['Requests/s'], label='Autoscale Webapp', color='green')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Requests/s')
    plt.title('Task 3: Autoscale Webapp Performance')
    plt.legend()
    plt.grid(True)
    plt.savefig('task3_plot.png')
    plt.close()
    print("Plots generated: all_tasks_plot.png, task3_plot.png")
else:
    print("Task 3 data not available.")