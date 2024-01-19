import os
import json
import pandas as pd

def process_key_events(events):
    """
    Process keydown events to extract text, handling backspaces and ignoring specified special keys.
    """
    text = []
    ignore_keys = {'Enter', 'Shift', 'Control', 'Alt', 'Escape', 'ArrowUp', 'ArrowDown', 'ArrowRight','ArrowLeft', 'Delete'}  # Set of keys to ignore

    for event in events:
        key = event.get('key', '')

        # Ignore specified keys
        if key in ignore_keys:
            continue

        # Handle backspace
        if key == 'Backspace':
            if text:
                text.pop()  # Remove the last character
        # Add other characters
        else:
            text.append(key)

    return ''.join(text)


def extract_text_from_keylog(file_path):
    """
    Extracts text from a key log file where keydown events are recorded.
    
    Args:
    file_path (str): The path to the key log JSON file.

    Returns:
    str: The extracted text after processing keydown events.
    """
    try:
        # Load the file
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        # Extracting the keydown events
        data_content = data.get("payload", [])
        keydown_events = [event for event in data_content if event.get('event') == 'keydown']
        print(f"Processing {len(keydown_events)} keydown events from {file_path}")  # Debug print

        # Process the keydown events
        return process_key_events(keydown_events)
    except Exception as e:
        return f"An error occurred: {e}"
    
def extract_texts_from_directory(directory_path):
    """
    Extracts texts from all JSON files in a given directory.

    Args:
    directory_path (str): The path to the directory containing the JSON files.

    Returns:
    dict: A dictionary with filenames as keys and extracted texts as values.
    """
    texts = {}
    for filename in os.listdir(directory_path):
        if filename.endswith('.json'):
            file_path = os.path.join(directory_path, filename)
            try:
                text = extract_text_from_keylog(file_path)
                texts[filename] = text
            except Exception as e:
                texts[filename] = f"An error occurred while processing {filename}: {e}"
    return texts

# Example usage
directory_path = r'C:\Users\josep\Desktop\logs\graysonhoffman2021@gmail.com\docs.google.com\document\d\1Ire_XLTcGx7QWGgLXzmoFbRh1GSh6endtzKKc2JaqsM\edit'
extracted_texts = extract_texts_from_directory(directory_path)    

# Displaying the extracted texts
for filename, text in extracted_texts.items():
    print(f"File: {filename}\nExtracted Text: {text}\n")

