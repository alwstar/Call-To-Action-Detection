import os
import json
import re
import time  # Import the time module
from openai import OpenAI
from equipment import myKey

# Set the API key and model name
MODEL = "gpt-4o-mini"
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", myKey))

# Function to analyze the text for a call to action and return a score and response
def analyze_text_for_cta(text):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You work in marketing at a university and you analyze text."},
            {"role": "user", "content": f"Analyze the following text for a call to action. The text is:\n\n{text}\n\nReturn a score from 0 to 1 in increments of 0.1 based on the likelihood it contains a call to action."}
        ],
        temperature=0.0,
    )
    response_text = response.choices[0].message.content.strip()

    # Use regex to extract the score from the response text
    score_match = re.search(r'\b(\d\.\d)\b', response_text)
    if score_match:
        score = float(score_match.group(1))
        return round(score, 1), response_text
    else:
        return 0.0, response_text  # Return 0.0 and the full response if the score cannot be parsed

# Function to check if a "-cta-txt" JSON file already exists
def json_text_analysis_exists(json_path):
    json_filename = os.path.splitext(json_path)[0] + "-cta-txt.json"
    return os.path.exists(json_filename)

# Path to the root directory containing the data
root_directory = r'C:\git\SocialReporter\data'

# Traverse the directory structure
for subdir, dirs, files in os.walk(root_directory):
    for filename in files:
        if filename.endswith(".json"):  # Check if the file is a JSON file
            json_path = os.path.join(subdir, filename)

            # Check if the text analysis is already done
            if not json_text_analysis_exists(json_path):
                try:
                    # Read the JSON file
                    with open(json_path, "r", encoding="utf-8") as file:
                        data = json.load(file)

                    # Check if the data is a list or a dictionary
                    if isinstance(data, list):
                        print(f"{filename}: JSON data is a list. Skipping file.")
                        continue
                    
                    # Extract the text instead of caption
                    text_content = data.get("text", "")

                    if text_content:  # Proceed if text exists
                        # Record the start time
                        start_time = time.time()

                        # Analyze the text
                        cta_score, api_response = analyze_text_for_cta(text_content)

                        # Create a new JSON object with the analysis result
                        analysis_result = {
                            "original_filename": filename,
                            "cta_txt_score": cta_score,
                            "api_txt_response": api_response
                        }

                        # Create a new filename with the "-cta-txt" suffix
                        new_filename = os.path.splitext(filename)[0] + "-cta-txt.json"
                        new_filepath = os.path.join(subdir, new_filename)

                        # Write the analysis result to the new JSON file
                        with open(new_filepath, "w", encoding="utf-8") as outfile:
                            json.dump(analysis_result, outfile, indent=4)

                        # Record the end time
                        end_time = time.time()

                        # Calculate the time taken
                        time_taken = end_time - start_time

                        # Output the result and time to the console
                        print(f"{filename}: {cta_score} (Result saved to {new_filename})")
                        print(f"Time taken to process {filename}: {time_taken:.2f} seconds")
                    else:
                        print(f"{filename}: No text found.")
                except json.JSONDecodeError as e:
                    print(f"{filename}: Error reading JSON - {e}")
                except Exception as e:
                    print(f"{filename}: An unexpected error occurred - {e}")
            else:
                print(f"Analysis for {filename} already exists. Skipping.")
