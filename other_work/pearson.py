import pandas as pd
import argparse

def calculate_correlations(file_path, output_file_path):
    # Load the data
    data = pd.read_csv(file_path)

    # Initialize an empty DataFrame to store results
    correlation_results = pd.DataFrame(columns=['id', 'correlation'])

    # Group by 'id' and calculate correlation
    for id, group in data.groupby('id'):
        correlation = group[['cursor_position', 'word_count']].corr().iloc[0, 1]
        correlation_results = correlation_results._append({'id': id, 'correlation': correlation}, ignore_index=True)

    # Write the results to a CSV file
    correlation_results.to_csv(output_file_path, index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calculate correlations.")
    parser.add_argument('file_path', type=str, help="Path to the input CSV file")
    parser.add_argument('output_file_path', type=str, help="Path for the output CSV file")

    args = parser.parse_args()

    calculate_correlations(args.file_path, args.output_file_path)
