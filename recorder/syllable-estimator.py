import collections

def process_hyphenated_words(file_path, encoding='utf-8', error_handling='replace'):
    """
    Process a file of hyphenated words to calculate the average number of syllables per word length,
    with options to handle encoding errors.

    :param file_path: Path to the file containing hyphenated words.
    :param encoding: The encoding used to open the file. Default is 'utf-8'.
    :param error_handling: The method to handle encoding errors ('ignore', 'replace', or 'strict'). Default is 'replace'.
    :return: Dictionary mapping word length to average syllables.
    """
    with open(file_path, 'r', encoding=encoding, errors=error_handling) as file:  # Handle different encodings and errors
        hyphenated_words = file.readlines()

    # Process each word
    word_data = []
    for word in hyphenated_words:
        clean_word = word.strip()  # Remove newline characters
        char_count = len(clean_word.replace("-", ""))  # Count characters excluding hyphens
        hyphen_count = clean_word.count("-")  # Count hyphens
        syllable_count = hyphen_count + 1  # Syllables are hyphen_count + 1
        word_data.append((char_count, syllable_count))

    # Aggregate information to calculate average syllables by word length
    syllables_by_length = collections.defaultdict(int)
    word_counts_by_length = collections.defaultdict(int)

    for char_count, syllable_count in word_data:
        syllables_by_length[char_count] += syllable_count
        word_counts_by_length[char_count] += 1

    # Calculate average syllables per word length
    average_syllables_per_length = {length: syllables_by_length[length] / word_counts_by_length[length]
                                    for length in syllables_by_length}

    return average_syllables_per_length

if __name__ == "__main__":
    # Example usage
    file_path = r'C:\Users\josep\Desktop\cursive\Development\syllable count\full.txt'
    averages = process_hyphenated_words(file_path, encoding='windows-1252', error_handling='replace')
    print(averages)
