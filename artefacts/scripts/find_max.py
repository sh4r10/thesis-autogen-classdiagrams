import os
import pickle
import argparse
from rich import print

def get_dicts(target_dir):
    """
    Load all .stat files in the target directory and return a list of tuples 
    containing the filename and the corresponding dictionary.
    """
    dicts = []
    for filename in os.listdir(target_dir):
        if filename.endswith(".stat"):
            filepath = os.path.join(target_dir, filename)
            with open(filepath, 'rb') as file:
                loaded_dict = pickle.load(file)
                dicts.append((filename, loaded_dict))
    return dicts

def get_f1_max_score(target_dir, category):
    """
    Find the file with the maximum F1 score for the given category.
    Returns a tuple of the filename and the F1 score details.
    """
    dicts = get_dicts(target_dir)
    
    if not dicts:
        raise ValueError(f"No valid .stat files found in the directory: {target_dir}")
    
    # Initialize with the first file's data
    max_score = {
        "file": dicts[0][0],
        "precision": dicts[0][1][category]["precision"],
        "recall": dicts[0][1][category]["recall"],
        "f1": dicts[0][1][category]["f1"]
    }

    # Iterate to find the maximum F1 score
    for file, d in dicts:
        score = d[category]["f1"]
        if score > max_score["f1"]:
            max_score = {
                "file": file,
                "precision": d[category]["precision"],
                "recall": d[category]["recall"],
                "f1": score
            }
    return max_score

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compile stats and find the maximum F1 score for a given category.")
    parser.add_argument('target_dir', help="Directory containing .stat files")
    parser.add_argument('category', help="Category to analyze for maximum F1 score")
    args = parser.parse_args()

    try:
        max_f1 = get_f1_max_score(args.target_dir, args.category)
        print(f"[bold green]Max F1 score for category '{args.category}':[/bold green] {max_f1['f1']}")
        print(f"[blue]Details:[/blue] Precision: {max_f1['precision']}, Recall: {max_f1['recall']}")
        print(f"[bold yellow]File:[/bold yellow] {max_f1['file']}")
    except (KeyError, ValueError) as e:
        print(f"[bold red]Error:[/bold red] {e}")

