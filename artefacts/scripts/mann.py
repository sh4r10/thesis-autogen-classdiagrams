import os, pickle, argparse, statistics
from scipy.stats import mannwhitneyu
from compile_stats import calculate_comp_score

def get_values(target_dir):
    scores = []
    for filename in os.listdir(target_dir):
        if filename.endswith(".stat"):
            with open(os.path.join(target_dir, filename), 'rb') as file:
                loaded_dict = pickle.load(file)
                score = calculate_comp_score(loaded_dict)
                scores.append(score)
    return scores

if __name__ == "__main__":
    parser = argparse.ArgumentParser("mann.py");
    parser.add_argument('no_haf_group')
    parser.add_argument('haf_group')
    args = parser.parse_args()
    no_haf_scores = get_values(args.no_haf_group) 
    haf_scores = get_values(args.haf_group) 
    print("mannwhitneyu(haf_scores, no_haf_scores)")
    result = mannwhitneyu(haf_scores, no_haf_scores)
    print(result)
    print('mannwhitneyu(haf_scores, no_haf_scores, alternative="two-sided")')
    result = mannwhitneyu(haf_scores, no_haf_scores, alternative="two-sided")
    print(result)
    print('mannwhitneyu(haf_scores, no_haf_scores, alternative="less")')
    result = mannwhitneyu(haf_scores, no_haf_scores, alternative="less")
    print(result)
    print('mannwhitneyu(haf_scores, no_haf_scores, alternative="greater")')
    result = mannwhitneyu(haf_scores, no_haf_scores, alternative="greater")
    print(result)
