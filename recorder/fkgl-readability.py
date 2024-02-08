import json

# Proxy syllable count based on word length
syllable_estimates = {
    9: 3.135599662162162, 5: 1.7931175747644408, 11: 3.908404347604225, 7: 2.464257451859668, 
    6: 2.1493303125208234, 8: 2.8036686601803087, 3: 1.1096187175043328, 10: 3.528810449521646, 
    4: 1.3641053989312695, 12: 4.291225847323409, 13: 4.687693099897014, 16: 5.864248704663212, 
    18: 6.576547231270358, 14: 5.091733870967742, 15: 5.486295848448206, 17: 6.218843172331544, 
    19: 6.865591397849462, 21: 7.684523809523809, 20: 7.183673469387755, 22: 7.806451612903226, 
    24: 8.682926829268293, 23: 8.40625, 27: 9.75, 28: 10.666666666666666, 25: 9.0, 26: 9.533333333333333, 
    2: 2.0, 29: 10.285714285714286, 34: 12.75, 31: 11.333333333333334, 30: 10.0, 32: 11.0, 35: 14.0, 45: 19.0
}

def estimate_syllables(word):
    """Estimate the number of syllables in a word based on its length."""
    return syllable_estimates.get(len(word), 1)  # Default to 1 syllable if length not in estimates

def calculate_readability(text):
    """Calculate the estimated Flesch-Kincaid grade level for the given text, 
       with added print statements to debug the counts of words, sentences, and syllables."""
    words = text.split()
    sentences = text.count('.') + text.count('!') + text.count('?')
    
    # Avoid division by zero
    if sentences == 0:
        sentences = 1
    
    total_syllables = sum(estimate_syllables(word) for word in words)
    words_count = len(words)

    # Print the counts for debugging
    print(f"Word Count: {words_count}")
    print(f"Sentence Count: {sentences}")
    print(f"Total Syllables Estimated: {total_syllables}")

    # Flesch-Kincaid grade level formula
    fk_grade_level = 0.39 * (words_count / sentences) + 11.8 * (total_syllables / words_count) - 15.59
    return fk_grade_level

def process_key_events(events):
    """Process key events to reconstruct text.
       This function filters for 'keydown' events and handles character construction,
       including dealing with spaces, punctuation, and backspaces."""
    text = ""
    for event in events:
        if event['event'] == 'keydown':
            key = event['key']
            if key in ['Space', 'Enter']:
                text += ' '
            elif len(key) == 1:  # Assuming it's a character
                text += key
            # Implement handling of backspace if necessary
    return text

def readability_from_key_log(json_file_path):
    """Load key log events from a JSON file and calculate its readability score."""
    with open(json_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        events = data['payload']  # This is the list of events
        text = process_key_events(events)  # Process events to reconstruct text
        print(f"Debug: Type of text is {type(text)}")  # Debug print to check the type
        return calculate_readability(text)  # Now, 'text' is a string

# Correct the example usage path to match your environment or setup
json_file_path = r'C:\Users\josep\Desktop\cursive\JSON\1702475183788-1702475315181.json'
readability_score = readability_from_key_log(json_file_path)
print(f"Estimated Flesch-Kincaid Grade Level: {readability_score}")

