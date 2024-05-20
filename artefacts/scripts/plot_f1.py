import os
import pickle
import argparse
import statistics
import matplotlib.pyplot as plt

def get_dicts(target_dir):
    dicts = []
    for filename in os.listdir(target_dir):
        if filename.endswith(".stat"):
            with open(os.path.join(target_dir, filename), 'rb') as file:
                loaded_dict = pickle.load(file)
                dicts.append((filename, loaded_dict))
    return dicts

weights =  {
    "major": 0.6,
    "moderate": 0.25,
    "minor": 0.15
}

def calculate_comp_score(target_dict):
    score = 0
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
    scores = []
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
    scores = {
        "major": [],       
        "moderate": [],       
        "minor": [],       
    }
    for filename in os.listdir(target_dir):
        if filename.endswith(".stat"):
            with open(os.path.join(target_dir, filename), 'rb') as file:
                loaded_dict = pickle.load(file)
                scores["major"].append(loaded_dict["major"]["f1"])
                scores["moderate"].append(loaded_dict["moderate"]["f1"])
                scores["minor"].append(loaded_dict["minor"]["f1"])
    return scores

def plot_f1_scores(target_dir, output_file):
    scores = get_f1_scores(target_dir)
    categories = ['major', 'moderate', 'minor']
    
    means = [statistics.mean(scores[cat]) for cat in categories]
    std_devs = [statistics.stdev(scores[cat]) for cat in categories]
    
    plt.bar(categories, means, yerr=std_devs, capsize=10)
    plt.xlabel('Category')
    plt.ylabel('F1 Score')
    plt.title('Mean F1 Score and Standard Deviation')
    plt.savefig(output_file)
    plt.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compile stats and plot F1 scores.")
    parser.add_argument('target_dir', help="Directory containing .stat files")
    parser.add_argument('output_file', help="File to save the plot")
    args = parser.parse_args()
    plot_f1_scores(args.target_dir, args.output_file)

