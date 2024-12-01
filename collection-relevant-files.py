import os
import json

def collect_relevant_files(root_directory, relevant_posts_file):
    # Load relevant post IDs
    with open(os.path.join(root_directory, relevant_posts_file), 'r') as f:
        relevant_posts = json.load(f)['filenames']
    
    relevant_files = {}
    
    for post_id in relevant_posts:
        base_name = os.path.splitext(post_id)[0]
        relevant_files[base_name] = {
            'original': post_id,
            'images': [],
            'local_cta_img': [],
            'api_cta_img': [],
            'cta_txt': None
        }
        
        # Search for related files in the directory
        for subdir, _, files in os.walk(root_directory):
            for file in files:
                if file.startswith(base_name):
                    if file.endswith('.png'):
                        relevant_files[base_name]['images'].append(file)
                    elif file.endswith('-cta-img-loc.json'):
                        relevant_files[base_name]['local_cta_img'].append(file)
                    elif file.endswith('-cta-img.json'):
                        relevant_files[base_name]['api_cta_img'].append(file)
                    elif file.endswith('-cta-txt.json'):
                        relevant_files[base_name]['cta_txt'] = file
    
    # Save the structured data
    output_file = os.path.join(root_directory, 'relevant_cta_files.json')
    with open(output_file, 'w') as f:
        json.dump(relevant_files, f, indent=2)
    
    print(f"Collected relevant files saved to: {output_file}")
    return relevant_files

if __name__ == "__main__":
    root_directory = r'C:\git\SocialReporter\data'
    relevant_posts_file = 'relevant_post_filenames.json'
    relevant_files = collect_relevant_files(root_directory, relevant_posts_file)
    
    # Print summary
    total_posts = len(relevant_files)
    total_images = sum(len(post['images']) for post in relevant_files.values())
    total_local_cta = sum(len(post['local_cta_img']) for post in relevant_files.values())
    total_api_cta = sum(len(post['api_cta_img']) for post in relevant_files.values())
    total_txt_cta = sum(1 for post in relevant_files.values() if post['cta_txt'])
    
    print(f"Total relevant posts: {total_posts}")
    print(f"Total images: {total_images}")
    print(f"Total local CTA analyses: {total_local_cta}")
    print(f"Total API CTA analyses: {total_api_cta}")
    print(f"Total text CTA analyses: {total_txt_cta}")