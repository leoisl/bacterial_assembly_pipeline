import matplotlib.pyplot as plt
import numpy as np
import sys

def main(input_file, output_file, plot_description):
    # Loading the content of the provided file
    with open(input_file, "r") as file:
        lines = file.readlines()

    # Parsing the data
    count = []
    nb_of_runs = []
    for line in lines:
        split_line = line.strip().split()
        count.append(int(split_line[0]))
        nb_of_runs.append(int(split_line[1]))

    # Segregating the counts and number of runs into two groups (<= 20 and > 20)
    count_less_equal_20 = [c for c, n in zip(count, nb_of_runs) if n <= 20]
    count_greater_20 = sum(c for c, n in zip(count, nb_of_runs) if n > 20)
    nb_of_runs_less_equal_20 = [n for n in nb_of_runs if n <= 20]

    # Appending the sum of counts > 20 as a single bar
    count_less_equal_20.append(count_greater_20)
    nb_of_runs_less_equal_20.append("20+")

    # Taking the logarithm of the counts
    log_count_less_equal_20 = np.log(count_less_equal_20)

    # Creating the updated bar plot with specified labels and title
    plt.figure(figsize=(12, 6))
    bars = plt.bar(range(len(nb_of_runs_less_equal_20)), log_count_less_equal_20, color='blue', alpha=0.7)
    plt.xticks(range(len(nb_of_runs_less_equal_20)), nb_of_runs_less_equal_20)  # Setting the x-tick labels
    plt.yscale('log')  # Setting the y-axis to log scale

    # Adding labels to the bars
    for bar, value in zip(bars, count_less_equal_20):
        height = bar.get_height()
        plt.annotate(f'{value}',
                     xy=(bar.get_x() + bar.get_width() / 2, height),
                     xytext=(0, 3),  # 3 points vertical offset
                     textcoords="offset points",
                     ha='center', va='bottom',
                     fontsize=9)

    plt.title(f'Sample x number of runs ({plot_description})')
    plt.xlabel('Number of Runs')
    plt.ylabel('Sample count (log scale)')
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.savefig(output_file)
    print(f"Plot saved to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python script.py <input_file.txt> <output_file.png> <plot_description>")
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        plot_description = sys.argv[3]
        main(input_file, output_file, plot_description)
