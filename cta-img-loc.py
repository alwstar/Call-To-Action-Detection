import os
import re
import json
import base64
import time
import requests
from PIL import Image

# Set the model name (adjust if needed)
MODEL = "llava:13b"

# Function to encode the image as a base64 string
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

# Function to analyze the image for a call to action and return a score and response
def analyze_image_for_cta(image_path):
    base64_image = encode_image(image_path)
    
    api_url = "http://localhost:11434/api/generate"
    payload = {
        "model": MODEL,
        "prompt": (
            "You are a helpful assistant that responds in Markdown. Help me analyze this image for a call to action."
            "Analyze the following image for a call to action. Return a score from 0 to 1 in increments of 0.1 based on the likelihood it contains a call to action."
            "Your response should always start with 'Score: ' followed by the number. Then provide a brief reasoning."
        ),
        "images": [base64_image],
        "stream": False
    }
    
    response = requests.post(api_url, json=payload)
    
    if response.status_code != 200:
        return 0.0, f"Error: HTTP {response.status_code} - {response.text}"
    
    response_text = response.json().get('response', 'No description available')
    
    # Use regex to extract the score from the response text
    score_match = re.search(r'Score:\s*(\d\.\d)', response_text)
    if score_match:
        score = float(score_match.group(1))
        return round(score, 1), response_text
    else:
        return 0.0, response_text  # Return 0.0 and the full response if the score cannot be parsed

# Function to check if a "-cta-img-loc" JSON file already exists
def json_analysis_exists(image_path):
    json_filename = os.path.splitext(image_path)[0] + "-cta-img-loc.json"
    return os.path.exists(json_filename)

# Path to the root directory containing the data
root_directory = r'C:\git\SocialReporter\data'

# Traverse the directory structure
for subdir, dirs, files in os.walk(root_directory):
    for filename in files:
        if filename.endswith(".png"):  # Check if the file is a PNG image
            image_path = os.path.join(subdir, filename)
            
            # Check if the analysis is already done
            if not json_analysis_exists(image_path):
                try:
                    # Record the start time
                    start_time = time.time()
                    
                    cta_score, api_response = analyze_image_for_cta(image_path)
                    
                    # Create a new JSON object with the analysis result
                    analysis_result = {
                        "original_loc_filename": filename,
                        "cta_img_loc_score": cta_score,
                        "api_img_loc_response": api_response
                    }
                    
                    # Create a new filename with the "-cta-img-loc" suffix
                    new_filename = os.path.splitext(filename)[0] + "-cta-img-loc.json"
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
                
                except Exception as e:
                    print(f"{filename}: An unexpected error occurred - {e}")
            else:
                print(f"Analysis for {filename} already exists. Skipping.")