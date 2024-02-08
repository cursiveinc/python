import json
import syllapy

# Function to load and parse the JSON data
def load_log_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data.get("payload", [])

# Function to reconstruct text from key events
def reconstruct_text(events):
    text_output = ""
    for event in events:
        if event['event'] != 'keydown':
            continue  # Only process 'keydown' events

        key = event['key']
        if key == "Enter":
            text_output += " "  # Treat 'Enter' as a space for text reconstruction
        elif key == "Backspace" and text_output:
            text_output = text_output[:-1]  # Remove last character for 'Backspace'
        elif len(key) == 1:  # Add the character to the output if it's a textual character
            text_output += key
        # Ignore other non-textual keys like "Shift", "Ctrl", etc.

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
    return fk_grade

# Main function to load data, reconstruct text, and calculate readability
def main(file_path):
    events = load_log_data(file_path)
    reconstructed_text = reconstruct_text(events)
    fk_grade_level = calculate_readability(reconstructed_text)
    
    print(f"Reconstructed Text: {reconstructed_text}")
    print(f"Flesch-Kincaid Grade Level: {fk_grade_level}")

# Example usage - replace 'path_to_your_file.json' with your actual file path
file_path = r'C:\Users\josep\Desktop\logs\joseph.thibault@gmail.com\docs.google.com\document\d\1KuNUWW44JuQp63vYFeNlsBef3mdiXdE_oxnHnhjyFdk\edit\1707138577097-1707138686182.json'
main(file_path)


