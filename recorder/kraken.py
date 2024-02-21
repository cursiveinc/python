import json
import os

# this file is for feature extraction and summary of the complete log file directory?
def process_file(json_data):
    client_ids = set()
    total_words = 0
    timestamps = []

    # Accessing the 'payload' key which contains the events
    events = json_data.get('data', []) if isinstance(json_data, dict) else json_data

    for event in events:
        if not isinstance(event, dict):
            continue

        client_ids.add(event.get('clientId'))

        if event.get('key') == ' ':
            total_words += 1

        timestamp = event.get('unixTimestamp')
        if timestamp and isinstance(timestamp, str):
            try:
                # Convert the timestamp string to an integer
                timestamp = int(timestamp)
                timestamps.append(timestamp)
            except ValueError:
                # Handle cases where the conversion fails
                print(f"Invalid timestamp format: {timestamp}")

    # Diagnostic: Print the total number of timestamps and the first few timestamps
    # print(f"Total number of timestamps: {len(timestamps)}")
    # print(f"First few timestamps: {timestamps[:5]}")

    # Calculate total time
    total_time = 0
    if timestamps:
        timestamps.sort()
        start_time = timestamps[0]
        end_time = timestamps[-1]
        total_duration = end_time - start_time

        gaps = 0
        for i in range(1, len(timestamps)):
            gap = timestamps[i] - timestamps[i - 1]
            if gap > 30000:  # 30 seconds in milliseconds
                gaps += gap
                # Diagnostic: Print details about the large gaps
                # print(f"Large gap found: {gap} ms between {timestamps[i - 1]} and {timestamps[i]}")

        total_time = total_duration - gaps
        # Diagnostic: Print the calculated total duration and total time
        # print(f"Total duration: {total_duration} ms, Total time after subtracting gaps: {total_time} ms")

    return client_ids, total_words, total_time

def read_json_files(directory):
    all_client_ids = set()
    total_words = 0
    total_time = 0

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.json'):
                with open(os.path.join(root, file), 'r') as json_file:
                    try:
                        json_data = json.load(json_file)
                        client_ids, file_words, file_time = process_file(json_data)
                        all_client_ids.update(client_ids)
                        total_words += file_words
                        total_time += file_time
                    except json.JSONDecodeError:
                        print(f"Error reading file: {file}")

    return all_client_ids, total_words, total_time

# Replace with the actual path to your JSON files directory
directory_path = r'C:\Users\josep\Desktop\steve'
client_ids, total_words, total_time = read_json_files(directory_path)

# Calculating additional metrics
total_pages = total_words / 300
words_per_minute = (total_words / (total_time / 60000)) if total_time > 0 else 0

print(f"Number of Files Represented: {len(client_ids)}")
print(f"Total Words: {total_words}")
print(f"Total Pages: {total_pages}")
print(f"Total Time (mins): {total_time / 1000 / 60}")
print(f"Words Per Minute: {words_per_minute}")
