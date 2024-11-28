import os
import pickle
import argparse
import statistics
import matplotlib.pyplot as plt
from compile_stats import get_f1_scores

def plot_f1_scores(target_dir, output_file):
    scores = get_f1_scores(target_dir)[1]
    print(scores)
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

