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
    "moderate": 0.3,
    "minor": 0.1
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

def append_if_not_empty(cat, arr, field):
    total = cat["tp"];
    if(total > 0):
        arr.append(cat[field])


def get_f1_scores(target_dir, field):
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
                append_if_not_empty(loaded_dict["major"], scores["major"], field)
                append_if_not_empty(loaded_dict["moderate"], scores["moderate"], field)
                append_if_not_empty(loaded_dict["minor"], scores["minor"], field)
    return files, scores


def safe_execute(default, function, *args):
    try:
        return function(*args)
    except:
        return default


if __name__ == "__main__":
    parser = argparse.ArgumentParser("compile_stats.py");
    parser.add_argument('target_dir')
    parser.add_argument('-f', '--field', action='store')
    args = parser.parse_args()
    field = args.field if args.field else "f1"
    stat_files, scores = get_f1_scores(args.target_dir, field)
    comp_scores, best_comp_score = get_comp_scores(args.target_dir)
    print("Stats for field: "+field)
    stats = {
        "files": stat_files,
        "major": {
            "mean": safe_execute("No values", statistics.mean, scores["major"]),
            "standard deviation": safe_execute("No values", statistics.stdev, scores["major"]),
            "variance": safe_execute("No values", statistics.variance, scores["major"]),
        },
        "moderate": {
            "mean": safe_execute("No values", statistics.mean, scores["moderate"]),
            "standard deviation": safe_execute("No values", statistics.stdev, scores["moderate"]),
            "variance": safe_execute("No values", statistics.variance, scores["moderate"]),
        },
        "minor": {
            "mean": safe_execute("No values", statistics.mean, scores["minor"]),
            "standard deviation": safe_execute("No values", statistics.stdev, scores["minor"]),
            "variance": safe_execute("No values", statistics.variance, scores["minor"]),
        }
    }
    pprint(stats, expand_all=True)
    print("# COMP SCORES")
    pprint(comp_scores, expand_all=True)
    print(f"\nFile: '{best_comp_score[0]}' has the best Comparison Score: '{best_comp_score[1]}'")
