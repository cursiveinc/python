import json

def process_key_events(events):
    """
    Process keydown events to extract text, handling backspaces and other special keys.
    """
    text = []
    for event in events:
        key = event.get('key', '')
        
        # Handle backspace
        if key == 'BACKSPACE':
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
        data_content = data.get("data", [])
        keydown_events = [event for event in data_content if event.get('event') == 'keydown']

        # Process the keydown events
        return process_key_events(keydown_events)
    except Exception as e:
        return f"An error occurred: {e}"

# Example usage of the function
# Replace the path below with the path to your JSON file
processed_text = extract_text_from_keylog(r'C:\Users\josep\Downloads\revision-1519.json')
print(processed_text)
