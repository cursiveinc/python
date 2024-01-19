import os
import json
from collections import defaultdict
import pandas as pd

# this is for feature extraction, it creates "user_typing_data.csv" 
# a summary of data by user as identified by the email-based file folder structure. 

def calculate_active_time_and_longest_session(events, idle_threshold=30000):
    active_time = 0
    longest_session = 0
    current_session = 0
    previous_timestamp = None

    for event in sorted(events, key=lambda e: e['unixTimestamp']):
        timestamp = int(event['unixTimestamp'])
        if previous_timestamp is not None:
            idle_time = timestamp - previous_timestamp
            if idle_time <= idle_threshold:
                active_time += idle_time
                current_session += idle_time
                if current_session > longest_session:
                    longest_session = current_session
            else:
                current_session = 0
        previous_timestamp = timestamp

    return active_time, longest_session

def is_special_character(key):
    # Define what constitutes a special character here
    # For simplicity, let's consider punctuation and symbols as special characters
    return not key.isalnum() and not key.isspace()

def extract_user_data(directory):
    user_data = defaultdict(lambda: {
        'documents': set(), 
        'events': [], 
        'total_characters': 0, 
        'total_spaces': 0,
        'backspace_count': 0,
        'special_characters_count': 0
    })

    for root, dirs, files in os.walk(directory):
        json_files = [f for f in files if f.endswith('.json')]
        user_email = None
        path_parts = root.split(os.sep)
        for part in path_parts:
            if '@' in part:
                user_email = part
                break

        if not user_email:
            continue

        for file in json_files:
            with open(os.path.join(root, file), 'r') as f:
                data = json.load(f)
                for event in data['payload']:
                    if event['event'] == 'keydown':  # Assuming 'event' is the relevant key in your data
                        client_id = event['clientId']
                    user_data[user_email]['documents'].add(client_id)
                    user_data[user_email]['events'].append(event)
                    if event['key'] == ' ':
                        user_data[user_email]['total_spaces'] += 1
                    elif event['key'] == 'Backspace':
                        user_data[user_email]['backspace_count'] += 1
                    elif is_special_character(event['key']):
                        user_data[user_email]['special_characters_count'] += 1
                    else:
                        user_data[user_email]['total_characters'] += 1

    for user in user_data:
        events = user_data[user]['events']
        active_time_ms, longest_session_ms = calculate_active_time_and_longest_session(events)
        user_data[user]['documents'] = len(user_data[user]['documents'])
        user_data[user]['active_time_minutes'] = active_time_ms / 60000  # Convert to minutes
        user_data[user]['longest_session_minutes'] = longest_session_ms / 60000  # Convert to minutes
        user_data[user]['total_words'] = user_data[user]['total_spaces'] + 1  # Assuming a space after each word
        user_data[user]['total_pages'] = user_data[user]['total_words'] / 300
        user_data[user]['words_per_minute'] = (user_data[user]['total_words'] / user_data[user]['active_time_minutes']) if user_data[user]['active_time_minutes'] > 0 else 0

    return user_data

def export_to_csv(user_data, filename):
    data_for_csv = [{
        'email': user, 
        'documents': data['documents'], 
        'total_characters': data['total_characters'],
        'total_spaces': data['total_spaces'],
        'total_words': data['total_words'], 
        'total_pages': data['total_pages'],
        'active_time_minutes': data['active_time_minutes'],
        'longest_session_minutes': data['longest_session_minutes'],
        'words_per_minute': data['words_per_minute'],
        'backspace_count': data['backspace_count'],
        'special_characters_count': data['special_characters_count']
    } for user, data in user_data.items()]

    df = pd.DataFrame(data_for_csv)
    df.to_csv(filename, index=False)

# Main execution
directory_path = r'c:\Users\josep\Desktop\logs'  # Replace with your directory path
user_data = extract_user_data(directory_path)
export_to_csv(user_data, 'user_typing_data.csv')

print("Data extraction and export complete!")
