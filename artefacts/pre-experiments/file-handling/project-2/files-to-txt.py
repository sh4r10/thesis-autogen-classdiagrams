import os

# List of Java filenames to search for
java_filenames = ["DAO.java", "Food.java", "Item.java",
                  "ItemVisitor.java", "Job.java", "Pet.java", "PetBuilder.java",
                  "RaiseMeUp.java", "User.java", "UserBuilder.java"]

# Path to the directory you want to search
root_dir = '/mnt/lts/thesis/replication-package/Models vs. Code/Version(s) of Source Code Used/2_RaiseMeUp-f3796c5/project/RaiseMeUp/src/raisemeup'

# Output file to append the filenames
output_file = 'files-as-txt.txt'

# Open the output file in append mode
with open(output_file, 'a') as file:
    # Walk through all directories and files in the directory tree
    for dirpath, dirnames, files in os.walk(root_dir):
        # Check each file to see if it's in the list of filenames we're looking for
        for filename in files:
            if filename in java_filenames:
                # Write the header to the output file
                file.write(f"---{filename}---\n")
                # Read the content of the file and write it to the output file
                full_path = os.path.join(dirpath, filename)
                with open(full_path, 'r') as java_file:
                    contents = java_file.read()
                    file.write(contents + '\n\n')


print(f"Search complete. Filenames appended to '{output_file}'.")
