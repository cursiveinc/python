import json
import time

# Load and parse the JSON data
def load_log_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data.get("payload", [])

def replay_events(events):
    text_output = ""
    for event in events:
        if event['event'] != 'keydown':
            continue  # Process only 'keydown' events

        key = event['key']

        if key == "Enter":
            text_output += "\n"  # Add a line break for 'Enter'
        elif key == "Backspace":
            text_output = text_output[:-1]  # Remove last character for 'Backspace'
        elif key in ["Shift", "Ctrl", "Control", "ArrowLeft", "ArrowRight","ArrowUp","ArrowDown", "Alt"]:
            continue  # Ignore 'Shift', 'Ctrl', and 'Alt' keys
        else:
            text_output += key  # Add the character to the output

        print(text_output, end='\r', flush=True)
        time.sleep(0.05)  # Adding a small delay to simulate typing

# Load the data
log_events = load_log_data(r'C:\Users\josep\Desktop\logs\joseph.thibault@gmail.com\docs.google.com\document\d\1au7rhQIySpsGqMizEeq-nXrGthkpsaU7qekSxQN3uwo\edit\1702325811916-1702326423098.json')

# Sort the events by 'unixTimestamp'
log_events.sort(key=lambda x: int(x['unixTimestamp']))

# Replay the events with updated controls
replay_events(log_events)