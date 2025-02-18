import os
import shutil
import subprocess

# List of categories to process
categories = ["classes", "relationships", "attributes", "methods",
              "access_modifiers", "attribute_type", "method_return_type",
              "parameter_name", "parameter_type"]

# List of source directories (update with your actual directories)
source_directories = [
    "project-1/stats-no-haf",
    "project-1/stats-haf",
    "project-2/stats-no-haf",
    "project-2/stats-haf",
    "project-3/stats-no-haf",
    "project-3/stats-haf",
    "project-4/stats-no-haf",
    "project-4/stats-haf",
    "project-5/stats-no-haf",
    "project-5/stats-haf",
] 

# Define the base folder for the dataset
dataset_folder = "dataset"

# Ensure the dataset folder exists
if not os.path.exists(dataset_folder):
    os.makedirs(dataset_folder)

# Function to call find_max.py and get the resulting file
def find_max_for_category(source_folder, category):
    # Call the find_max.py script with the category
    result = subprocess.run(
        ["python", "find_max.py", source_folder, category],
        capture_output=True,
        text=True
    )
    # Capture the max file output
    if result.returncode == 0:
        # The output is expected to be something like "The max score file is t3-no-haf.stat"
        output_line = result.stdout.strip().split("\n")[-1]
        print(output_line)
        filename = output_line.split()[-1]  
        return filename
    else:
        print(f"Error in find_max.py for category: {category} in {source_folder}")
        print(result.stderr)
        return None

# Function to copy the resulting file to the appropriate location
def copy_file_to_category_folder(source_folder, filename, category):
    if filename:
        # Create category, haf, and no-haf subfolders
        category_folder = os.path.join(dataset_folder, category)
        haf_folder = os.path.join(category_folder, "haf")
        no_haf_folder = os.path.join(category_folder, "no-haf")
        
        # Make sure the directories exist
        os.makedirs(haf_folder, exist_ok=True)
        os.makedirs(no_haf_folder, exist_ok=True)

        # Determine the destination path
        if "no-haf" in filename:  # Check if the filename relates to haf
            destination_folder = no_haf_folder
        else:  # Default to no-haf
            destination_folder = haf_folder
        
        # Define the source path (make sure the filename is correct)
        source_path = os.path.join(source_folder, filename)
        curr_project = "p"+source_folder.split("/")[0].split("-")[1]
        destination_filename = curr_project+"-"+filename
        destination_path= os.path.join(destination_folder, destination_filename)
        
        # Check if the file exists before copying
        if os.path.exists(source_path):
            # Copy the file to the destination folder
            shutil.copy(source_path, destination_path)
            print(f"Copied {filename} to {destination_filename}")
        else:
            print(f"File {filename} not found in {source_folder}")
    else:
        print(f"File for category {category} not found.")

# Main function to process all categories across all source directories
def process_categories():
    for category in categories:
        print(f"Processing category: {category}")
        
        # Loop over each source directory
        for source_folder in source_directories:
            print(f"Processing source directory: {source_folder}")
            
            # Find the max score file for the category from the current source folder
            filename = find_max_for_category(source_folder, category)
            
            # Copy the resulting file to the appropriate subfolder
            copy_file_to_category_folder(source_folder, filename, category)

if __name__ == "__main__":
    process_categories()

