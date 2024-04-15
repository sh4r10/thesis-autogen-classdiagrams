import os

# Set the directory you want to start from
dir_path = '/home/shariq/lts/thesis/replication-package/Models vs. Code/Version(s) of Source Code Used/4_FreeDaysIntern-b306738/Sts/freeday/src/main/java/freedays/timesheet'
output_file_path = 'prompt.txt'

with open(output_file_path, 'w', encoding='utf-8') as output_file:
    # Walk through all files and directories in the specified directory
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            # Check if the file has a .java extension
            if file.endswith('.java'):
                # Create the path to the current file
                file_path = os.path.join(root, file)
                # Write the name of the file to the output file
                output_file.write(f'----{file}----\n')
                # Open and read the contents of the file
                with open(file_path, 'r', encoding='utf-8') as current_file:
                    file_contents = current_file.read()
                    # Write the contents of the file to the output file
                    output_file.write(f'{file_contents}\n\n')

print(
    f'All .java files have been processed. Output is saved in {output_file_path}.')
