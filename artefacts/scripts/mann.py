import os, pickle, argparse, statistics
from rich import print
from scipy.stats import rankdata,mannwhitneyu
from compile_stats import calculate_comp_score
import numpy as np

def get_values(target_dir):
    scores = []
    for filename in os.listdir(target_dir):
        if filename.endswith(".stat"):
            with open(os.path.join(target_dir, filename), 'rb') as file:
                loaded_dict = pickle.load(file)
                score = calculate_comp_score(loaded_dict)
                scores.append(score)
    return scores

def vargha_delaney_a12(X, Y):
    combined = np.concatenate((X, Y))
    ranks = rankdata(combined)
    
    # Get ranks corresponding to elements in X
    ranks_X = ranks[:len(X)]
    
    # Calculate rank sum for X
    R_X = np.sum(ranks_X)
    
    n_X = len(X)
    n_Y = len(Y)
    
    A12 = (R_X / (n_X * n_Y)) - ((n_X + 1) / (2 * n_Y))
    return A12


if __name__ == "__main__":
    parser = argparse.ArgumentParser("mann.py");
    parser.add_argument('haf_group')
    parser.add_argument('no_haf_group')
    args = parser.parse_args()
    no_haf_scores = get_values(args.no_haf_group) 
    haf_scores = get_values(args.haf_group) 
    result = mannwhitneyu(haf_scores, no_haf_scores, alternative="greater")
    a12 = vargha_delaney_a12(haf_scores, no_haf_scores)
    print("No HAF: "+str(no_haf_scores))
    print("HAF: "+str(haf_scores))
    print("\n# RESULTS")
    print(result)
    print(f"'Vargha-Delaney A12': {a12}")

