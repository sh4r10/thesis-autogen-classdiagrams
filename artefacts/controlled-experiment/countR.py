def count_relationship_lines(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    start_section = "# RELATIONSHIP DIFFERENCES"
    end_section = "# STATISTICS"
    
    count = 0
    in_section = False
    
    for line in lines:
        line = line.strip()
        if line == start_section:
            in_section = True
            continue
        if line == end_section:
            in_section = False
            continue
        if in_section and line.startswith("Relationship"):
            count += 1
    
    return count

# Example usage
file_path = 'all_commands_output.txt'
relationship_lines_count = count_relationship_lines(file_path)
print(f"Number of 'Relationship' lines: {relationship_lines_count}")
