import os, pickle, argparse
from rich.pretty import pprint

if __name__ == "__main__":
    parser = argparse.ArgumentParser("compile_stats.py");
    parser.add_argument('target_file')
    args = parser.parse_args()
    with open(args.target_file, 'rb') as file:
        loaded_dict = pickle.load(file)
        pprint(loaded_dict, expand_all=True)

