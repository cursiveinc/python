import os
import json
import pandas as pd
from datetime import datetime

# Complete script with all necessary functions
def extract_person_id_from_filepath(file_path):
    """
    Extracts the personID from the file path assuming the personID is the folder name in email format.

    :param file_path: The full path of the file.
    :return: Extracted personID.
    :path_parts backs up from the lowest folder in Google Docs to identify 
    :the personID(folder name which is email)
    """
    path_parts = file_path.split(os.sep)
    person_id = path_parts[-7] if len(path_parts) > 1 else None
    return person_id

def extract_features_from_json_with_person_id(json_data, file_path):
    """
    Extract required features from the given JSON data, including personID from file path.

    :param json_data: JSON data loaded from a file.
    :param file_path: The full path of the JSON file.
    :return: Extracted features as a dictionary.
    """
    person_id = extract_person_id_from_filepath(file_path)
    latest_timestamp = 0
    total_characters = 0
    total_spaces = 0
    total_periods = 0
    total_backspace = 0

    for event in json_data.get("payload", []):
        timestamp = int(event.get("unixTimestamp", 0))
        latest_timestamp = max(latest_timestamp, timestamp)
        key = event.get("key", "").lower()
        if key:
            total_characters += 1
            if key == ' ':
                total_spaces += 1
            elif key == '.':
                total_periods += 1
            elif key == 'backspace':
                total_backspace += 1

    latest_datetime = datetime.fromtimestamp(latest_timestamp / 1000).strftime('%Y-%m-%d %H:%M:%S')
    return {
        "personId": person_id,
        "latestDatetime": latest_datetime,
        "totalCharacters": total_characters,
        "totalSpaces": total_spaces,
        "totalPeriods": total_periods,
        "totalBackspace": total_backspace
    }

def find_json_files(directory, base_folder_name='logs'):
    json_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.json'):
                json_files.append(os.path.join(root, file))
    return json_files

def process_json_files(directory, output_csv):
    # Check if the CSV file already exists and read it
    file_exists = os.path.isfile(output_csv)
    if file_exists:
        processed_df = pd.read_csv(output_csv)
        # Check if 'filename' column exists, if not create an empty set
        processed_files = set(processed_df['filename'].tolist()) if 'filename' in processed_df.columns else set()
    else:
        processed_files = set()

    all_extracted_features = []  # To store all extracted features
    processed_file_names = []  # To store names of processed files

    # Find all JSON files
    json_files = find_json_files(directory)

    # Process each JSON file
    for file_path in json_files:
        file_name = os.path.basename(file_path)
        if file_name not in processed_files:
            with open(file_path, 'r') as file:
                json_data = json.load(file)
            # Extract features
            extracted_features = extract_features_from_json_with_person_id(json_data, file_path)
            extracted_features['filename'] = file_name  # Add filename to the features
            all_extracted_features.append(extracted_features)
            processed_file_names.append(file_name)

    # Convert to DataFrame and append to CSV only if there are new files
    if all_extracted_features:
        df = pd.DataFrame(all_extracted_features)
        df['processedTimestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        df.to_csv(output_csv, mode='a' if file_exists else 'w', header=not file_exists, index=False)

        # Print the names of the processed files
        print(f"Processed {len(processed_file_names)} new files: {', '.join(processed_file_names)}")
        print(f"Data saved to {output_csv}.")
    else:
        print("No new files to process.")

# Example usage (to be adjusted for your environment)
directory = r'C:\Users\josep\Desktop\logs'
output_csv = r'C:\Users\josep\Desktop\python\log_data.csv'
process_json_files(directory, output_csv)

