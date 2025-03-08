import os
import json
from collections import defaultdict

# Function to gather statistics on character usage in transcription fields
def gather_transcription_stats(directory):
    # Dictionary to hold character counts
    char_counts = defaultdict(int)

    # Iterate through all files in the specified directory
    total_files = 0
    for filename in os.listdir(directory):
        total_files += 1
        if filename.endswith(".json"):
            filepath = os.path.join(directory, filename)
            # Open and read JSON file
            with open(filepath, 'r', encoding='utf-8') as f:
                try:
                    data = json.load(f)
                    # Extract transcription field
                    transcription = data.get("transcription", "")
                    # Update character count for each character in transcription
                    for char in transcription:
                        char_counts[char] += 1
                except json.JSONDecodeError:
                    print(f"Warning: Failed to decode JSON in file {filename}")

    # Sort and print character statistics
    sorted_chars = sorted(char_counts.keys())
    all_used_chars = []

    print("Total JSON files:", total_files)

    for char in sorted_chars:
        print(f"{char} : {char_counts[char]}")
        all_used_chars.append(char)

    print("\nAll used characters sorted:")
    print(all_used_chars)

# Specify the directory containing the JSON files
directory = "./prompt_data/"

# Run the transcription stats function
gather_transcription_stats(directory)
