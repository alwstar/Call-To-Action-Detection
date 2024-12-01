import os
import json
from datetime import datetime, timezone

def is_valid_json_file(filename):
    return filename.endswith('.json')

def is_post_from_dec_2023_onwards(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        if 'time' in data:
            post_time = datetime.fromisoformat(data['time'].replace('Z', '+00:00'))
            comparison_date = datetime(2023, 12, 1, tzinfo=timezone.utc)
            return post_time >= comparison_date
    return False

def get_posts_from_dec_2023_onwards(root_directory):
    relevant_filenames = []
   
    for subdir, _, files in os.walk(root_directory):
        for file in files:
            if is_valid_json_file(file):
                file_path = os.path.join(subdir, file)
                if is_post_from_dec_2023_onwards(file_path):
                    relevant_filenames.append(file)
   
    return relevant_filenames

def save_results(filenames, output_file):
    result = {
        'total_posts_from_dec_2023': len(filenames),
        'filenames': filenames
    }
   
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    root_directory = r'C:\git\SocialReporter\data'
    output_file = os.path.join(root_directory, 'relevant_post_filenames.json')
   
    relevant_filenames = get_posts_from_dec_2023_onwards(root_directory)
    save_results(relevant_filenames, output_file)
   
    print(f"Analyse abgeschlossen. {len(relevant_filenames)} Dateien für Posts ab Dezember 2023 gefunden.")
    print(f"Ergebnisse wurden in {output_file} gespeichert.")