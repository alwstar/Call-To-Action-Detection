import os
import json
import re
import requests
import time
from datetime import datetime

# Set the model name
MODEL = "llama3.1"

def analyze_text_for_cta(text):
    api_url = "http://localhost:11434/api/generate"
    payload = {
        "model": MODEL,
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

def get_relevant_posts(root_directory, relevant_filenames_json):
    with open(os.path.join(root_directory, relevant_filenames_json), 'r') as f:
        relevant_data = json.load(f)
        return set(relevant_data['filenames'])

def analyze_captions(root_directory, relevant_posts):
    results = {}
    total_analyzed = 0

    for subdir, _, files in os.walk(root_directory):
        for filename in files:
            if filename in relevant_posts:
                json_path = os.path.join(subdir, filename)
                analysis_filename = f"{os.path.splitext(filename)[0]}-cta-txt-loc.json"
                analysis_path = os.path.join(subdir, analysis_filename)

                if not os.path.exists(analysis_path):
                    try:
                        with open(json_path, 'r', encoding='utf-8') as file:
                            data = json.load(file)

                        text_content = data.get("text", "")

                        if text_content:
                            start_time = time.time()
                            cta_score, api_response = analyze_text_for_cta(text_content)
                            total_analyzed += 1

                            analysis_result = {
                                "original_loc_filenam": filename,
                                "cta_txt_loc_score": cta_score,
                                "api_txt_loc_response": api_response,
                                "analysis_date": datetime.now().isoformat()
                            }

                            with open(analysis_path, "w", encoding="utf-8") as outfile:
                                json.dump(analysis_result, outfile, indent=4)

                            end_time = time.time()
                            time_taken = end_time - start_time

                            print(f"{filename}: {cta_score} (Result saved to {analysis_filename})")
                            print(f"Time taken to process {filename}: {time_taken:.2f} seconds")

                            results[filename] = cta_score
                        else:
                            print(f"{filename}: No text content found.")
                    except Exception as e:
                        print(f"{filename}: An unexpected error occurred - {e}")
                else:
                    print(f"Analysis for {filename} already exists. Skipping.")
                    with open(analysis_path, 'r') as f:
                        existing_analysis = json.load(f)
                        cta_score = existing_analysis.get('cta_caption_score', 0.0)
                    results[filename] = cta_score
                    total_analyzed += 1

    return results, total_analyzed

def save_summary(root_directory, results, total_analyzed, relevant_posts):
    summary = {
        "total_relevant_posts": len(relevant_posts),
        "analyzed_captions": total_analyzed,
        "caption_cta_scores": results
    }

    output_filename = 'cta_txt_analysis_summary.json'
    output_path = os.path.join(root_directory, output_filename)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    print(f"Summary created:")
    print(f"  Total relevant posts: {len(relevant_posts)}")
    print(f"  Analyzed captions: {total_analyzed}")
    print(f"Summary saved to: {output_path}")

if __name__ == "__main__":
    root_directory = r'C:\git\SocialReporter\data'
    relevant_filenames_json = 'relevant_post_filenames.json'
    
    relevant_posts = get_relevant_posts(root_directory, relevant_filenames_json)
    results, total_analyzed = analyze_captions(root_directory, relevant_posts)
    save_summary(root_directory, results, total_analyzed, relevant_posts)