import os
import json
import re
import base64
import time
import requests
from PIL import Image

# Set the model name (adjust if needed)
MODEL = "llava:13b"

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

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
    
    score_match = re.search(r'Score:\s*(\d\.\d)', response_text)
    if score_match:
        score = float(score_match.group(1))
        return round(score, 1), response_text
    else:
        return 0.0, response_text

def get_relevant_posts(root_directory, relevant_filenames_json):
    with open(os.path.join(root_directory, relevant_filenames_json), 'r') as f:
        relevant_data = json.load(f)
        return set(file.replace('.json', '') for file in relevant_data['filenames'])

def analyze_posts(root_directory, relevant_posts):
    results = {}
    total_analyzed = 0
    total_relevant_pictures = 0

    for subdir, _, files in os.walk(root_directory):
        for filename in files:
            if filename.endswith(('.png', '.jpg', '.jpeg')):
                post_id = filename.split('_')[0]
                if post_id in relevant_posts:
                    total_relevant_pictures += 1
                    image_path = os.path.join(subdir, filename)
                    
                    # Check if analysis already exists
                    analysis_filename = f"{os.path.splitext(filename)[0]}-cta-img-loc.json"
                    analysis_path = os.path.join(subdir, analysis_filename)
                    
                    if not os.path.exists(analysis_path):
                        try:
                            start_time = time.time()
                            cta_score, api_response = analyze_image_for_cta(image_path)
                            total_analyzed += 1

                            analysis_result = {
                                "original_loc_filename": filename,
                                "cta_img_loc_score": cta_score,
                                "api_img_loc_response": api_response
                            }

                            with open(analysis_path, "w", encoding="utf-8") as outfile:
                                json.dump(analysis_result, outfile, indent=4)

                            end_time = time.time()
                            time_taken = end_time - start_time

                            print(f"{filename}: {cta_score} (Result saved to {analysis_filename})")
                            print(f"Time taken to process {filename}: {time_taken:.2f} seconds")

                        except Exception as e:
                            print(f"{filename}: An unexpected error occurred - {e}")
                    else:
                        print(f"Analysis for {filename} already exists. Skipping.")
                        with open(analysis_path, 'r') as f:
                            existing_analysis = json.load(f)
                            cta_score = existing_analysis.get('cta_img_loc_score', 0.0)
                        total_analyzed += 1

                    if post_id not in results:
                        results[post_id] = []
                    results[post_id].append((filename, cta_score))

    return results, total_analyzed, total_relevant_pictures

def save_summary(root_directory, results, total_analyzed, total_relevant_pictures, relevant_posts):
    summary = {
        "total_relevant_posts": len(relevant_posts),
        "total_relevant_pictures": total_relevant_pictures,
        "analyzed_pictures": total_analyzed,
        "posts_with_multiple_pictures": sum(1 for pics in results.values() if len(pics) > 1),
        "cta_scores": {f"{post_id}_{filename}": score for post_id, pics in results.items() for filename, score in pics}
    }

    output_filename = 'updated_cta_analysis_summary.json'
    output_path = os.path.join(root_directory, output_filename)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    print(f"Summary created:")
    print(f"  Total relevant posts: {len(relevant_posts)}")
    print(f"  Total relevant pictures: {total_relevant_pictures}")
    print(f"  Analyzed pictures: {total_analyzed}")
    print(f"  Posts with multiple pictures: {summary['posts_with_multiple_pictures']}")
    print(f"Summary saved to: {output_path}")

if __name__ == "__main__":
    root_directory = r'C:\git\SocialReporter\data'
    relevant_filenames_json = 'relevant_post_filenames.json'
    
    relevant_posts = get_relevant_posts(root_directory, relevant_filenames_json)
    results, total_analyzed, total_relevant_pictures = analyze_posts(root_directory, relevant_posts)
    save_summary(root_directory, results, total_analyzed, total_relevant_pictures, relevant_posts)