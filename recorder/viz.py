import json
import os
import pandas as pd
from datetime import datetime

# this file parses the log data for visualization 
# it spits out a "typing_data.csv" file which can be used to create time series visualizations
def process_file(json_data, typing_data):
    events = json_data.get('payload', []) if isinstance(json_data, dict) else json_data

    for event in events:
        if not isinstance(event, dict) or event.get('key') != ' ':
            continue

        timestamp = event.get('unixTimestamp')
        if timestamp and isinstance(timestamp, str):
            try:
                timestamp = int(timestamp)
                date_time = datetime.utcfromtimestamp(timestamp / 1000)  # Convert to datetime object
                typing_data.append({'date': date_time.date(), 'hour': date_time.hour, 'words': 1})
            except ValueError:
                print(f"Invalid timestamp format: {timestamp}")

def read_json_files(directory):
    typing_data = []

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.json'):
                with open(os.path.join(root, file), 'r') as json_file:
                    try:
                        json_data = json.load(json_file)
                        process_file(json_data, typing_data)
                    except json.JSONDecodeError:
                        print(f"Error reading file: {file}")

    return typing_data

directory_path = r'c:\Users\josep\Desktop\joseph.thibault@gmail.com\joseph.thibault@gmail.com'
typing_data = read_json_files(directory_path)

# Convert the list of data to a pandas DataFrame
df_typing = pd.DataFrame(typing_data)
df_typing.to_csv('typing_data.csv', index=False)

print("Data processing complete. Saved to 'typing_data.csv'")
