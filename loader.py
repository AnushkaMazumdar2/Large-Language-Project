import pandas as pd
import os

def load_csv_files_with_subjects(directory):
    combined_df = pd.DataFrame()
    for file in os.listdir(directory):
        if file.endswith('.csv'):
            subject = os.path.splitext(file)[0]
            try:
                df = pd.read_csv(os.path.join(directory, file),encoding='latin1')
                df['Subject'] = subject
                combined_df = pd.concat([combined_df, df], ignore_index=True)
            except Exception as e:
                print(f"Error loading {file}: {e}")
    return combined_df

# Example usage
directory = r'C:\Users\Anushka\OneDrive\Desktop\LLM Project\data'
combined_df = load_csv_files_with_subjects(directory)

# Save the combined DataFrame to a CSV file
combined_df.to_csv('combined_library_data.csv', encoding='utf-8', index=False)
