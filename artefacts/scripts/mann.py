import numpy as np
from scipy.stats import mannwhitneyu

def read_group(prompt):
    numbers = []
    while True:
        user_input = input(prompt+" (press q to finish):").strip()
        if(user_input == "q"):
            break
        try:
            num = float(user_input)
            numbers.append(num)
        except:
            print("Please enter a valid number")

    return numbers


if __name__ == "__main__":
    haf = read_group("Enter values for haf")
    nohaf = read_group("\nEnter values for nohaf")
    
    result = mannwhitneyu(haf, nohaf)
    print(result)

