import pandas as pd
import numpy as np

def calculate_features(file_path):
    # Load the data
    data = pd.read_csv(file_path)
    features_df = calculate_features(r'C:\Users\josep\Desktop\train_logs\train_logs.csv')

    # Feature extraction
    # 1. Duration of writing, minus pauses longer than 30 seconds
    data['time_diff'] = data['down_time'].diff()
    active_periods = data[data['time_diff'] <= 30000]
    data['active_time'] = active_periods.groupby('id')['action_time'].transform('sum')

    # 2. Total characters (excluding backspaces)
    data['total_characters'] = data[data['down_event'] != 'Backspace'].groupby('id').cumcount()

    # 3. Total backspaces
    data['total_backspaces'] = data[data['down_event'] == 'Backspace'].groupby('id').cumcount()

    # 4. Average word length (based on "Space" events)
    data['word_length'] = data[data['down_event'] == 'Space'].groupby('id').cumcount()
    data['average_word_length'] = data['total_characters'] / data['word_length']

    # 5. Average sentence length (based on periods)
    data['sentence_length'] = data[data['down_event'] == '.'].groupby('id').cumcount()
    data['average_sentence_length'] = data['total_characters'] / data['sentence_length']

    # 6. Sentence complexity ratio
    complexity_chars = data[data['down_event'].isin([',', ':', ';'])].groupby('id').cumcount()
    data['sentence_complexity_ratio'] = complexity_chars / data['sentence_length']

    # 7. Backspace percentage
    data['backspace_percentage'] = (data['total_backspaces'] / data['total_characters']) * 100

    # 8. Correlation coefficient of cursor location and word count
    # data['cursor_word_correlation'] = data[['cursor_position', 'word_count']].corr().iloc[0, 1]

    # 9. Shannon's entropy
    # char_frequencies = data['down_event'].value_counts(normalize=True)
    # data['shannons_entropy'] = -np.sum(char_frequencies * np.log2(char_frequencies))

    # 10. Last word count per ID
    data['last_word_count'] = data.groupby('id')['word_count'].transform('last')

    # Selecting the last entry per ID for each feature
    final_data = data.groupby('id').last().reset_index()

    # Selecting required columns
    final_data = final_data[['id', 'active_time', 'total_characters', 'total_backspaces', 
                             'average_word_length', 'average_sentence_length', 
                             'sentence_complexity_ratio', 'backspace_percentage', 
                             'last_word_count']]

    # Return the final dataframe
    return final_data

# Print to path
file_path = r'C:\Users\josep\Desktop\train_logs\train_logs.csv'
features_df = calculate_features(file_path)

# Save the output to a CSV file
features_df.to_csv(r'C:\Users\josep\Desktop\train_logs\extracted.csv', index=False)