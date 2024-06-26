import os, pickle, argparse, statistics
from rich import print
from rich.pretty import pprint
from rich.console import Console

def get_dicts(target_dir):
    dicts = []
    for filename in os.listdir(target_dir):
        if filename.endswith(".stat"):
            with open(os.path.join(target_dir, filename), 'rb') as file:
                total_elems = 0;
                loaded_dict = pickle.load(file)
                dicts.append((filename, loaded_dict))
    return dicts


weights =  {
    "major": 0.6,
    "moderate": 0.25,
    "minor": 0.15
}

def calculate_comp_score(target_dict):
    score = 0;
    totaled = {"total": 0, "major": {"total": 0, "f1": 0}, "moderate": {"total": 0, "f1": 0}, "minor": {"total": 0, "f1": 0}}

    for c in list(weights.keys()):
        totaled[c]["total"] += target_dict[c]["tp"]
        totaled[c]["total"] += target_dict[c]["fp"] 
        totaled[c]["total"] += target_dict[c]["fn"] 
        totaled["total"] += totaled[c]["total"]
        totaled[c]["f1"] = target_dict[c]["f1"]

    for key in weights.keys():
        ratio = totaled[key]["total"] / totaled["total"]
        score += ratio * weights[key] * totaled[key]["f1"]

    return score * 100


def get_comp_scores(target_dir):
    totaled_items = []
    scores =  []
    dicts = get_dicts(target_dir)
    for file, d in dicts:
        score = calculate_comp_score(d)
        scores.append((file, score))
    
    max_score = scores[0]
    for file, score in scores:
        if score > max_score[1]:
            max_score = (file, score)

    return dict(scores), max_score

def get_f1_scores(target_dir):
    files = []
    scores = {
        "major": [],       
        "moderate": [],       
        "minor": [],       
    }
    for filename in os.listdir(target_dir):
        if filename.endswith(".stat"):
            files.append(filename)
            with open(os.path.join(target_dir, filename), 'rb') as file:
                loaded_dict = pickle.load(file)
                scores["major"].append(loaded_dict["major"]["f1"])
                scores["moderate"].append(loaded_dict["moderate"]["f1"])
                scores["minor"].append(loaded_dict["minor"]["f1"])
    return files, scores

if __name__ == "__main__":
    parser = argparse.ArgumentParser("compile_stats.py");
    parser.add_argument('target_dir')
    args = parser.parse_args()
    stat_files, scores = get_f1_scores(args.target_dir)
    comp_scores, best_comp_score = get_comp_scores(args.target_dir)
    stats = {
        "files": stat_files,
        "major": {
            "mean": statistics.mean(scores["major"]),
            "standard deviation": statistics.stdev(scores["major"]),
            "variance": statistics.variance(scores["major"]),
        },
        "moderate": {
            "mean": statistics.mean(scores["moderate"]),
            "standard deviation": statistics.stdev(scores["moderate"]),
            "variance": statistics.variance(scores["moderate"]),
        },
        "minor": {
            "mean": statistics.mean(scores["minor"]),
            "standard deviation": statistics.stdev(scores["minor"]),
            "variance": statistics.variance(scores["minor"]),
        }
    }
    pprint(stats, expand_all=True)
    print("# COMP SCORES")
    pprint(comp_scores, expand_all=True)
    print(f"\nFile: '{best_comp_score[0]}' has the best Comparison Score: '{best_comp_score[1]}'")
