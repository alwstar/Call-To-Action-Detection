# image analysis source code documentation

Certainly. Here's a comprehensive summary that includes both the method and the findings:

# CTA Analysis in Social Media Posts

This project analyzes Call-to-Action (CTA) elements in social media posts, comparing local and API-based detection methods. The analysis focuses on the prevalence of different CTA types and their impact on engagement rates.

## Method

1. **Data Collection**: 
   - Analyzed 403 social media posts
   - Collected data includes post content, engagement metrics, and CTA scores

2. **CTA Detection**:
   - Local method: Custom algorithm to detect CTAs in text and images
   - API method: Utilized an external API for CTA detection

3. **CTA Categorization**:
   - Categorized posts into: No CTA, Text Only, Image Only
   - Used a threshold score of 0.5 to determine CTA presence

4. **Engagement Analysis**:
   - Calculated engagement rate: (likes + comments) / follower count
   - Compared average engagement rates across CTA categories

5. **Statistical Analysis**:
   - Performed t-tests to assess significance of engagement rate differences
   - Calculated correlations between local and API CTA scores

6. **Visualization**:
   - Created bar charts for CTA distribution and engagement rates
   - Generated histograms for CTA score distributions

## Key Findings

1. **CTA Distribution**:
   - Local method: No CTA (65.51%), Text Only (27.30%), Image Only (7.20%)
   - API method: No CTA (67.74%), Text Only (17.12%), Image Only (15.14%)

2. **Engagement Rates**:
   - Image-based CTAs show the highest average engagement rates for both local (2.05%) and API (1.92%) methods.
   - Text-only CTAs show lower engagement rates compared to posts with no CTA.

3. **Engagement Rate Comparisons** (relative to posts with no CTA):
   - Local method: Image Only (+26.45%), Text Only (-18.51%)
   - API method: Image Only (+24.89%), Text Only (-8.72%)

4. **Statistical Significance**:
   - Local method: 
     - Significant difference for Text Only vs No CTA (p=0.0354)
     - Non-significant difference for Image Only vs No CTA (p=0.1129)
   - API method: 
     - Significant difference for Image Only vs No CTA (p=0.0428)
     - Non-significant difference for Text Only vs No CTA (p=0.4343)

5. **Correlation between Local and API Scores**:
   - Text CTA scores: 0.3411
   - Image CTA scores: 0.2705

## Conclusion

The analysis suggests that image-based CTAs are associated with higher engagement rates, while text-only CTAs might have a negative impact on engagement. However, the statistical significance of these findings varies between the local and API methods:

- The local method shows a significant negative impact of text-only CTAs on engagement.
- The API method indicates a significant positive impact of image-based CTAs on engagement.

These inconsistencies between methods highlight the importance of considering multiple approaches in CTA analysis and interpreting results cautiously. The differences in detection methods (local vs API) underscore the complexity of CTA analysis in social media posts and the need for robust, multi-faceted approaches to draw reliable conclusions.

The methodology combines data processing, statistical analysis, and visualization techniques to provide comprehensive insights into CTA effectiveness in social media posts. By using both local and API-based detection methods, the study offers a more nuanced understanding of CTA impact, revealing potential differences in effectiveness depending on the detection approach used.


# Call to Action (CTA) Analysis Scripts

This repository contains a set of Python scripts designed to analyze images and text for the presence of calls to action (CTAs). The scripts use both cloud-based AI services and local AI models to perform the analysis on a dataset focused on the last 6 months.

## Overview

The scripts in this repository perform the following tasks:

1. Analyze images for CTAs using cloud-based AI (OpenAI's GPT-4o Mini)
2. Analyze images for CTAs using a local AI model (LLaVA:13B)
3. Analyze text for CTAs using cloud-based AI (OpenAI's GPT-4o Mini)
4. Analyze text for CTAs using a local AI model (LLaMa3.1:8B)
5. Analyze a 6-month subset of image data using local AI (LLaVA:13B)
6. Analyze a 6-month subset of text data using local AI (LLaMa3.1:8B)

Each script processes files in a specified directory, performs the analysis, and saves the results in JSON format.

## Scripts

### 1. cta-img-api.py

This script analyzes PNG images for CTAs using OpenAI's GPT-4 Vision API.

- Traverses a specified directory for PNG files
- Encodes images as base64 strings
- Sends images to the GPT-4o Mini API for analysis
- Extracts a CTA score and response from the API
- Saves results in a new JSON file with the "-cta-img" suffix

### 2. cta-img-loc.py

This script performs the same image analysis as cta-img-api.py but uses a local LLaVA model instead of the cloud API.

- Uses the LLaVA:13b model running on localhost
- Saves results in a new JSON file with the "-cta-img-loc" suffix

### 3. cta-text-api.py

This script analyzes text content from JSON files for CTAs using OpenAI's GPT-4 API.

- Reads JSON files and extracts text content
- Sends text to the GPT-4o Mini API for analysis
- Extracts a CTA score and response from the API
- Saves results in a new JSON file with the "-cta-txt" suffix

### 4. cta-txt-loc.py

This script performs the same text analysis as cta-text-api.py but uses a local LLaMa model instead of the cloud API.

- Uses the LLaMa 3.1 model running on localhost
- Saves results in a new JSON file with the "-cta-local" suffix

### 5. cta-img-loc-6months.py

This script analyzes a subset of image data from the last 6 months using the local LLaVA model.

- Reads a list of relevant post filenames from a JSON file
- Processes only the images associated with these relevant posts
- Uses the LLaVA:13b model running on localhost
- Saves individual results in JSON files with the "-cta-img-loc" suffix
- Generates a summary of the analysis in 'updated_cta_analysis_summary.json'

### 6. cta-txt-loc-6months.py

This script analyzes a subset of text data from the last 6 months using the local LLaMa model.

- Reads a list of relevant post filenames from a JSON file
- Processes only the text content associated with these relevant posts
- Uses the LLaMa 3.1 model running on localhost
- Saves individual results in JSON files with the "-cta-txt-loc" suffix
- Generates a summary of the analysis in 'cta_txt_analysis_summary.json'

## Setup and Usage

1. Install the required Python packages:
   ```
   pip install openai Pillow requests chardet
   ```

2. Set up your OpenAI API key in an environment variable or in the `equipment.py` file.

3. Ensure you have the local AI models (LLaVA and LLaMa) set up and running on localhost if you plan to use the local scripts.

4. Adjust the `root_directory` variable in each script to point to your data directory.

5. Create a 'relevant_post_filenames.json' file in your root directory with the list of relevant post filenames for the 6-month analysis.

6. Run the scripts individually:
   ```
   python cta-img-api.py
   python cta-img-loc.py
   python cta-text-api.py
   python cta-txt-loc.py
   python cta-img-loc-6months.py
   python cta-txt-loc-6months.py
   ```

## Output

Each script generates JSON files containing the analysis results. The JSON files include:

- The original filename
- The CTA score (0 to 1 in increments of 0.1)
- The full response from the AI model
- A timestamp of when the analysis was performed

The 6-month analysis scripts also generate summary JSON files with overall statistics.

## Notes

- The scripts skip files that have already been analyzed to avoid duplicate work.
- Error handling is implemented to manage issues with file reading, API calls, and unexpected errors.
- Processing times are logged for each file and for the overall execution.
- The 6-month analysis scripts focus on a subset of data, providing a more targeted analysis of recent posts.

## Customization

You can modify the prompt templates, model names, and file patterns to suit your specific needs. Adjust the scoring logic or output format by modifying the relevant functions in each script. The time range for the 6-month analysis can be adjusted by modifying the 'relevant_post_filenames.json' file.