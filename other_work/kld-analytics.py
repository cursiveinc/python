import sys
import json
import datetime
from collections import Counter

def timestamp_to_datetime(timestamp):
    """Converts a Unix timestamp to a datetime object."""
    return datetime.datetime.fromtimestamp(int(timestamp)/1000)

def load_data(file_path):
    """Loads JSON data from the given file path."""
    with open(file_path, 'r') as file:
        return json.load(file)

def analyze_keylog_data(data):
    """Performs analysis on keylog data."""
    keydown_events = [e for e in data['data'] if e.get('event') == 'keydown']

    character_keys = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
    key_count = len(keydown_events)
    character_count = sum(1 for e in keydown_events if e.get('key') in character_keys)

    key_frequencies = Counter(e.get('key') for e in keydown_events)
    most_frequent_keys = key_frequencies.most_common()

    special_keys = {'Shift', 'Control', 'Alt', 'Backspace', 'Enter', 'Tab', 'Escape'}
    special_key_count = sum(1 for e in keydown_events if e.get('key') in special_keys)

    # Activity over time sorted chronologically
    time_intervals = Counter(timestamp_to_datetime(e.get('unixTimestamp')).minute for e in keydown_events)
    activity_over_time = sorted(time_intervals.items())

    max_pause = 30
    timestamps = [timestamp_to_datetime(e.get('unixTimestamp')) for e in keydown_events]
    sorted_timestamps = sorted(timestamps)
    adjusted_duration = datetime.timedelta()
    previous_timestamp = None

    for timestamp in sorted_timestamps:
        if previous_timestamp:
            difference = timestamp - previous_timestamp
            if difference.total_seconds() <= max_pause:
                adjusted_duration += difference
        previous_timestamp = timestamp

    return adjusted_duration, key_count, character_count, most_frequent_keys, special_key_count, activity_over_time

def main():
    # Use the file path from the command-line argument
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        print("Please provide a file path.")
        return

    # Load the data
    data = load_data(file_path)

    # Analyze the data
    duration, key_count, character_count, most_frequent_keys, special_key_count, activity_over_time = analyze_keylog_data(data)

    # Output the results
    print(f"Duration of Activity: {duration}")
    print(f"Total Key Count: {key_count}")
    print(f"Total Character Count: {character_count}")
    print(f"Most Frequently Used Keys: {most_frequent_keys}")
    print(f"Special Key Usage Count: {special_key_count}")
    print(f"Activity Over Time: {activity_over_time}")

if __name__ == "__main__":
    main()
