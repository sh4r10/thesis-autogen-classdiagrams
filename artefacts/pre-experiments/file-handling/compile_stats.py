import os, pickle, argparse, statistics
from rich import print
from rich.pretty import pprint

def get_f1_scores(target_dir):
    files = []
    scores = {
        "major": [],       
        "moderate": [],       
        "minor": [],       
    }
    for filename in os.listdir(target_dir):
        if filename.endswith(".pkl"):
            print("Reading "+filename+"...")
            files.append(filename)
            with open(os.path.join(target_dir, filename), 'rb') as file:
                loaded_dict = pickle.load(file)
                scores["major"].append(loaded_dict["major"]["f1"])
                scores["moderate"].append(loaded_dict["moderate"]["f1"])
                scores["minor"].append(loaded_dict["minor"]["f1"])
    print("Done.")
    return files, scores

if __name__ == "__main__":
    parser = argparse.ArgumentParser("compile_stats.py");
    parser.add_argument('target_dir')
    parser.add_argument('-f', '--file', action='store')
    parser.add_argument('-d', '--dir', action='store')
    args = parser.parse_args()
    files, scores = get_f1_scores(args.target_dir);
    stats = {
        "files": files,
        "major": {
            "mean": statistics.mean(scores["major"]),
            "variance": statistics.mean(scores["major"]),
        },
        "moderate": {
            "mean": statistics.mean(scores["moderate"]),
            "variance": statistics.mean(scores["moderate"]),
        },
        "minor": {
            "mean": statistics.mean(scores["minor"]),
            "variance": statistics.mean(scores["minor"]),
        }
    }
    pprint(stats, expand_all=True)
    

