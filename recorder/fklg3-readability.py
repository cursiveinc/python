# fklg3-readability.py

import json
import syllapy

# Function to load and parse the JSON data
def load_log_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data.get("data", [])

# Function to reconstruct text from key events
def reconstruct_text(events):
    text_output = ""
    ctrl_pressed = False  # Track the state of the CTRL key
    for event in events:
        key = event['key']

        if event['event'] == 'keydown':
            if key == "Control":
                ctrl_pressed = True  # CTRL key is pressed down
            elif key == "Enter":
                text_output += " "  # Treat 'Enter' as a space for text reconstruction
            elif key == "Backspace":
                if ctrl_pressed and text_output:  # If CTRL was pressed before Backspace
                    # Remove the last word: find the last space after removing trailing spaces
                    text_output = text_output.rstrip()  # Remove trailing spaces
                    last_space = text_output.rfind(' ')
                    # Keep the last space by adding +1 (if there is a space to keep)
                    text_output = text_output[:last_space + 1 if last_space != -1 else 0]
                elif text_output:
                    text_output = text_output[:-1]  # Regular backspace functionality
            elif len(key) == 1:  # If it's a regular character key
                text_output += key
        elif event['event'] == 'keyup' and key == "Control":
            ctrl_pressed = False  # CTRL key is released

    print(text_output)
    return text_output

# Function to calculate the Flesch-Kincaid Grade Level
def calculate_readability(text):
    words = text.split()
    num_sentences = text.count('.') + text.count('!') + text.count('?')
    num_words = len(words)
    num_syllables = sum(syllapy.count(word) for word in words)

    # Ensure we don't divide by zero
    if num_sentences == 0 or num_words == 0:
        return 0

    # Flesch-Kincaid Grade Level formula
    fk_grade = 0.39 * (num_words / num_sentences) + 11.8 * (num_syllables / num_words) - 15.59
    # Ensure fk_grade is within the bounds of 1 and 26
    fk_grade = max(1, min(fk_grade, 22))
    return fk_grade

# Main function to load data, reconstruct text, and calculate readability
def main(file_path):
    events = load_log_data(file_path)
    reconstructed_text = reconstruct_text(events)
    fk_grade_level = calculate_readability(reconstructed_text)

    print(f"Flesch-Kincaid Grade Level: {fk_grade_level}")

# Example usage - replace 'path_to_your_file.json' with your actual file path
file_path = r'C:\Users\josep\Downloads\https___docs.google.com (53).json'
main(file_path)