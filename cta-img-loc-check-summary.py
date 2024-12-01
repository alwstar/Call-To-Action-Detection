import os
import json
from collections import defaultdict

def find_missing_cta_analyses(root_directory, relevant_filenames_json, output_filename):
    # Load the list of relevant filenames
    with open(os.path.join(root_directory, relevant_filenames_json), 'r') as f:
        relevant_data = json.load(f)
        relevant_filenames = set(file.replace('.json', '') for file in relevant_data['filenames'])

    # Dictionary to store post IDs and their associated picture files
    post_pictures = defaultdict(list)
    analyzed_pictures = set()
    missing_analyses = defaultdict(list)

    # Walk through the directory structure
    for subdir, _, files in os.walk(root_directory):
        for filename in files:
            if filename.endswith(('.png', '.jpg', '.jpeg')):
                # Extract the post ID (assume it's the part before the first dot or underscore)
                post_id = filename.split('.')[0].split('_')[0]
                
                # Check if this post ID is in our relevant list
                if post_id in relevant_filenames:
                    full_path = os.path.join(subdir, filename)
                    post_pictures[post_id].append(full_path)
                    
                    # Check if a corresponding CTA analysis file exists
                    cta_filename = filename.rsplit('.', 1)[0] + '-cta-img-loc.json'
                    if os.path.exists(os.path.join(subdir, cta_filename)):
                        analyzed_pictures.add(full_path)
                    else:
                        missing_analyses[post_id].append(filename)

    # Create the summary
    summary = {
        "total_relevant_posts": len(relevant_filenames),
        "posts_with_multiple_pictures": sum(1 for pics in post_pictures.values() if len(pics) > 1),
        "total_relevant_pictures": sum(len(pics) for pics in post_pictures.values()),
        "analyzed_pictures": len(analyzed_pictures),
        "posts_with_missing_analyses": len(missing_analyses),
        "missing_analyses": dict(missing_analyses)
    }

    # Write the summary to a new JSON file
    output_path = os.path.join(root_directory, output_filename)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    print(f"Summary created:")
    print(f"  Total relevant posts: {summary['total_relevant_posts']}")
    print(f"  Posts with multiple pictures: {summary['posts_with_multiple_pictures']}")
    print(f"  Total relevant pictures: {summary['total_relevant_pictures']}")
    print(f"  Analyzed pictures: {summary['analyzed_pictures']}")
    print(f"  Posts with missing analyses: {summary['posts_with_missing_analyses']}")
    print(f"Summary saved to: {output_path}")

    # Print some examples of posts with missing analyses
    if missing_analyses:
        print("\nExamples of posts with missing CTA analyses:")
        for post_id, pictures in list(missing_analyses.items())[:5]:
            print(f"  {post_id}: {', '.join(pictures)}")
        if len(missing_analyses) > 5:
            print(f"  ... and {len(missing_analyses) - 5} more")
    else:
        print("\nAll relevant pictures have been analyzed.")

if __name__ == "__main__":
    root_directory = r'C:\git\SocialReporter\data'
    relevant_filenames_json = 'relevant_post_filenames.json'
    output_filename = 'missing_cta_analyses_summary.json'
    find_missing_cta_analyses(root_directory, relevant_filenames_json, output_filename)