import os
import pickle

def aggregate_stats(stats_list):
    """
    Given a list of stat dictionaries (each with keys "tp", "fp", "fn"),
    compute the aggregated totals and derive precision, recall, and F1.
    """
    total_tp = sum(item.get("tp", 0) for item in stats_list)
    total_fp = sum(item.get("fp", 0) for item in stats_list)
    total_fn = sum(item.get("fn", 0) for item in stats_list)

    precision = total_tp / (total_tp + total_fp) if (total_tp + total_fp) > 0 else 0
    recall = total_tp / (total_tp + total_fn) if (total_tp + total_fn) > 0 else 0
    f1 = (2 * precision * recall / (precision + recall)
          if (precision + recall) > 0 else 0)
    
    return {
        "tp": total_tp,
        "fp": total_fp,
        "fn": total_fn,
        "precision": precision,
        "recall": recall,
        "f1": f1,
    }

# Define groups mapping to the stat categories
grouping = {
    "coarse": ["classes", "relationships"],
    "medium": ["attributes", "methods"],
    "fine": [
        "access_modifiers",
        "attribute_type",
        "method_return_type",
        "parameter_name",
        "parameter_type",
    ],
}

# Base directory containing the dataset
base_dir = "dataset"

# Initialize a results dictionary for both modes, with sub-dictionaries for each group.
# Structure: results[mode][group][project] = list of stat dictionaries
results = {"haf": {"coarse": {}, "medium": {}, "fine": {}},
           "no-haf": {"coarse": {}, "medium": {}, "fine": {}}}

# Process each mode and each group
for mode in ["haf", "no-haf"]:
    for group, categories in grouping.items():
        for category in categories:
            category_dir = os.path.join(base_dir, category, mode)
            if not os.path.isdir(category_dir):
                print(f"Directory not found: {category_dir}")
                continue

            for fname in os.listdir(category_dir):
                if fname.endswith('.stat'):
                    file_path = os.path.join(category_dir, fname)
                    print(f"Reading file: {file_path}")
                    try:
                        with open(file_path, 'rb') as file:
                            data = pickle.load(file)
                            # Extract the stat for the current category.
                            stat = data.get(category)
                            if stat is None:
                                print(f"Category '{category}' not found in {file_path}")
                                continue
                            # Extract the project identifier from the filename (e.g., "p1" from "p1-t3-haf.stat")
                            project = fname.split('-')[0]
                            if project not in results[mode][group]:
                                results[mode][group][project] = []
                            results[mode][group][project].append(stat)
                    except Exception as e:
                        print(f"Error reading {file_path}: {e}")

# Print out aggregated results for each project (p1, p2, etc.) in each mode
for mode in results:
    print(f"\nResults for mode '{mode}':")
    # Get the union of all projects across the three groups for this mode.
    projects = set()
    for group in results[mode]:
        projects.update(results[mode][group].keys())
    
    for project in sorted(projects):
        print(f"\nProject {project}:")
        for group in ["coarse", "medium", "fine"]:
            if project in results[mode][group]:
                aggregated = aggregate_stats(results[mode][group][project])
                print(f"  {group.capitalize()}: Precision: {aggregated['precision']:.2f}, "
                      f"Recall: {aggregated['recall']:.2f}, F1: {aggregated['f1']:.2f}")
            else:
                print(f"  {group.capitalize()}: No data")

