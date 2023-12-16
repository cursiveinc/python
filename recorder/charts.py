import pandas as pd
import calplot
import matplotlib 
import matplotlib.pyplot as plt

# Set the default font to Arial or another available font
plt.rcParams['font.family'] = 'Arial'

# Load the CSV file into a pandas DataFrame
df_typing = pd.read_csv(r"C:\Users\josep\Desktop\python\typing_data.csv")

# Ensure 'date' is a datetime object
df_typing['date'] = pd.to_datetime(df_typing['date'])

# Aggregate typing activity by day
daily_typing_activity = df_typing.groupby('date')['words'].sum()

# Create the heatmap calendar
calplot.calplot(daily_typing_activity, cmap='YlGn', suptitle='Typing Activity Heatmap Calendar')

# Group data by hour and calculate the average
hourly_typing_activity = df_typing.groupby('hour')['words'].sum()

# Create the bar chart
plt.figure(figsize=(10, 6))
plt.bar(hourly_typing_activity.index, hourly_typing_activity.values, color='skyblue')
plt.xlabel('Hour of Day')
plt.ylabel('Average Words Typed')
plt.title('Average Words Typed by Hour of Day')
plt.xticks(range(0, 24))  # Set x-ticks to be every hour
plt.grid(axis='y')
plt.show()
