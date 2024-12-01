import os
import json
import re
import requests
import chardet
from datetime import datetime
import time
from equipment import myDirectory

def detect_encoding(file_path):
    with open(file_path, 'rb') as file:
        raw_data = file.read()
    return chardet.detect(raw_data)['encoding']

def analyze_text_for_cta(text):
    api_url = "http://localhost:11434/api/generate"
    payload = {
        "model": "llama3.1",
        "prompt": (
            "You work in marketing at a university and you analyze text. "
            f"Analyze the following text for a call to action. The text is:\n\n{text}\n\n"
            "Return a score from 0 to 1 in increments of 0.1 based on the likelihood it contains a call to action.\n"
            "Respond in the following format:\n"
            "Score: [Your score]\n"
            "Reasoning: [Your reasoning]"
        ),
        "stream": False
    }
   
    response = requests.post(api_url, json=payload)
   
    if response.status_code != 200:
        return 0.0, f"Error: HTTP {response.status_code} - {response.text}"
   
    response_json = response.json()
    response_text = response_json.get('response', 'No analysis available')
   
    score_match = re.search(r'Score:\s*(\d+\.?\d*)', response_text)
    if score_match:
        score = float(score_match.group(1))
        return round(score, 1), response_text
    else:
        return 0.0, response_text

directory = myDirectory

start_time = time.time()

for filename in os.listdir(directory):
    if filename.endswith(".json") and not filename.endswith("-cta-local.json"):
        json_path = os.path.join(directory, filename)
        cta_local_path = os.path.join(directory, os.path.splitext(filename)[0] + "-cta-local.json")
        
        file_start_time = time.time()
        
        try:
            # Check if -cta-local.json file exists and has been checked
            if os.path.exists(cta_local_path):
                with open(cta_local_path, "r", encoding="utf-8") as cta_file:
                    cta_data = json.load(cta_file)
                    if cta_data.get("checked", False):
                        print(f"{filename}: Already analyzed. Skipping.")
                        continue
            
            encoding = detect_encoding(json_path)
            with open(json_path, "r", encoding=encoding) as file:
                data = json.load(file)
            
            caption = data.get("caption", "")
            
            if not caption and isinstance(data, dict):
                # Try to find caption in nested structures
                for key, value in data.items():
                    if isinstance(value, dict) and "caption" in value:
                        caption = value["caption"]
                        break
            
            if caption:
                cta_score, api_response = analyze_text_for_cta(caption)
                
                analysis_result = {
                    "original_filename": filename,
                    "cta_txt_score": cta_score,
                    "api_txt_response": api_response,
                    "checked": True,
                    "check_date": datetime.now().isoformat()
                }
                
                with open(cta_local_path, "w", encoding="utf-8") as outfile:
                    json.dump(analysis_result, outfile, indent=4)
                
                print(f"{filename}: {cta_score} (Result saved to {os.path.basename(cta_local_path)})")
            else:
                print(f"{filename}: No caption found.")
                # Create a file indicating it was checked but no caption was found
                analysis_result = {
                    "original_filename": filename,
                    "checked": True,
                    "check_date": datetime.now().isoformat(),
                    "error": "No caption found"
                }
                with open(cta_local_path, "w", encoding="utf-8") as outfile:
                    json.dump(analysis_result, outfile, indent=4)
        
        except json.JSONDecodeError as e:
            print(f"{filename}: Error reading JSON - {e}")
        except Exception as e:
            print(f"{filename}: An unexpected error occurred - {str(e)}")
        
        file_end_time = time.time()
        print(f"Time taken to process {filename}: {file_end_time - file_start_time:.2f} seconds")

end_time = time.time()
print(f"Total processing time: {end_time - start_time:.2f} seconds")
print("Processing complete.")
