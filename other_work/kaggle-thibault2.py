def calculate_features(data):
    dtypes = {'id': 'category', 'down_event': 'category', 'up_event': 'category', 
              'text_change': 'category', 'activity': 'category'}
    data = pd.read_csv(file_path, dtype=dtypes)

    # Calculate time difference and active time
    data['time_diff'] = data.groupby('id')['down_time'].diff()
    data['active'] = data['time_diff'] <= 30000
    data['active_time'] = data['active'].groupby(data['id']).transform('sum') * data['action_time']

    # Character counts
    data['total_characters'] = (data['down_event'] != 'Backspace').groupby(data['id']).cumsum()
    data['total_backspaces'] = (data['down_event'] == 'Backspace').groupby(data['id']).cumsum()

    # Word and sentence lengths
    data['word_length'] = (data['down_event'] == 'Space').groupby(data['id']).cumsum()
    data['sentence_length'] = (data['down_event'] == '.').groupby(data['id']).cumsum()

    # Complexity chars and periods
    complexity_chars = data[data['down_event'].isin([',', ':', ';'])].groupby('id')['down_event'].count()
    num_periods = data[data['down_event'] == '.'].groupby('id')['down_event'].count()

    # Merge complexity chars and periods into main dataframe
    data = data.merge(complexity_chars.rename('complexity_chars'), on='id', how='left')
    data = data.merge(num_periods.rename('num_periods'), on='id', how='left')

    # Calculate other features
    data['average_word_length'] = data['total_characters'] / data['word_length'].replace(0, np.nan)
    data['average_sentence_length'] = data['total_characters'] / data['sentence_length'].replace(0, np.nan)
    data['sentence_complexity_ratio'] = data['complexity_chars'] / data['num_periods'].replace(0, np.nan)
    data['backspace_percentage'] = (data['total_backspaces'] / data['total_characters'].replace(0, np.nan)) * 100

    # Final aggregation
    final_data = data.groupby('id').agg({
        'active_time': 'sum',
        'total_characters': 'last',
        'total_backspaces': 'last',
        'average_word_length': 'mean',
        'average_sentence_length': 'mean',
        'sentence_complexity_ratio': 'mean',
        'backspace_percentage': 'mean',
        'word_count': 'last'
    }).reset_index()

    return final_data

# Usage
file_path = '/kaggle/input/linking-writing-processes-to-writing-quality/train_logs.csv'
features_df = calculate_features(file_path)

# Write to the temporary directory
temp_file_path = os.path.join(temp_directory, 'extracted_features.csv')
features_df.to_csv(temp_file_path, index=False)

print(f"Features saved to temporary file: {temp_file_path}")

from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

# Load features and scores
features_df = pd.read_csv('/kaggle/temp/extracted_features.csv')
scores_df = pd.read_csv('/kaggle/input/linking-writing-processes-to-writing-quality/train_scores.csv')

# Merge features and scores
merged_df = features_df.merge(scores_df, on='id')

# Split data
X = merged_df.drop(['id', 'score'], axis=1)  # Features
y = merged_df['score']  # Target variable
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# Impute NaN values with the median for both training and validation sets
imputer = SimpleImputer(strategy='median')
X_train_imputed = imputer.fit_transform(X_train)
X_val_imputed = imputer.transform(X_val)

# Scaling the features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train_imputed)
X_val_scaled = scaler.transform(X_val_imputed)

# Training and validating the model
rf = RandomForestRegressor(n_estimators=100, random_state=42)
rf.fit(X_train_scaled, y_train)
y_pred = rf.predict(X_val_scaled)
mse = mean_squared_error(y_val, y_pred)
rmse = np.sqrt(mse)

print("Validation RMSE:", rmse)

# Load the test data
test_df = pd.read_csv('/kaggle/input/linking-writing-processes-to-writing-quality/test_logs.csv')

# define the scoring intervals of .5
def round_to_half(number):
    """Round a number to the nearest half."""
    return round(number * 2) / 2

# Apply the same feature extraction process to the test data
# You should use the same 'calculate_features' function you defined earlier
test_features_df = calculate_features(test_df)

# Preprocess the test features
# Impute missing values
test_features_imputed = imputer.transform(test_features_df.drop(['id'], axis=1))

# Scale the features
test_features_scaled = scaler.transform(test_features_imputed)

# Make predictions
test_predictions = rf.predict(test_features_scaled)

# Apply the custom rounding function to each prediction
rounded_predictions = [round_to_half(score) for score in test_predictions]

# Prepare the submission file
# submission_df = pd.DataFrame({'id': test_features_df['id'], 'PredictedScore': test_predictions})
# submission_df.to_csv('/kaggle/temp/submission.csv', index=False)

# Prepare the submission file with the rounded predictions
submission_df = pd.DataFrame({'id': test_features_df['id'], 'PredictedScore': rounded_predictions})
submission_df = submission_df.rename(columns={'PredictedScore': 'score'})
submission_df.to_csv('/kaggle/temp/submission.csv', index=False)

print("Training Data file with rounded scores created successfully in temp.")
