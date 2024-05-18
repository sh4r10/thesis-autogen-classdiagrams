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

def get_f1_max_score(target_dir, category):
    dicts = get_dicts(target_dir)
    max_score = (dicts[0][0], dicts[0][1][category]["f1"])
    for file, d in dicts:
        score = d[category]["f1"] 
        if score > max_score[1]:
            max_score = (file, score) 
    return max_score


if __name__ == "__main__":
    parser = argparse.ArgumentParser("compile_stats.py");
    parser.add_argument('target_dir')
    parser.add_argument('category')
    args = parser.parse_args()

    max_f1 = get_f1_max_score(args.target_dir, args.category)
    print(f"The max score for the {args.category} category is {max_f1[1]}, in {max_f1[0]}")

