import os
import json

def create_cta_summary(root_directory, output_filename):
    summary = {}
    total_analyzed = 0

    # Walk through the directory structure
    for subdir, _, files in os.walk(root_directory):
        for filename in files:
            if filename.endswith("-cta-img-loc.json"):
                file_path = os.path.join(subdir, filename)
                
                # Read the CTA analysis result
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Extract the original filename and CTA score
                original_filename = data.get('original_loc_filename', '').replace('.png', '.json')
                cta_score = data.get('cta_img_loc_score', 0.0)
                
                # Add to summary
                summary[original_filename] = cta_score
                total_analyzed += 1

    # Create the final summary dictionary
    final_summary = {
        "total_analyzed_posts": total_analyzed,
        "cta_scores": summary
    }

    # Write the summary to a new JSON file
    output_path = os.path.join(root_directory, output_filename)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(final_summary, f, indent=2, ensure_ascii=False)

    print(f"Summary created with {total_analyzed} posts analyzed.")
    print(f"Summary saved to: {output_path}")

if __name__ == "__main__":
    root_directory = r'C:\git\SocialReporter\data'
    output_filename = 'cta_analysis_summary.json'
    create_cta_summary(root_directory, output_filename)