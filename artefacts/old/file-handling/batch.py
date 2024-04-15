import os
import shutil
import math

# Set the directory you want to start from
source_dir = '/home/shariq/lts/thesis/replication-package/Models vs. Code/Version(s) of Source Code Used/4_FreeDaysIntern-b306738/Sts/freeday/src/main/java/freedays'
output_base_dir = 'batched_java_files'
batch_size = 10

# Function to get all java files in a directory and its subdirectories


def get_all_java_files(directory):
    java_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.java'):
                java_files.append(os.path.join(root, file))
    return java_files


# Create the output base directory if it doesn't exist
if not os.path.exists(output_base_dir):
    os.makedirs(output_base_dir)

java_files = get_all_java_files(source_dir)
num_batches = math.ceil(len(java_files) / batch_size)

for batch_index in range(num_batches):
    batch_output_dir = os.path.join(
        output_base_dir, f'batch_{batch_index + 1}')
    os.makedirs(batch_output_dir)

    start_index = batch_index * batch_size
    end_index = min((batch_index + 1) * batch_size, len(java_files))

    for file_index in range(start_index, end_index):
        source_file_path = java_files[file_index]
        file_name = os.path.basename(source_file_path)
        shutil.copy(source_file_path, batch_output_dir)

print(
    f'Java files have been batched and copied into new directories in "{output_base_dir}".')

